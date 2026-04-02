# YouTube Data Harvesting & Warehousing

A Streamlit web application that fetches data from YouTube channels using the YouTube Data API v3, stores it in a MySQL database, and provides interactive analytics and visualizations.

🔗 **Live App:** https://youtube-data-harvesting-lhwgzjqpygjae44mgrbhd6.streamlit.app/

---

## Features

- **Fetch & Store** — Enter any YouTube channel ID to fetch channel info, video details, and comments, stored in MySQL
- **Channel Details** — View subscriber count, total views, video count, and channel description
- **Video Analytics** — Browse all videos for a channel with views, likes, comments, and publish date
- **SQL Analytics** — 10 pre-built SQL queries for deep insights across channels

---

## Tech Stack

| Layer | Technology |
|---|---|
| Frontend | Streamlit |
| Backend | Python |
| Database | MySQL (Railway) |
| API | YouTube Data API v3 |
| Libraries | Pandas, mysql-connector-python |

---

## SQL Queries Covered

1. All videos and their corresponding channels
2. Channels with the most videos
3. Top 10 most viewed videos
4. Comment count per video
5. Videos with the highest likes
6. Total likes per video
7. Total views per channel
8. Channels that published videos in 2022
9. Video durations per channel
10. Videos with the most comments

---

## Project Structure

```
youtube-data-harvesting/
├── app.py                  # Streamlit application
├── youtube_functions.py    # API fetch + MySQL insert functions
├── notebook.ipynb          # Development notebook
├── requirements.txt        # Dependencies
├── .gitignore              # Excludes .env and secrets
└── README.md
```

---

## How to Run Locally

1. Clone the repo:
```
git clone https://github.com/akashravuru/youtube-data-harvesting
```

2. Install dependencies:
```
pip install -r requirements.txt
```

3. Create a `.env` file:
```
API_KEY=your_youtube_api_key
HOST=your_mysql_host
DB_USER=your_mysql_user
PASSWORD=your_mysql_password
DATABASE=your_database_name
PORT=3306
```

4. Run the app:
```
streamlit run app.py
```

---

## Database Schema

**channels** — channel_ID, title, description, subscriber_count, view_count, video_count, playlist_id

**videos** — video_ID, channel_ID, title, description, likes, view_count, comment_count, duration, published_at

**comments** — comment_ID, video_ID, comment_text

---

Built by [Akash Ravuru](https://linkedin.com/in/akashravuru)