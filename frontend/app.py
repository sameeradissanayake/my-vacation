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
        placeholder = st.empty()
        with placeholder.container():
            col = st.columns([1])[0]  # single column
            with col:
                row1, row2 = st.columns([4, 1])  # text bigger, GIF smaller
                with row1:
                    st.markdown(
                        "<p style='font-size:20px; margin:0;'>⏳ Sending request... please wait</p>", 
                        unsafe_allow_html=True
                    )
                with row2:
                    st.image("https://i.gifer.com/ZZ5H.gif", width=30)


        response = requests.post(BACKEND_URL, json=payload)
        response.raise_for_status()
        data = response.json()

        placeholder.empty()

        st.subheader("🗓️ Your Itinerary")
        st.write(data["itinerary"])

        if "attractions" in data:
            st.subheader(f"📍 Popular Attractions in {destination}")
            count = len(data["attractions"])
            
            attraction_list = ""
            for i in data["attractions"]:
                attraction_list += f"- {i['name']}\n"

            st.markdown(attraction_list)

        # if "weather_summary" in data:
        #     st.subheader("🌦️ Weather Forecast (raw data)")
        #     # st.json(data["weather_summary"])

    except Exception as e:
        placeholder.empty()
        st.write("Sorry our planner is not available at the moment!! 😞")
        # st.error(f"Error fetching itinerary: {e}")
