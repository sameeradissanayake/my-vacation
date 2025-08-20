from fastapi import FastAPI
from pydantic import BaseModel
import os
import certifi

from openai import OpenAI

from .config import OPENAI_API_KEY, GOOGLE_API_KEY, WEATHER_API_KEY, AI_MODEL
from .api_clients import get_attractions, get_weather_forecast


if not OPENAI_API_KEY:
    raise ValueError("OPENAI_API_KEY not found in environment variables")

if not GOOGLE_API_KEY:
    raise ValueError("GOOGLE_API_KEY not found in environment variables")

if not WEATHER_API_KEY:
    raise ValueError("WEATHER_API_KEY not found in environment variables")

os.environ["SSL_CERT_FILE"] = certifi.where()

# Initialize OpenAI client
client = OpenAI(base_url="https://models.github.ai/inference", api_key = OPENAI_API_KEY)

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

    prompt = (
        f"Create a short travel plan for {request.duration} days in {request.destination} "
        f"with a {request.budget} budget."
        f"Include popular spots like {attractions} based on time availability."
    )

    response = client.chat.completions.create(
    messages=[{"role": "user", "content": prompt}],
    temperature=1,
    top_p=1,
    model=AI_MODEL
)

    return {"itinerary": response.choices[0].message.content, "attractions": attractions, "weather": weather}
