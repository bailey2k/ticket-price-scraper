import httpx
from bs4 import BeautifulSoup

async def fetch_stubhub_prices(event_url: str) -> float:
    async with httpx.AsyncClient() as client:
        response = await client.get(event_url, timeout=10.0)
        response.raise_for_status()
        soup = BeautifulSoup(response.text, 'html.parser')
        listings_container = soup.find("div", id="listings-container")
        
        prices = []
        if listings_container:
            for listing in listings_container.find_all("div"):
                price_text = listing.get_text(strip=True)
                if "$" in price_text:
                    price = float(price_text.replace("$", "")).replace(",", "")
                    prices.append(price)

    lowest_price = min(prices)
    return lowest_price

# TODO: implement any other scraper functions
# async def fetch_seatgeek_prices(event_url: str) -> float:

# if you want to add a new site, just add the name here and fill out the .env accordingly
SCRAPERS = {
    "stubhub": fetch_stubhub_prices,
    # "seatgeek": fetch_seatgeek_prices,
    # "ticketmaster": fetch_ticketmaster_prices,
    # "vividseats": fetch_vividseats_prices,
}