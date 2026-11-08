import streamlit as st
from managers.storage import StorageManager, StorageError 

from services.location_service import LocationService

from services.weather_client import WeatherClient

from models import Forecast, Location

from analyzer import ActivityRiskAnalyzer

from recommender import RecommendationEngine

from pages.weather_page import show_weather_page

from pages.activity_page import show_activity_page

from pages.history_page import show_history_page

def show_home_page():

    st.title("🌦️ Weather Risk & Activity Planner")

    st.write("Plan your outdoor activities safely.")

    menu = st.sidebar.radio(

        "Navigation",

        ["Home", "Weather Forecast", "Activity Planner", "Weather History"]

    )

    if menu == "Weather Forecast":

        show_weather_page()

        return

    if menu == "Activity Planner":

        show_activity_page()

        return

    if menu == "Weather History":

        show_history_page()

        return

    st.subheader("Check Your Weather Risk")

    location = st.text_input("Enter your location")

    activity = st.selectbox(

        "Select an activity",

        ["Select an activity", "Football", "Jogging",

         "Farming", "Picnic", "Travelling", "Outdoor events"]

    )

    if st.button("Check Weather Risk"):

        if not location.strip():

            st.warning("Please enter your location.")

            return

        if activity == "Select an activity":

            st.warning("Please select an activity.")

            return

        try:

            location_service = LocationService()

            results = location_service.search_location(location)

            if not results:

                st.error("Location not found.")

                return

            data = results[0]

            selected_location = Location(

                name=data["name"],

                country=data.get("country") or "",

                latitude=data["latitude"],

                longitude=data["longitude"],

                timezone=data.get("timezone") or "auto"

            )

            weather_client = WeatherClient()

            weather_data = weather_client.get_weather(

                selected_location.latitude,

                selected_location.longitude

            )

            if not weather_data:

                st.error("Unable to retrieve weather data.")

                return

            forecast = Forecast(weather_data, selected_location)

            analyzer = ActivityRiskAnalyzer(

                activity=activity.lower().replace(" ", "_")

            )

            engine = RecommendationEngine(analyzer)

            plan = engine.build_plan(

                forecast,

                forecast.local_now.date(),

                duration=2

            )
            try:
                storage = StorageManager()
                storage.save_search(
                    storage = selected_location.label,
                    activity = activity,
                    search_data = {
                        "temperature": forecast.get_temperature(),
                        "humidity": forecast.get_humidity(),
                        "wind_speed": forecast.get_wind_speed(),
                        "risk_rating": plan.rating.value,
                        "recommended_time": plan.window.label
                    }
                )
                storage.save_activity_plan(plan)
            except (StorageError, ValueError) as error:
                st.warning(f"Unable to save history: {error}")
                
                
                        
                    
                

            st.success("Weather assessment completed!")

            st.write("Location:", selected_location.label)

            st.subheader("Current Weather")

            col1, col2, col3 = st.columns(3)

            col1.metric("Temperature", f"{forecast.get_temperature()} °C")

            col2.metric("Humidity", f"{forecast.get_humidity()}%")

            col3.metric("Wind Speed", f"{forecast.get_wind_speed()} km/h")

            st.subheader("Risk Assessment")

            st.write("Activity:", activity)

            st.write("Risk Rating:", plan.rating.value)

            st.write("Recommended Time:", plan.window.label)

            st.subheader("Reasons")

            for reason in plan.reasons:

                st.write("-", reason)

            st.subheader("Safety Advice")

            for advice in plan.advice:

                st.write("-", advice)

            st.subheader("Packing Checklist")

            for item in plan.checklist:

                st.write("-", item)

        except Exception as error:

            st.error(f"Weather assessment failed: {error}")
