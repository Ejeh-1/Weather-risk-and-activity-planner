import streamlit as st

from datetime import date, time

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

        location = st.text_input(

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

            if not location.strip():

                st.warning("Please enter your location.")

            else:

                st.success("Your activity plan has been created!")

                st.write("### 📌 Activity Details")

                st.write(f"**Location:** {location}")

                st.write(f"**Activity:** {activity}")

                st.write(f"**Date:** {activity_date}")

                st.write(f"**Time:** {activity_time}")

                if notes.strip():

                    st.write(f"**Notes:** {notes}")

                st.info(

                    "Weather risk assessment will be connected "

                    "to this activity planner soon."

                )
