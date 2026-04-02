# Imports

import os
import streamlit as st
import pandas as pd
from googleapiclient.discovery import build
import mysql.connector as mc

# Load secrets - works both locally and on Streamlit Cloud
try:
    api_key = st.secrets["API_KEY"]
    host = st.secrets["HOST"]
    db_user = st.secrets["DB_USER"]
    password = st.secrets["PASSWORD"]
    database = st.secrets["DATABASE"]
    port = int(st.secrets["PORT"])
except:
    from dotenv import load_dotenv
    load_dotenv()
    api_key = os.getenv("API_KEY")
    host = os.getenv("HOST")
    db_user = os.getenv("DB_USER")
    password = os.getenv("PASSWORD")
    database = os.getenv("DATABASE")
    port = int(os.getenv("PORT"))

connection = build('youtube', 'v3', developerKey=api_key)

mydb = mc.connect(
    host=host,
    user=db_user,
    password=password,
    database=database,
    port=port
)

cursor = mydb.cursor(buffered=True)
##FETCHING DETAILS
# ------------------ CHANNEL ------------------
def fetch_channel_info(channel_id):
    response = connection.channels().list(
        part="snippet,statistics,contentDetails",
        id=channel_id
    ).execute()

    item = response['items'][0]

    return {
        "channel_id": item['id'],
        "title": item['snippet']['title'],
        "description": item['snippet']['description'],
        "subscriber_count": item['statistics']['subscriberCount'],
        "view_count": item['statistics']['viewCount'],
        "video_count": item['statistics']['videoCount'],
        "playlist_id": item['contentDetails']['relatedPlaylists']['uploads']
    }

# ------------------ VIDEO IDS ------------------
def fetch_video_ids(playlist_id):
    video_ids = []

    request = connection.playlistItems().list(
        part="contentDetails",
        playlistId=playlist_id
    ).execute()

    while True:
        for item in request['items']:
            video_ids.append(item['contentDetails']['videoId'])

        token = request.get('nextPageToken')
        if not token:
            break

        request = connection.playlistItems().list(
            part="contentDetails",
            playlistId=playlist_id,
            pageToken=token
        ).execute()

    return video_ids

# ------------------ VIDEO DETAILS ------------------
def fetch_video_details(video_id):
    response = connection.videos().list(
        part="snippet,statistics,contentDetails",
        id=video_id
    ).execute()

    item = response.get('items', [{}])[0]

    snippet = item.get('snippet', {})
    stats = item.get('statistics', {})
    details = item.get('contentDetails', {})

    return {
        "video_id": item.get('id'),
        "title": snippet.get('title', ""),
        "description": snippet.get('description', ""),
        "likes": stats.get('likeCount', 0),
        "views": stats.get('viewCount', 0),
        "comment_count": stats.get('commentCount', 0),
        "duration": details.get('duration', ""),
        "published_at": snippet.get('publishedAt', "").replace('T', ' ').replace('Z', '')
    }

# ------------------ COMMENTS ------------------
def fetch_comments(video_id):
    comments = []

    try:
        request = connection.commentThreads().list(
            part="snippet",
            videoId=video_id
        ).execute()

        while True:
            for item in request.get('items', []):
                snippet = item['snippet']['topLevelComment']['snippet']

                comments.append({
                    "comment_id": item['snippet']['topLevelComment']['id'],
                    "comment": snippet.get('textDisplay', "")
                })

            token = request.get('nextPageToken')
            if not token:
                break

            request = connection.commentThreads().list(
                part="snippet",
                videoId=video_id,
                pageToken=token
            ).execute()

    except Exception as e:
        print("Comment fetch error:", e)

    return comments

# ------------------ MASTER FETCH ------------------
def fetch_all_video_data(channel_id):
    channel_info = fetch_channel_info(channel_id)
    video_ids = fetch_video_ids(channel_info['playlist_id'])

    videos = []

    for vid in video_ids:
        videos.append({
            "video_details": fetch_video_details(vid),
            "comments": fetch_comments(vid)
        })

    return {
        "channel_info": channel_info,
        "videos": videos
    }

#Inserting Details  
# ------------------ CHANNEL ------------------
def insert_channel_data(channel_info):
    cursor.execute("""
    INSERT IGNORE INTO channels VALUES (%s,%s,%s,%s,%s,%s,%s)
    """, (
        channel_info['channel_id'],
        channel_info['title'],
        channel_info['description'],
        int(channel_info['subscriber_count']),
        int(channel_info['view_count']),
        int(channel_info['video_count']),
        channel_info['playlist_id']
    ))
    mydb.commit()

# ------------------ VIDEO ------------------
def insert_video_data(video_info, channel_id):
    cursor.execute("""
    INSERT IGNORE INTO videos VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s)
    """, (
        video_info['video_id'],
        channel_id,
        video_info['title'],
        video_info['description'],
        int(video_info['likes']),
        int(video_info['views']),
        int(video_info['comment_count']),
        video_info['duration'],
        video_info['published_at']
    ))
    mydb.commit()

# ------------------ COMMENTS ------------------
def insert_comment_data(comment_info, video_id):
    cursor.execute("""
    INSERT IGNORE INTO comments VALUES (%s,%s,%s)
    """, (
        comment_info['comment_id'],
        video_id,
        comment_info['comment']
    ))
    mydb.commit()

# ------------------ PIPELINE ------------------
def store_channel_data(channel_id):
    channel_info = fetch_channel_info(channel_id)
    insert_channel_data(channel_info)

    video_ids = fetch_video_ids(channel_info['playlist_id'])

    for vid in video_ids:
        video_info = fetch_video_details(vid)
        insert_video_data(video_info, channel_id)

        comments = fetch_comments(vid)
        for c in comments:
            insert_comment_data(c, vid)


def convert_duration(duration):
    import re
    if not duration:
        return 0
    match = re.match(r'PT(?:(\d+)H)?(?:(\d+)M)?(?:(\d+)S)?', duration)
    if not match:
        return 0
    hours = int(match.group(1) or 0)
    minutes = int(match.group(2) or 0)
    seconds = int(match.group(3) or 0)
    return hours * 3600 + minutes * 60 + seconds


# Export cursor and connection
def get_cursor():
    return cursor

def get_connection():
    return mydb