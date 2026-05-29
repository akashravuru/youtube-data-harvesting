from youtube_functions import *
import streamlit as st
import pandas as pd
import os

from dotenv import load_dotenv
from google import genai

load_dotenv()

client = genai.Client(
    api_key=os.getenv("GEMINI_API_KEY")
)

cursor = get_cursor()
mydb = get_connection()

page = st.sidebar.radio(
    "Navigation",
    [
        "Channel Details",
        "Videos",
        "Analytics",
        "AI Creator Intelligence"
    ]
    )


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
                
        cursor.execute("SELECT * FROM channels WHERE channel_ID = ?", (selected_id,))
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
        WHERE channel_ID = ?
        """, (selected_id,))

        videos = cursor.fetchall()

        cursor.execute("SELECT * FROM channels WHERE channel_ID = ?", (selected_id,))
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
# Question 3
    if query_choice == "3. Top 10 most viewed videos":
        cursor.execute("""
        SELECT videos.title, channels.title, videos.view_count
        FROM videos
        JOIN channels ON videos.channel_ID = channels.channel_ID
        ORDER BY videos.view_count DESC
        LIMIT 10
        """)

        results = cursor.fetchall()

        df = pd.DataFrame(
            results,
            columns=["Video Title", "Channel Name", "Views"]
        )

        st.subheader("📈 Top 10 Most Viewed Videos")
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
        WHERE strftime('%Y', videos.published_at) = '2022'
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

elif page == "AI Creator Intelligence":

    st.title("🤖 AI Creator Intelligence")

    # TOP VIEWED VIDEOS
    cursor.execute("""
    SELECT videos.title, channels.title, videos.view_count
    FROM videos
    JOIN channels ON videos.channel_ID = channels.channel_ID
    ORDER BY videos.view_count DESC
    LIMIT 10
    """)

    top_views = cursor.fetchall()

    df_views = pd.DataFrame(
        top_views,
        columns=["Video Title", "Channel Name", "Views"]
    )

    st.subheader("📈 Top Viewed Videos")
    st.dataframe(df_views)

    # TOP LIKED VIDEOS
    cursor.execute("""
    SELECT videos.title, channels.title, videos.likes
    FROM videos
    JOIN channels ON videos.channel_ID = channels.channel_ID
    ORDER BY videos.likes DESC
    LIMIT 10
    """)

    top_likes = cursor.fetchall()

    df_likes = pd.DataFrame(
        top_likes,
        columns=["Video Title", "Channel Name", "Likes"]
    )

    st.subheader("❤️ Top Liked Videos")
    st.dataframe(df_likes)

    st.divider()

    # TOP CHANNELS BY VIEWS

    cursor.execute("""
    SELECT title, view_count
    FROM channels
    ORDER BY view_count DESC
    LIMIT 10
    """)

    top_channels = cursor.fetchall()

    df_channels = pd.DataFrame(
        top_channels,
        columns=["Channel Name", "Views"]
    )

    st.subheader("📺 Top Channels By Views")
    st.dataframe(df_channels)

    if st.button("Generate Content Intelligence"):

        views_text = df_views.to_string(index=False)
        likes_text = df_likes.to_string(index=False)
        channels_text = df_channels.to_string(index=False)

        prompt = f"""
        You are a YouTube analytics expert.

        Analyze the following YouTube performance data.

        TOP VIEWED VIDEOS:
        {views_text}

        TOP LIKED VIDEOS:
        {likes_text}

        TOP CHANNELS:
        {channels_text}

        Provide a detailed analysis with the following sections:

        1. KEY INSIGHT
        - What is the single most important takeaway from the data?

        2. CONTENT PATTERNS
        - What recurring themes, formats, topics, title styles, or content categories appear among the top-performing videos?

        3. WINNING FORMATS
        - Which content formats appear to perform best?
        - Examples: shorts, comparisons, reviews, tutorials, podcasts, educational content, lists, etc.
        - Only use formats that are evident from the provided data.

        4. CHANNEL PERFORMANCE ANALYSIS
        - Which channels dominate the dataset?
        - Which channels contribute most of the top-performing content?
        - Are there noticeable differences in performance between channels?

        5. GROWTH OPPORTUNITIES
        - Based only on the available data, what opportunities exist for creators to increase performance?
        - If information is missing, explicitly state the limitation.

        6. RECOMMENDATIONS
        - Provide practical content recommendations supported by the data.
        - Do not recommend strategies that are not supported by the provided information.

        IMPORTANT RULES:
        - Only use information present in the data.
        - Do not assume audience demographics.
        - Do not invent metrics.
        - Do not speculate about watch time, CTR, retention, revenue, or audience behavior unless directly supported by the data.
        - If information is missing, clearly say so.
        - Support observations with examples from the supplied data whenever possible.

        Format your response using clear headings:

        KEY INSIGHT

        CONTENT PATTERNS

        WINNING FORMATS

        CHANNEL PERFORMANCE ANALYSIS

        GROWTH OPPORTUNITIES

        RECOMMENDATIONS
        """

        try:

            with st.spinner("Analyzing channel performance..."):

                response = client.models.generate_content(
                    model="gemini-2.5-flash",
                    contents=prompt
                )

            st.subheader("🤖 AI Content Intelligence")
            st.write(response.text)

        except Exception:
            st.error(
                "AI service is temporarily unavailable. Please try again in a few moments."
            )