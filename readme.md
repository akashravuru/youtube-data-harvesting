# AI Creator Intelligence Platform

An AI-powered analytics platform that transforms raw YouTube channel data into actionable creator insights using SQL analytics, large language models, and interactive visualizations.

### Live Application

🚀 Live Demo: https://youtube-data-harvesting-lhwgzjqpygjae44mgrbhd6.streamlit.app/

### GitHub Repository

💻 GitHub: https://github.com/akashravuru/youtube-data-harvesting

---

## Overview

Most creator dashboards show data.

This platform explains the data.

The AI Creator Intelligence Platform combines YouTube Analytics, SQL-based performance analysis, and Google's Gemini models to identify content patterns, winning formats, channel performance trends, and growth opportunities.

The system ingests channel-level data from YouTube, stores it in a structured analytics database, performs SQL-powered reporting, and generates AI-driven content intelligence from real creator performance metrics.

---

## What Makes This Different?

Instead of simply displaying analytics, the platform acts like an AI Content Strategist.

It can:

* Identify recurring content patterns among top-performing videos
* Analyze creator performance across multiple channels
* Surface winning content formats
* Compare channel performance
* Generate AI-powered recommendations based on actual performance data
* Convert analytics into creator-friendly insights

---

## Features

### YouTube Data Collection

* Fetch channel information using YouTube Data API v3
* Collect video metadata
* Collect comment data
* Build a structured creator dataset

### Analytics Engine

* SQL-powered analytical reports
* Cross-channel analysis
* Performance benchmarking
* Video-level metrics
* Channel-level metrics

### AI Creator Intelligence

Generate AI-powered reports including:

* Key Insights
* Content Pattern Detection
* Winning Content Formats
* Channel Performance Analysis
* Growth Opportunities
* Content Recommendations

---

## Dataset

The platform currently analyzes:

* 6 YouTube Channels
* 930+ Videos
* 204,000+ Comments

---

## Technology Stack

| Layer           | Technology          |
| --------------- | ------------------- |
| Frontend        | Streamlit           |
| Backend         | Python              |
| Database        | SQLite              |
| Data Processing | Pandas              |
| API Integration | YouTube Data API v3 |
| AI Layer        | Gemini 2.5 Flash    |
| Analytics       | SQL                 |
| Deployment      | Streamlit Cloud     |

---

## System Architecture

```text
YouTube Data API
        ↓
Data Collection Layer
        ↓
SQLite Analytics Database
        ↓
SQL Analytics Engine
        ↓
Pandas Data Processing
        ↓
Gemini AI Analysis
        ↓
Creator Intelligence Dashboard
```

---

## Analytics Modules

### Channel Intelligence

* Subscriber Analysis
* View Analysis
* Video Volume Analysis
* Channel Overview

### Video Intelligence

* Video Performance Metrics
* Engagement Analysis
* Likes & Comments Analysis
* Publishing Information

### SQL Analytics

1. Videos and their Channels
2. Channels with the Most Videos
3. Top 10 Most Viewed Videos
4. Comment Count per Video
5. Most Liked Videos
6. Total Likes per Video
7. Total Views per Channel
8. Channels Publishing in 2022
9. Video Duration Analysis
10. Most Commented Videos

### AI Creator Intelligence

The AI layer analyzes:

* Top Viewed Videos
* Top Liked Videos
* Top Performing Channels

and generates:

* Key Insights
* Content Patterns
* Winning Formats
* Channel Performance Analysis
* Growth Opportunities
* Strategic Recommendations

---

## Project Structure

```text
youtube-data-harvesting/
│
├── app.py
├── youtube_functions.py
├── notebook.ipynb
├── requirements.txt
├── youtube_data.db
├── README.md
└── .gitignore
```

---

## Local Installation

### Clone Repository

```bash
git clone https://github.com/akashravuru/youtube-data-harvesting.git

cd youtube-data-harvesting
```

### Install Dependencies

```bash
pip install -r requirements.txt
```

### Configure Environment Variables

```env
API_KEY=YOUR_YOUTUBE_API_KEY
GEMINI_API_KEY=YOUR_GEMINI_API_KEY
```

### Run Application

```bash
streamlit run app.py
```

---

## Future Enhancements

* Multi-channel benchmarking
* AI-generated content strategy reports
* Trend prediction models
* Thumbnail intelligence
* Title optimization recommendations
* Retrieval-Augmented Creator Knowledge Base
* Agentic Creator Copilot

---

## Skills Demonstrated

* Python Development
* SQL Analytics
* Data Engineering
* API Integration
* LLM Application Development
* Prompt Engineering
* Streamlit Application Development
* Data Modeling
* AI Product Development
* End-to-End Deployment

---

Built by Akash Ravuru

AI Engineer • Data Analytics • Applied AI Systems
