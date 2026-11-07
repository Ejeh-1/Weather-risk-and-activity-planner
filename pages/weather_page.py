import streamlit as st

from services.location_service import LocationService

from services.weather_client import WeatherClient

from models.forecast import Forecast

def show_weather_page():

    """Display the weather forecast page."""

    st.title("🌤️ Weather Forecast")

    st.write(

        "Check current weather conditions and forecasts "

        "for your selected location."

    )

    st.divider()

    st.subheader("📍 Search Weather")

    with st.form("weather_search_form"):

        location = st.text_input(

            "Enter your location:",

            placeholder="e.g. Lokoja, Nigeria"

        )

        submitted = st.form_submit_button(

            "Search Weather",

            use_container_width=True

        )

    if submitted:

        location = location.strip()

        if not location:

            st.warning("Please enter a location.")

        else:

            with st.spinner("Searching for location..."):

                location_service = LocationService()

                locations = location_service.search_location(location)

            if not locations:

                st.error("Location not found. Please try another city.")

            else:

                selected_location = locations[0]

                latitude = selected_location["latitude"]

                longitude = selected_location["longitude"]

                city = selected_location["name"]

                country = selected_location.get("country", "")

                st.success(f"Location found: {city}, {country}")

                with st.spinner("Fetching weather information..."):

                    weather_client = WeatherClient()

                    weather_data = weather_client.get_weather(

                        latitude,

                        longitude

                    )

                if not weather_data:

                    st.error(

                        "Unable to retrieve weather information. "

                        "Please try again."

                    )

                else:

                    forecast = Forecast(weather_data)

                    weather = forecast.to_dict()

                    st.divider()

                    st.subheader("🌡️ Current Weather Information")

                    col1, col2 = st.columns(2)

                    temperature = weather["temperature"]

                    humidity = weather["humidity"]

                    wind_speed = weather["wind_speed"]

                    rain_probability = weather["rain_probability"]

                    with col1:

                        st.metric(

                            "Temperature",

                            f"{temperature} °C"

                            if temperature is not None else "--"

                        )

                        st.metric(

                            "Humidity",

                            f"{humidity}%"

                            if humidity is not None else "--"

                        )

                    with col2:

                        st.metric(

                            "Wind Speed",

                            f"{wind_speed} km/h"

                            if wind_speed is not None else "--"

                        )

                        st.metric(

                            "Rain Probability",

                            f"{rain_probability}%"

                            if rain_probability is not None else "--"

                        )

                    st.divider()

                    st.subheader("🌦️ Upcoming Weather Forecast")

                    hourly = forecast.get_hourly_forecast()

                    times = hourly.get("time", [])

                    probabilities = hourly.get(

                        "precipitation_probability", []

                    )

                    if times and probabilities:

                        st.dataframe(

                            {

                                "Time": times[:24],

                                "Rain Probability (%)": probabilities[:24]

                            },

                            use_container_width=True

                        )

                    else:

                        st.info(

                            "Hourly forecast information is unavailable."

                        )
