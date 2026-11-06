import streamlit as st
from services.location_service import LocationService

def main():
    location_service = LocationService()

    st.set_page_config(

        page_title="Weather Risk & Outdoor Activity Planner",

        page_icon="🌦️",

        layout="wide"

    )

    st.title("🌦️ Weather Risk & Outdoor Activity Planner")

    st.write(

        "Welcome! Plan your outdoor activities safely "

        "with weather forecasts and risk assessments."

    )

    st.subheader("📍 Search for a Location")

    city_name = st.text_input("Enter your city")

    country_code = st.text_input(

        "Enter country code (optional, e.g. NG, GB, US)"

    )

    if st.button("Search Location"):

        if city_name.strip():

            locations = location_service.search_location(

                city_name, country_code or None

            )

            if locations:

                st.success("Location search successful!")

                for location in locations:

                    st.write(f"**City:** {location['name']}")

                    st.write(f"**Country:** {location['country']}")

                    st.write(f"**Latitude:** {location['latitude']}")

                    st.write(f"**Longitude:** {location['longitude']}")

                    st.write(f"**Timezone:** {location['timezone']}")

                    st.divider()

            else:

                st.warning("No location found. Please try again.")

        else:

            st.warning("Please enter a city name.")

if __name__ == "__main__":

    main()
