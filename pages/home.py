import streamlit as st
from pages.weather_page import show_weather_page
from pages.activity_page import show_activity_page
from pages.history_page import show_history_page
from datetime import date, timedelta

from services.location_service import LocationService

from services.weather_client import WeatherClient

from models import Forecast, Location

from analyzer import ActivityRiskAnalyzer

from recommender import RecommendationEngine

def show_home_page():

    """Display the home page of the application."""

    # Custom styling

    st.markdown("""

        <style>

        .main {

            background-color: #F0F7FA;

        }

        .hero {

            background: linear-gradient(135deg, #075985, #0EA5E9);

            padding: 35px;

            border-radius: 15px;

            color: white;

            text-align: center;

            margin-bottom: 25px;

        }

        .hero h1 {

            color: white;

            font-size: 32px;

        }

        .hero p {

            color: white;

            font-size: 16px;

        }

        .weather-card {

            background-color: #E0F2FE;

            padding: 20px;

            border-radius: 12px;

            text-align: center;

            margin-bottom: 15px;

        }

        </style>

    """, unsafe_allow_html=True)

    # Sidebar navigation

    st.sidebar.title("🌦️ WEATHER PLANNER")

    st.sidebar.write("Your outdoor safety companion")

    menu = st.sidebar.radio(

        "Navigation",

        [

            "Home",

            "Weather Forecast",

            "Activity Planner",

            "Weather History"

        ]

    )

    if menu == "Home":

        # Welcome section

        st.markdown("""

            <div class="hero">

                <h1>🌦️ Weather Risk & Outdoor Activity Planner</h1>

                <p>Make smarter decisions before stepping outdoors.</p>

            </div>

        """, unsafe_allow_html=True)

        st.subheader("Welcome!")

        st.write(

            "Check weather conditions, understand potential risks "

            "and plan your outdoor activities safely."

        )

        st.divider()

        # Weather information cards

        st.subheader("🌤️ Weather Planning")

        col1, col2, col3 = st.columns(3)

        with col1:

            st.markdown("""

                <div class="weather-card">

                    <h3>🌡️</h3>

                    <b>Temperature</b>

                    <p>Awaiting forecast</p>

                </div>

            """, unsafe_allow_html=True)

        with col2:

            st.markdown("""

                <div class="weather-card">

                    <h3>💧</h3>

                    <b>Humidity</b>

                    <p>Awaiting forecast</p>

                </div>

            """, unsafe_allow_html=True)

        with col3:

            st.markdown("""

                <div class="weather-card">

                    <h3>💨</h3>

                    <b>Wind Speed</b>

                    <p>Awaiting forecast</p>

                </div>

            """, unsafe_allow_html=True)

        st.divider()

        # Activity planning form

        st.subheader("📍 Plan Your Outdoor Activity")

        with st.form("activity_form"):

            location = st.text_input(

                "Enter your location:",

                placeholder="e.g. Lokoja, Nigeria"

            )

            activities = [
                "Select an activity",

                "Football",

                "Jogging",

                "Farming",

                "Picnic",

                "Travelling",

                "Outdoor events"

            ]

            activity = st.selectbox(

                "Select your outdoor activity:",

                activities,
                index = 0

            )

            submitted = st.form_submit_button(

                "🌦️ Check Weather Risk",

                use_container_width=True

            )

            if submitted:

                location = location.strip()

                if not location:

                    st.warning("Please enter your location.")

                elif activity == "Select an activity":

                    st.warning("Please select an outdoor activity.")

                else:

                    st.success(

                        f"Activity: {activity} | Location: {location}"

                    )

                    try:

    # 1. Find the location

    location_service = LocationService()

    locations = location_service.search_location(location)

    if not locations:

        st.error("Location not found. Please check the spelling.")

        return

    # Use the first matching location

    location_data = locations[0]

    selected_location = Location(

        name=location_data["name"],

        country=location_data.get("country") or "",

        latitude=location_data["latitude"],

        longitude=location_data["longitude"],

        timezone=location_data.get("timezone") or "auto"

    )

    # 2. Retrieve weather forecast

    weather_client = WeatherClient()

    weather_data = weather_client.get_weather(

        selected_location.latitude,

        selected_location.longitude

    )

    if not weather_data:

        st.error("Unable to retrieve weather data. Please try again.")

        return

    # 3. Process the forecast

    forecast = Forecast(weather_data, selected_location)

    # 4. Analyze weather risks

    activity_key = activity.lower().replace(" ", "_")

    analyzer = ActivityRiskAnalyzer(activity=activity_key)

    # 5. Generate activity recommendations

    engine = RecommendationEngine(analyzer)

    plan = engine.build_plan(

        forecast=forecast,

        day=forecast.local_now.date(),

        duration=2

    )

    # 6. Display results

    st.success("Weather assessment completed!")

    st.subheader("📍 Location")

    st.write(selected_location.label)

    st.subheader("🌤️ Current Weather")

    col1, col2, col3 = st.columns(3)

    with col1:

        st.metric("Temperature", f"{forecast.get_temperature()} °C")

    with col2:

        st.metric("Humidity", f"{forecast.get_humidity()}%")

    with col3:

        st.metric("Wind Speed", f"{forecast.get_wind_speed()} km/h")

    st.subheader("🛡️ Activity Risk Assessment")

    st.write(f"Activity: {activity}")

    st.write(f"Risk Rating: **{plan.rating.value}**")

    st.write(f"Recommended Time: **{plan.window.label}**")

    st.subheader("Why this rating?")

    for reason in plan.reasons:

        st.write(f"- {reason}")

    st.subheader("Safety Advice")

    for advice in plan.advice:

        st.write(f"- {advice}")

    st.subheader("Packing Checklist")

    for item in plan.checklist:

        st.write(f"- {item}")

except Exception as error:

    st.error(f"Unable to complete weather assessment: {error}")

    elif menu == "Weather Forecast":
        show_weather_page()

        

    elif menu == "Activity Planner":
        show_activity_page()

    elif menu == "Weather History":
        show_history_page()
        
