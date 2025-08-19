from fastapi import FastAPI
from pydantic import BaseModel
import os

from openai import OpenAI

from .config import OPENAI_API_KEY, GOOGLE_API_KEY, WEATHER_API_KEY
from .api_clients import get_attractions, get_weather_forecast


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY not found in environment variables")


# Initialize OpenAI client
client = OpenAI(api_key=OPENAI_API_KEY)

# FastAPI app
app = FastAPI(title="AI Travel Planner")

# Request model
class TripRequest(BaseModel):
    destination: str
    duration: int
    budget: str


# POST endpoint
@app.post("/plan")
async def generate_plan(request: TripRequest):
    attractions = await get_attractions(request.destination, GOOGLE_API_KEY)
    weather = await get_weather_forecast(request.destination, WEATHER_API_KEY)

    # print(f"Attractions in {request.destination}: {attractions}")
    # prompt = (
    #     f"Create a short travel plan for {request.duration} days in {request.destination} "
    #     f"with a {request.budget} budget. Include popular spots."
    # )

    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.7
    # )

    return {"attractions": attractions, "weather": weather}
