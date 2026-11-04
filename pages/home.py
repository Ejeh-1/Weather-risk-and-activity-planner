import streamlit as st

def show_home_page():

    """Display the home page of the application."""

    # Sidebar navigation

    st.sidebar.title("🌦️ WEATHER PLANNER")

    menu = st.sidebar.radio(

        "Navigation",

        [

            "Home",

            "Weather Forecast",

            "Activity Planner",

            "Weather History"

        ]

    )

    # Home page

    if menu == "Home":

        st.title("🌦️ Weather Risk & Outdoor Activity Planner")

        st.write(

            "Welcome! Plan your outdoor activities safely "

            "with weather forecasts and risk assessments."

        )

        st.divider()

        st.subheader("📍 Plan Your Outdoor Activity")

        with st.form("activity_form"):

            location = st.text_input(

                "Enter your location:"

            )

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

            submitted = st.form_submit_button(

                "Check Weather Risk"

            )

            if submitted:

                if not location.strip():

                    st.warning("Please enter your location.")

                else:

                    st.success(

                        f"Activity: {activity}\n\n"

                        f"Location: {location}"

                    )

                    st.info(

                        "Weather assessment will be available soon."

                    )

    elif menu == "Weather Forecast":

        st.title("🌤️ Weather Forecast")

        st.info("Weather forecast feature coming soon.")

    elif menu == "Activity Planner":

        st.title("🏃 Activity Planner")

        st.info("Activity planning feature coming soon.")

    elif menu == "Weather History":

        st.title("📋 Weather History")

        st.info("Weather history feature coming soon.")
