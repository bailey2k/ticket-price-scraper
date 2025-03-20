# 🎟️ Ticket Price Scraper API

## Overview

A simple scraper in Python I made over spring break that scrapes ticket resale websites and sends an email whenever price drops at or below the price you want.  
For now, tracks Stubhub prices with direct HTML scraping with HTTPX and BeautifulSoup.  
SeatGeek, Ticketmaster, VividSeats hide their prices behind JavaScript, possible to integrate later.

---

## Features
- Tracks ticket prices from supported sites  
- Sends email alerts when price falls at/below your desired price  
- Uses MongoDB for persistent storage to keep tracking  
- FastAPI documentation  
- Automatically removes old events  
- Easily deployable in Docker  

---

## Prerequisites
- Python 3.10+  
- MongoDB  
- Docker (optionally) for containerized deployment  
- SMTP credentials (email/password)  

---

## Installation

### 1️⃣ Clone this repository  
```sh
git clone https://github.com/bailey2k/ticket-price-scraper.git
cd ticket-price-scraper
```

### 2️⃣ Create a virtual environment  
```sh
python3 -m venv venv  # or python -m venv venv  
source venv/bin/activate  # macOS/Linux  
venv\Scripts\activate   # Windows  
```

### 3️⃣ Install dependencies  
```sh
pip install -r requirements.txt
```

### 4️⃣ Set up MongoDB  
```sh
docker run -d --name mongo -p 27017:27017 mongo
```

---

## Set up email alerts  

### 1️⃣ Create a `.env` file  
```sh
touch .env
```

### 2️⃣ Add the following:  
```ini
# Configure your email
EMAIL_FROM=email@gmail.com
EMAIL_PASSWORD=password

# Use a Gmail address above if you don't want to deal with this
SMTP_SERVER=smtp.gmail.com
SMTP_PORT=587

# The interval the price will be checked in minutes
TRACK_INTERVAL=60
# Change to whatever you want or keep this way
MONGO_URL=mongodb://localhost:27017
```

---

## 🚀 Running the API

### 1️⃣ Start MongoDB  
```sh
docker run -d --name mongo -p 27017:27017 mongo
```
*(If running MongoDB locally, keep the port the same.)*

### 2️⃣ Start FastAPI  
```sh
python3 -m uvicorn app:app --host 0.0.0.0 --port 8000 --reload
```
🌎 **API should now available at:**  
http://localhost:8000  

---

## 🌐 API Endpoints  

### 1️⃣ Start tracking an event (`POST /track`)  

Run this command:  
```sh
curl -X POST "http://localhost:8000/track" -H "Content-Type: application/json" -d '{
  "site": "stubhub",
  "event_name": "The Weeknd in Landover, MD",
  "event_url": "https://www.stubhub.com/the-weeknd-landover-tickets-8-2-2025/event/157155913/?quantity=0",
  "event_date": "2025-08-02",
  "target_price": 100,
  "email": "user@example.com"
}'
```

📌 **Parameters:**  
- `site`: The name of the ticket site in lowercase  
- `event_name`: This will be mentioned in the email you get  
- `event_url`: Copy/paste the URL of your desired event *(change the end quantity to `0`)*  
- `event_date`: Format: `YYYY-MM-DD`  
- `target_price`: The maximum amount you want to pay for tickets  
- `email`: The email to send the notification to  

✅ **Response:**  
```json
{"message": "Event added successfully"}
```

---

### 2️⃣ Get all tracked events (`GET /events`)  

Run:  
```sh
curl -X GET "http://localhost:8000/events"
```
✅ **Response:**  
Returns a list of the above event JSONs.

---

### 3️⃣ Check prices and send alerts (`GET /prices`)  

Run:  
```sh
curl -X GET "http://localhost:8000/prices"
```
✅ **If a price drops below your target, you will receive an email alert.**  

---

## ⭐ Like this project? Leave a star!  

If you enjoy this, please **leave a star on GitHub**. ⭐ 
If you'd like to make changes, please do!

TYSM - **bailey2k**  
