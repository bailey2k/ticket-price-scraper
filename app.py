#app.py

from fastapi import FastAPI, HTTPException, BackgroundTasks
from pydantic import BaseModel
from scraper import SCRAPERS
from send_email_module import send_email
from apscheduler.schedulers.background import BackgroundScheduler
from apscheduler.triggers.interval import IntervalTrigger
from cfg import settings
from pymongo import MongoClient
import datetime

app = FastAPI(title = "Ticket Price Tracker API",
              description="Track ticket prices and get email alerts when prices drop.",
              version='1.0.0')
scheduler = BackgroundScheduler()
scheduler.start()

client = MongoClient(settings.mongo_url)
db = client["ticket-tracker"]
events_db = db['tracked_events']

class TrackRequest(BaseModel):
    site: str
    event_url: str
    event_name: str
    event_date: str 
    target_price: float
    email: str

    def to_mongo(self):
        return self.model_dump()
    
@app.post("/track", summary="Track a new event", description="Adds a new event to the tracker and stores it in MongoDB.")
def track_event(event: TrackRequest): 
        if events_db.find_one({"event_url": event.event_url}):
            raise HTTPException(status_code = 400, detail="Event is already being tracked")
        events_db.insert_one(event.to_mongo())
        return {"message": "Event added successfully"}

@app.get("/events", summary="Get the current tracked events", description="Retrieves the current events stored in MongoDB")
def get_tracked_events():
    events = [TrackRequest(**event) for event in events_db.find({}, {"_id": 0})]
    return events

@app.get("/prices", summary="Check the current prices (while removing old ones)", description="Check the current prices of each event that is currently inside the MongoDB database, but also remove any that are out of date.")
async def check_prices():
    for event in events_db.find():
        curr_event = TrackRequest(**event)

        # if event has passed, remove from database 
        if datetime.datetime.strptime(curr_event.event_date, "%Y-%m-%d") < datetime.datetime.now():
            events_db.delete_one({"event_url": curr_event.event_url})

        scraper_fx = SCRAPERS.get(curr_event.site)

        if scraper_fx:
            lowest_price = scraper_fx(curr_event.event_url)
            if lowest_price and lowest_price <= curr_event.target_price:
                await send_email (
                    subject= f"Price below {curr_event.target_price} for {curr_event.event_name} on {curr_event.site}",
                    # hyperlinking to the event page 
                    body= f"""Current price is ${lowest_price} 
                    <a href='{curr_event.event_url}' target='_blank' 
                    style='color: blue; text-decoration: underline;'>Click here to view tickets</a>.""",
                    recipient= curr_event.email,
                )
        
        # TODO: handling some other form of notification. I like email the most.


scheduler.add_job(check_prices, IntervalTrigger(minutes=settings.track_interval))
