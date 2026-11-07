import streamlit as st

from datetime import date, time

from services.location_service import LocationService

from services.weather_client import WeatherClient

from models import Forecast, Location

from analyzer import ActivityRiskAnalyzer

from recommender import RecommendationEngine

from exceptions import InvalidInputError, WeatherDataError

def show_activity_page():

    """Display the outdoor activity planning page."""

    st.title("🏃 Activity Planner")

    st.write(

        "Plan your outdoor activities by selecting "

        "your preferred location, date and time."

    )

    st.divider()

    st.subheader("📋 Create Your Activity Plan")

    activities = [

        "Football",

        "Jogging",

        "Farming",

        "Picnic",

        "Travelling",

        "Outdoor events"

    ]

    with st.form("activity_planning_form"):

        location_input = st.text_input(

            "📍 Enter your location:",

            placeholder="e.g. Lokoja, Nigeria"

        )

        activity = st.selectbox(

            "🏃 Select your activity:",

            activities

        )

        activity_date = st.date_input(

            "📅 Select activity date:",

            min_value=date.today()

        )

        activity_time = st.time_input(

            "⏰ Select preferred time:",

            value=time(9, 0)

        )

        notes = st.text_area(

            "📝 Additional notes (optional):",

            placeholder="Add any extra information about your activity."

        )

        submitted = st.form_submit_button(

            "Create Activity Plan",

            use_container_width=True

        )

    if submitted:

        if not location_input.strip():

            st.warning("Please enter your location.")

        else:

            with st.spinner("Retrieving weather forecast and assessing risks..."):

                try:

                    location_service = LocationService()

                    locations = location_service.search_location(

                        location_input.strip()

                    )

                    if not locations:

                        st.error("Location not found. Please try another location.")

                    else:

                        location_data = locations[0]

                        selected_location = Location(

                            name=location_data["name"],

                            country=location_data.get("country") or "",

                            latitude=location_data["latitude"],

                            longitude=location_data["longitude"],

                            timezone=location_data.get("timezone") or "UTC"

                        )

                        weather_client = WeatherClient()

                        weather_data = weather_client.get_weather(

                            selected_location.latitude,

                            selected_location.longitude

                        )

                        if not weather_data:

                            st.error("Unable to retrieve weather data. Please try again.")

                        else:

                            forecast = Forecast(

                                weather_data,

                                location=selected_location

                            )

                            analyzer = ActivityRiskAnalyzer(activity)

                            recommendation_engine = RecommendationEngine(

                                analyzer

                            )

                            plan = recommendation_engine.build_plan(

                                forecast=forecast,

                                day=activity_date,

                                duration=2,

                                start=activity_time

                            )

                            st.success("Your activity plan has been created!")

                            st.divider()

                            st.subheader("📌 Activity Risk Assessment")

                            st.write(plan.to_text())

                            st.divider()

                            st.subheader("⏰ Hourly Weather Risk Assessment")

                            st.code(plan.hourly_table())

                            if notes.strip():

                                st.write("**Additional notes:**")

                                st.write(notes)

                except (InvalidInputError, WeatherDataError, ValueError) as error:

                    st.warning(str(error))

                except Exception as error:

                    st.error(

                        f"An unexpected error occurred: {error}"

                    )
        
