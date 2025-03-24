# 🎟️ Ticket Price Scraper API 🎟️  

[![Made with FastAPI](https://img.shields.io/badge/Made%20with-FastAPI-0ba360?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Email Alerts](https://img.shields.io/badge/Email-Alerts-red?style=for-the-badge&logo=gmail&logoColor=white)](https://developers.google.com/gmail/api)

## Overview

🔍 Scrape ticket resale sites and get email alerts when prices drop.  
Built over spring break because I got tired of refreshing StubHub.

This API scrapes event listings using a headless browser and sends HTML email alerts when ticket prices hit your desired target.

---

## 🛠 Built With

- 🐍 Python 3.10+  
- ⚡ FastAPI  
- 🧠 MongoDB  
- 🦊 [Camoufox](https://github.com/daijro/camoufox)(custom Firefox build)  
- 📬 SMTP email alerts (styled w/ HTML)  
- ⏰ APScheduler for background price checks  

---

## ✅ Features

- Tracks ticket prices from StubHub  
- Sends HTML emails when prices fall below your target  
- Stores tracked events persistently in MongoDB  
- Cleans out expired events  
- REST API powered by FastAPI  
- Docker-friendly (MongoDB in one line)  
- Scheduler runs automatically in the background  

---

## 📦 Prerequisites

- Python 3.10+  
- MongoDB (Docker or local)  
- SMTP credentials (Gmail recommended)  

---

## 🧰 Installation

### 1️⃣ Clone this repo

```bash
git clone https://github.com/bailey2k/ticket-price-scraper.git
cd ticket-price-scraper
```

### 2️⃣ Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Start MongoDB using Docker

```bash
docker run -d --name mongo -p 27017:27017 mongo
```

---

## 📧 Email Setup

### 1️⃣ Create a `.env` file

```bash
touch .env
```

### 2️⃣ Add your email credentials

```ini
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MONGO_URL=mongodb://localhost:27017
TRACK_INTERVAL=60  # price check interval in minutes
```

---

## 🚀 Running the App

```bash
uvicorn app:app --reload
```

📍 Swagger UI: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## 🌐 API Endpoints

### `POST /track` – Track an event

```json
{
  "site": "stubhub",
  "event_name": "The Weeknd in Landover, MD",
  "event_url": "https://www.stubhub.com/the-weeknd-landover-tickets-8-2-2025/event/157155913/?quantity=0",
  "event_date": "2025-08-02",
  "target_price": 100,
  "email": "user@example.com"
}
```

### `DELETE /events` – Delete an event by URL

```json
{
  "event_url": "https://stubhub.com/..."
}
```

### `GET /events` – Get all tracked events  
Returns a list of active events stored in MongoDB.

### `GET /prices` – Run a manual price check  
Scrapes prices + sends alert emails (this also runs automatically in the background).

---

## 💌 Email Preview

```text
Subject: 🎟️ Price drop for The Weeknd in Landover, MD on stubhub!
🎟️ Price Alert: The Weeknd in Landover, MD
Event Date: 2025-08-02
Current Price: $150
Your Target: $160
→ View Tickets
```

(HTML-styled + mobile-friendly)

---

## 🗺️ Roadmap

- [ ] Add SeatGeek + VividSeats support  
- [ ] Build a web UI dashboard  
- [ ] Add push notifications / SMS alerts  
- [ ] Track price history over time  

---

## ⭐ Like this project?

If this helped you or you like the idea, please **leave a star** ⭐  
PRs welcome if you want to contribute!

---

> Made with 💻 and overpriced concert tickets by [@bailey2k](https://github.com/bailey2k)
