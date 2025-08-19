import httpx
import os
import asyncio



async def get_attractions(destination: str, api_key: str):
    url = "https://places.googleapis.com/v1/places:searchText"
    headers = {
        "Content-Type": "application/json",
        "X-Goog-Api-Key": api_key,
        "X-Goog-FieldMask": "places.displayName,places.formattedAddress,places.priceLevel"
    }
    payload = {
        "textQuery": f"Give me popular attractions in {destination}"
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
    url = "https://api.openweathermap.org/data/2.5/forecast?"
    params = {
        "q": city,
        "appid": api_key
    }
    async with httpx.AsyncClient(verify=False) as client:
        resp = await client.get(url, params=params)
        data = resp.json()

        daily_forecast = {}

        for entry in data["list"]:
            date = entry["dt_txt"].split(" ")[0]  # extract date (YYYY-MM-DD)
            time = entry["dt_txt"].split(" ")[1]  # extract time (HH:MM:SS)
            
            if time == "12:00:00":  # pick the forecast for 12:00 each day
                daily_forecast[date] = {
                    "temp": entry["main"]["temp"],
                    "humidity": entry["main"]["humidity"],
                    "feels_like": entry["main"]["feels_like"],
                    "description": entry["weather"][0]["description"]
                }
        return daily_forecast  # You can later filter by trip dates
