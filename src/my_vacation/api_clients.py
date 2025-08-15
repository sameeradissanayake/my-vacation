import httpx
import os
import asyncio
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
WEATHER_API_KEY = os.getenv("WEATHER_API_KEY")

if not GOOGLE_API_KEY:
    raise ValueError("Google API key is missing. Set the GOOGLE_API_KEY environment variable.")


async def get_attractions(destination: str, api_key: str):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.priceLevel"
    }
    payload = {
        "textQuery": f"Give me travel hotspots in {destination}"
    }

    async with httpx.AsyncClient() as client:
        response = await client.post(url, json=payload, headers=headers)
        response.raise_for_status()
        data = response.json()
    
    # Extract results in a clean format
    results = []
    for place in data.get("places", []):
        results.append({
            "name": place.get("displayName", {}).get("text"),
            "address": place.get("formattedAddress"),
            "priceLevel": place.get("priceLevel")
        })
    
    return results


async def get_weather_forecast(city: str, api_key: str):
    url = "https://api.openweathermap.org/data/2.5/weather"
    params = {
        "q": city,
        "appid": api_key
    }
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url, params=params)
        data = resp.json()
        return data  # You can later filter by trip dates
