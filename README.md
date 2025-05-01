# Ticket Price Scraper API 

[![Made with FastAPI](https://img.shields.io/badge/Made%20with-FastAPI-0ba360?style=for-the-badge&logo=fastapi&logoColor=white)](https://fastapi.tiangolo.com/)
[![Python](https://img.shields.io/badge/Python-3.10+-blue?style=for-the-badge&logo=python&logoColor=white)](https://www.python.org/)
[![MongoDB](https://img.shields.io/badge/Database-MongoDB-brightgreen?style=for-the-badge&logo=mongodb&logoColor=white)](https://www.mongodb.com/)
[![Email Alerts](https://img.shields.io/badge/Email-Alerts-red?style=for-the-badge&logo=gmail&logoColor=white)](https://developers.google.com/gmail/api)

## Overview

Scrape ticket resale sites and get email alerts when prices drop.  
Built over spring break to help snipe some non-overpriced tickets to sold out events.

Currently relatively accurate, but sometimes gets confused whenever StubHub decides to bait site visitors with "recently sold" ticket prices.

This API scrapes event listings on a timed interval using a headless browser and sends HTML email alerts when ticket prices hit your desired target.

Easily deployable in Docker, which is how I do.

---

## Built With

- Python 3.10+  
- FastAPI  
- MongoDB  
- [Camoufox](https://github.com/daijro/camoufox)(custom Firefox build)  
- SMTP email alerts
- APScheduler 

## Prerequisites

- Python 3.10+  
- MongoDB (Docker or local)  
- SMTP email credentials (Gmail recommended and what I use)  

---

## Installation

### 1. Clone this repo

```bash
git clone https://github.com/bailey2k/ticket-price-scraper.git
cd ticket-price-scraper
```

### 2. Create virtual environment

```bash
python3 -m venv venv
source venv/bin/activate  # macOS/Linux
venv\Scripts\activate     # Windows
```

### 3. Install dependencies

```bash
pip install -r requirements.txt
```

### 4. Start MongoDB using Docker (if necessary)

```bash
docker run -d --name mongo -p 27017:27017 mongo
```

---

## Email Notification Setup

### 1. Create a `.env` file

```bash
touch .env
```

### 2. Copy/paste this in the .env and replace placeholders

```ini
EMAIL_FROM=your_email@gmail.com
EMAIL_PASSWORD=your_app_password
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587
MONGO_URL=mongodb://localhost:27017
TRACK_INTERVAL=60  # price check interval in minutes
```

---

## Running the App

```bash
uvicorn app:app --reload
```

Access the API here: [http://localhost:8000/docs](http://localhost:8000/docs)

---

## API Endpoints

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

### `GET /prices` – Run a price check  
Scrapes prices + sends alert emails (this also runs automatically in the background).


## Like it?
Leave me a star or submit a PR if you'd like to. Anything is welcome.

---

> Made with love by [@bailey2k](https://github.com/bailey2k)
