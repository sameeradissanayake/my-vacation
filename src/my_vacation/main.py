from fastapi import FastAPI
from pydantic import BaseModel
import os
from dotenv import load_dotenv
from openai import OpenAI

from .api_clients import get_attractions, get_weather_forecast

# Load .env
load_dotenv()

# Get API key
api_key = os.getenv("OPENAI_API_KEY")

if not api_key:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

# Initialize OpenAI client
client = OpenAI(api_key=api_key)

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
    attractions = await get_attractions(request.destination)

    print(f"Attractions in {request.destination}: {attractions}")
    # prompt = (
    #     f"Create a short travel plan for {request.duration} days in {request.destination} "
    #     f"with a {request.budget} budget. Include popular spots."
    # )

    # response = client.chat.completions.create(
    #     model="gpt-4o-mini",
    #     messages=[{"role": "user", "content": prompt}],
    #     temperature=0.7
    # )

    return {"attractions": attractions}
