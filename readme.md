# AI Creator Intelligence Platform

An AI-powered YouTube analytics platform that collects channel data using the YouTube Data API, stores it in MySQL, performs advanced analytics, and generates AI-driven content insights using Google's Gemini models.

🔗 **Live App:** https://youtube-data-harvesting-lhwgzjqpygjae44mgrbhd6.streamlit.app/

---

## Overview

Creators have access to massive amounts of performance data, but extracting actionable insights from that data is time-consuming.

This project transforms raw YouTube analytics into AI-generated recommendations by combining:

* YouTube Data API
* MySQL Data Warehousing
* SQL Analytics
* Gemini LLM Integration
* Streamlit Dashboard

The platform enables creators to analyze channel performance, identify content patterns, and receive AI-powered recommendations based on real video performance data.

---

## Key Features

### Data Collection & Warehousing

* Fetch channel metadata using YouTube Data API v3
* Store channels, videos, and comments in MySQL
* Maintain a structured analytics database for querying and reporting

### Analytics Dashboard

* Channel performance overview
* Video-level analytics
* Subscriber, views, likes, and engagement metrics
* 10 SQL-powered analytical reports

### AI Creator Insights

Generate AI-powered analysis for top-performing videos:

* Key performance insights
* Content pattern detection
* Topic and format analysis
* Growth recommendations
* Cross-channel content comparisons

The AI analyzes real channel data and identifies recurring themes, content formats, and audience engagement patterns.

---

## Tech Stack

| Layer           | Technology                                   |
| --------------- | -------------------------------------------- |
| Frontend        | Streamlit                                    |
| Backend         | Python                                       |
| Database        | MySQL                                        |
| Data Processing | Pandas                                       |
| APIs            | YouTube Data API v3                          |
| AI Layer        | Gemini 2.5 Flash                             |
| Libraries       | google-genai, mysql-connector-python, pandas |

---

## AI Workflow

```text
YouTube API
     ↓
MySQL Database
     ↓
SQL Analytics
     ↓
Pandas DataFrames
     ↓
Gemini AI
     ↓
Content Insights & Recommendations
```

---

## Analytics Queries

1. Videos and their channels
2. Channels with the most videos
3. Top 10 most viewed videos
4. Comment count per video
5. Videos with the most likes
6. Total likes per video
7. Total views per channel
8. Channels publishing videos in 2022
9. Video duration analysis
10. Videos with the most comments

---

## Project Structure

```text
youtube-data-harvesting/
├── app.py
├── youtube_functions.py
├── notebook.ipynb
├── requirements.txt
├── .env
├── .gitignore
└── README.md
```

---

## Local Setup

### Clone Repository

```bash
git clone https://github.com/akashravuru/youtube-data-harvesting
cd youtube-data-harvesting
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```env
API_KEY=your_youtube_api_key
GEMINI_API_KEY=your_gemini_api_key

HOST=localhost
DB_USER=root
PASSWORD=your_mysql_password
DATABASE=youtube_data
PORT=3306
```

### Run Application

```bash
streamlit run app.py
```

---

## Database Schema

### channels

* channel_ID
* title
* description
* subscriber_count
* view_count
* video_count
* playlist_id

### videos

* video_ID
* channel_ID
* title
* description
* likes
* view_count
* comment_count
* duration
* published_at

### comments

* comment_ID
* video_ID
* comment_text

---

## Future Improvements

* Structured AI outputs
* AI insights for all analytics modules
* Channel benchmarking
* Trend prediction
* Multi-model support
* Creator growth score

---

Built by Akash Ravuru
