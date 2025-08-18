import streamlit as st
import datetime
import requests


# Point this to your FastAPI backend
BACKEND_URL = "http://127.0.0.1:8000/plan"

st.set_page_config(page_title="AI Travel Planner", page_icon="🌍", layout="centered")

st.title("🌍 AI Travel Planner")
st.write("Trouble planning your vacation? Our AI trip planner is here for you..!!!")


# User inputs
destination = st.text_input("Destination", "Singapore")
travel_date = st.date_input("Travel Date", value=datetime.date.today())
duration = st.number_input("Trip Duration (days)", 1, 30, 5)
budget = st.selectbox("Budget", ["low", "medium", "high"])
activities = st.text_area("Preferred Activities (optional)")


if st.button("✨ Generate Itinerary"):
    payload = {
        "destination": destination,
        "travel_date": travel_date.isoformat(),
        "duration": duration,
        "budget": budget,
    }
    if activities:
        payload["activities"] = activities

    try:
        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        print(payload["travel_date"])

        st.subheader("🗓️ Your Itinerary")
        # st.write(data["itinerary"])

        if "attractions" in data:
            st.subheader("📍 Attractions")
            st.write(data["attractions"])

        if "weather_summary" in data:
            st.subheader("🌦️ Weather Forecast (raw data)")
            # st.json(data["weather_summary"])

    except Exception as e:
        st.error(f"Error fetching itinerary: {e}")
