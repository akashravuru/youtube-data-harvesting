from youtube_functions import *
import streamlit as st
import pandas as pd

cursor = get_cursor()
mydb = get_connection()

page = st.sidebar.radio("Navigation", ["Channel Details", "Videos", "Analytics"])


if page == "Channel Details":
    st.write("Channel Details Page")
    channel_id = st.text_input("Enter YouTube Channel ID")
    if st.button("Fetch & Store Channel"):
        if channel_id:
            store_channel_data(channel_id)
            st.success("Channel data stored successfully!")
        else:
            st.warning("Please enter a Channel ID")
    cursor.execute("SELECT channel_ID, title FROM channels")
    channels = cursor.fetchall()
    titles = [channel[1] for channel in channels]
    selected_title = st.selectbox("Select a Channel", ["Select a channel"] + titles)

    if selected_title != "Select a channel":
        for channel in channels:
            
            if channel[1] == selected_title:
                selected_id = channel[0]
                
        cursor.execute("SELECT * FROM channels WHERE channel_ID = %s", (selected_id,))
        channel_data = cursor.fetchone()
        st.subheader(channel_data[1])
        st.caption(channel_data[2]) 
        col1, col2, col3 = st.columns(3)
        col1.metric("Subscribers", channel_data[3])
        col2.metric("Total Views", channel_data[4])
        col3.metric("Total Videos", channel_data[5])


    
elif page == "Videos":
    st.write("Video Details Page")

    channel_id = st.text_input("Enter YouTube Channel ID")

    if st.button("Fetch & Store Channel"):
        if channel_id:
            store_channel_data(channel_id)
            st.success("Channel data stored successfully!")
        else:
            st.warning("Please enter a Channel ID")
    cursor.execute("SELECT channel_ID, title FROM channels")
    channels = cursor.fetchall()
    titles = [channel[1] for channel in channels]
    selected_title = st.selectbox("Select a Channel", ["Select a channel"] + titles)
    
    if selected_title != "Select a channel":
        for channel in channels:
            
            if channel[1] == selected_title:
                selected_id = channel[0]    
        
        cursor.execute("""
        SELECT title, description, view_count, likes, comment_count, published_at
        FROM videos
        WHERE channel_ID = %s
        """, (selected_id,))

        videos = cursor.fetchall()

        cursor.execute("SELECT * FROM channels WHERE channel_ID = %s", (selected_id,))
        channel_data = cursor.fetchone()
        st.subheader(channel_data[1])
        st.caption(channel_data[2]) 
        col1, col2, col3 = st.columns(3)
        col1.metric("Subscribers", channel_data[3])
        col2.metric("Total Views", channel_data[4])
        col3.metric("Total Videos", channel_data[5])
            

        df = pd.DataFrame(videos, columns=["Title", "Description", "Views", "Likes", "Comments", "Published"])
        st.dataframe(df)

        for video in videos:

            st.subheader(video[0])      # title
            st.caption(video[1])        # description
            col1, col2, col3 = st.columns(3)
            col1.metric("Views", video[2])
            col2.metric("Likes", video[3])
            col3.metric("Comments", video[4])
            st.text(f"Published: {video[5]}")
            st.divider()

           
    
elif page == "Analytics":
    st.title("Analytics")
    
    query_choice = st.selectbox("Select a Query", [
        "1. Videos and their channels",
        "2. Channels with most videos",
        "3. Top 10 most viewed videos",
        "4. Comment count per video",
        "5. Videos with most likes",
        "6. Total likes per video",
        "7. Total views per channel",
        "8. Channels that published in 2022",
        "9. Duration of videos per channel",
        "10. Videos with most comments"
    ])
#Question 1 "1. Videos and their channels"
    if query_choice == "1. Videos and their channels":
        ###QUESTION 1
        cursor.execute("""SELECT videos.title, channels.title 
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID""")
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Title", "Channel Name"])
        st.dataframe(df)
#Question 2 
    if query_choice == "2. Channels with most videos":
        cursor.execute("""
        SELECT channels.title, COUNT(videos.video_ID) AS video_count
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        GROUP BY channels.channel_ID
        ORDER BY video_count DESC
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Title", "Channel Name"])
        st.dataframe(df)
#Question 3
    if query_choice == "3. Top 10 most viewed videos":
        cursor.execute("""
        SELECT videos.title, channels.title, videos.view_count
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        ORDER BY videos.view_count DESC
        LIMIT 10
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Title", "Channel Name", "Views"])
        st.dataframe(df)

#Question "4. Comment count per video"
    if query_choice == "4. Comment count per video":
        cursor.execute("""
        SELECT videos.title, COUNT(comments.comment_ID) AS comment_count
        FROM videos
        LEFT JOIN comments 
        ON videos.video_ID = comments.video_ID
        GROUP BY videos.video_ID
        ORDER BY comment_count DESC
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Title", "Comment Count"])
        st.dataframe(df)

#Question "5. Videos with most likes"
    if query_choice == "5. Videos with most likes":
        cursor.execute("""
        SELECT videos.title, channels.title, videos.likes
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        ORDER BY videos.likes DESC
        LIMIT 10
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Title","Channel Name ","Likes"])
        st.dataframe(df)

#Question "6. Total likes per video",      
        
    if query_choice == "6. Total likes per video":
        cursor.execute("""
        SELECT title, likes
        FROM videos
        ORDER BY likes DESC
        LIMIT 10
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Title","Likes"])
        st.dataframe(df)
#Question "7. Total views per channel"
    if query_choice == "7. Total views per channel":
        cursor.execute("""
        SELECT title, view_count
        FROM channels
        ORDER BY view_count DESC
        """)

        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Channel Name","Views"])
        st.dataframe(df)

#Question "8. Channels that published in 2022"
    if query_choice == "8. Channels that published in 2022":
        cursor.execute("""
        SELECT DISTINCT channels.title
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        WHERE YEAR(videos.published_at) = 2022
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Channel Name"])
        st.dataframe(df)

#Question "9. Duration of videos per channel"
    if query_choice == "9. Duration of videos per channel":
        cursor.execute("""
        SELECT channels.title, videos.title, videos.duration
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        ORDER BY channels.title
        """)
        results = cursor.fetchall()
        
        df = pd.DataFrame(results, columns=["Channel Name","Video Name", "Duration"])
        df['Duration (seconds)'] = df['Duration'].apply(convert_duration)
        df = df.drop(columns=["Duration"])
        
        st.dataframe(df)

#Question "10. Videos with most comments"
    if query_choice == "10. Videos with most comments":
        cursor.execute("""
        SELECT videos.title, channels.title, videos.comment_count
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        ORDER BY videos.comment_count DESC
        LIMIT 10
        """)
        results = cursor.fetchall()
        df = pd.DataFrame(results, columns=["Video Name","Channel Name", "Comment"])
        st.dataframe(df)