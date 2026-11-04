import streamlit as st

def show_home_page():

    """Display the home page of the Weather Risk & Outdoor Activity Planner."""

    st.title("🌦️ Weather Risk & Outdoor Activity Planner")

    st.write(

        "Welcome! Plan your outdoor activities safely "

        "with weather forecasts and risk assessments."

    )

    st.subheader("Plan Your Outdoor Activity")

    # Location input

    location = st.text_input("Enter your location:")

    # Activity selection

    activities = [

        "Football",

        "Jogging",

        "Farming",

        "Picnic",

        "Travelling",

        "Outdoor events"

    ]

    activity = st.selectbox(

        "Select your outdoor activity:",

        activities

    )

    # Planning button

    if st.button("Check Weather Risk"):

        if not location.strip():

            st.warning("Please enter your location.")

        else:

            st.success(

                f"Your activity is {activity} in {location}."

            )

            st.info("Weather assessment will be available soon.")
