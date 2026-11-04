import streamlit as st

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

                "🌦️ Check Weather Risk",

                use_container_width=True

            )

            if submitted:

                if not location.strip():

                    st.warning("Please enter your location.")

                else:

                    st.success(

                        f"Activity: {activity} | Location: {location}"

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
