
from cfg import settings
from camoufox.async_api import AsyncCamoufox
import asyncio
import re

async def fetch_stubhub_prices(event_url: str):
    async with AsyncCamoufox(headless=True, os="macos") as browser:
        page = await browser.new_page()
        print(f"\nOpening StubHub page: {event_url}")
        await page.goto(event_url)
        await asyncio.sleep(5)  # wait for javascript rendering

        try:
            price_element = await page.query_selector_all("#listings-container div[data-price]")

            # means nothing is listed for the event (or some other screw up)
            # implemented this for small concerts with minimal resale
            if not price_element:
                # for debugging
                print("\nCould not find any ticket listing with a price.")
                return None

            prices = []
            for p in price_element:
                raw_price = await p.get_attribute("data-price")
                if raw_price:
                    try:
                        # Extract only digits and decimal point using regex
                        clean_price = re.sub(r"[^\d.]", "", raw_price)
                        if clean_price:
                            price = float(clean_price)
                            prices.append(price)
                    except ValueError:
                        print(f"Skipping unconvertible price: {raw_price}")
            
            min_price = min(prices)
            print(f"\nLowest price found: ${min_price}")
            return min_price

        except Exception as e:
            print(f"Exception during scraping: {e}")
            return None
        

# TODO: implement any other scraper functions
# async def fetch_seatgeek_prices(event_url: str):

# if you want to add a new site, just add the name here and fill out the .env accordingly
SCRAPERS = {
    "stubhub": fetch_stubhub_prices,
    # "seatgeek": fetch_seatgeek_prices,
    # "ticketmaster": fetch_ticketmaster_prices,
    # "vividseats": fetch_vividseats_prices,
}