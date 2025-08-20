import streamlit as st
import datetime
import requests

import pandas as pd


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

        st.write("")
        st.subheader("🗓️ Your Itinerary")
        st.write(data["itinerary"])

        if "attractions" in data:
            st.write("")
            st.subheader(f"📍 Popular Attractions in {destination}")
            count = len(data["attractions"])
            
            attraction_list = ""
            for i in data["attractions"]:
                attraction_list += f"- {i['name']}\n"

            st.markdown(attraction_list)

        if "weather" in data:
            st.write("")
            st.subheader(f"🌦️ Weather Forecast for Next Several Days in {destination}")

            dates_list = []
            temperature_list = []
            humidity_list = []
            feels_like_list = []
            description_list = []

            for date in data["weather"]:
                dates_list.append(date)

                temp_k = data["weather"][date]["temp"]
                formatted_temp_c = "{:.2f}".format(temp_k - 273.15)
                temperature_list.append(formatted_temp_c)

                humidity_list.append(data["weather"][date]["humidity"])
                
                feels_k = data["weather"][date]["feels_like"]
                formatted_feel_c = "{:.2f}".format(feels_k - 273.15)
                feels_like_list.append(formatted_feel_c)

                description_list.append(data["weather"][date]["description"])

            weather_summary = {'Date': dates_list,
                               'Temperature': temperature_list,
                               'Humidity': humidity_list,
                               'Feels Like': feels_like_list,
                               'Description': description_list}
            
            weather_df = pd.DataFrame(weather_summary)

            st.table(weather_df)

    except Exception as e:
        placeholder.empty()
        st.write("Sorry our planner is not available at the moment!! 😞")
        # st.error(f"Error fetching itinerary: {e}")
