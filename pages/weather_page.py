import streamlit as st

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

            if not location.strip():

                st.warning("Please enter a location.")

            else:

                st.success(

                    f"Searching weather information for {location}."

                )

                st.info(

                    "Weather forecast data will appear here "

                    "after connecting the Open-Meteo API."

                )

    st.divider()

    st.subheader("🌦️ Weather Information")

    col1, col2 = st.columns(2)

    with col1:

        st.metric(

            label="Temperature",

            value="-- °C"

        )

        st.metric(

            label="Humidity",

            value="-- %"

        )

    with col2:

        st.metric(

            label="Wind Speed",

            value="-- km/h"

        )

        st.metric(

            label="Rain Probability",

            value="-- %"

        )

    st.divider()

    st.subheader("📅 Weather Forecast")

    st.info(

        "Your upcoming weather forecast will appear here."
