import streamlit as st

from location_service import LocationService

def show_location_page():

    """Display the location search page."""

    st.title("📍 Location Search")

    st.write(

        "Search for a city and retrieve its geographical coordinates."

    )

    st.divider()

    st.subheader("Search for a Location")

    city_name = st.text_input("Enter your city")

    country_code = st.text_input(

        "Enter country code (optional, e.g. NG, GB, US)"

    )

    if st.button("Search Location"):

        if city_name.strip():

            location_service = LocationService()

            locations = location_service.search_location(

                city_name, country_code or None

            )

            if locations:

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
