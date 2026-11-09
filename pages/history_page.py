import streamlit as st

from managers.storage import StorageManager, StorageError

def show_history_page():

    st.title("📋 Weather History")

    st.write("View your previous weather searches and activity plans.")

    storage = StorageManager()

    try:

        # ==========================

        # SEARCH HISTORY

        # ==========================

        st.divider()

        st.subheader("🔍 Search History")

        searches = storage.get_search_history()

        if searches:

            for index, search in enumerate(searches):

                details = search.get("details", {})

                with st.expander(

                    f"📍 {search.get('location', 'Unknown')} "

                    f"— {search.get('activity', 'Unknown')}"

                ):

                    st.caption(

                        f"Searched at: {search.get('searched_at', 'Unknown')}"

                    )

                    col1, col2, col3 = st.columns(3)

                    col1.metric(

                        "Temperature",

                        f"{details.get('temperature', 'N/A')} °C"

                    )

                    col2.metric(

                        "Humidity",

                        f"{details.get('humidity', 'N/A')}%"

                    )

                    col3.metric(

                        "Wind Speed",

                        f"{details.get('wind_speed', 'N/A')} km/h"

                    )

                    st.write(

                        "Risk Rating:",

                        details.get("risk_rating", "N/A")

                    )

                    st.write(

                        "Recommended Time:",

                        details.get("recommended_time", "N/A")

                    )

        else:

            st.info("No previous weather searches found.")

        if searches and st.button("🗑️ Clear Search History"):

            storage.clear_search_history()

            st.success("Search history cleared!")

            st.rerun()

        # ==========================

        # ACTIVITY PLANNING HISTORY

        # ==========================

        st.divider()

        st.subheader("🏃 Activity Planning History")

        plans = storage.get_activity_plans()

        if plans:

            for index, record in enumerate(plans):

                plan = record.get("plan", {})

                location = plan.get("location", {})

                with st.expander(

                    f"🏃 {plan.get('activity_name', 'Outdoor Activity')} "

                    f"— {location.get('name', 'Unknown Location')}"

                ):

                    st.caption(

                        f"Saved at: {record.get('saved_at', 'Unknown')}"

                    )

                    st.write(

                        "**Location:**",

                        location.get("name", "Unknown"),

                        location.get("country", "")

                    )

                    st.write("**Date:**", plan.get("day", "N/A"))

                    st.write(

                        "**Duration:**",

                        f"{plan.get('duration', 'N/A')} hours"

                    )

                    window = plan.get("window", {})

                    if isinstance(window, dict):

                        assessments = window.get("assessments", [])

                        if assessments:

                            st.write("**Recommended Time:**")

                            for assessment in assessments:

                                hour = assessment.get("hour", {})

                                time_value = hour.get("time", "N/A")

                                if time_value != "N/A":

                                    st.write(f"• {time_value}")

                        st.write(

                            "**Risk Score:**",

                            window.get("score", "N/A")

                        )

                    # Safety Advice

                    st.write("### 🛡️ Safety Advice")

                    advice = plan.get("advice", [])

                    if advice:

                        for item in advice:

                            st.write(f"• {item}")

                    else:

                        st.info("No safety advice available.")

                    # Packing Checklist

                    st.write("### 🎒 Packing Checklist")

                    checklist = plan.get("checklist", [])

                    if checklist:

                        for item in checklist:

                            st.write(f"☐ {item}")

                    else:

                        st.info("No packing checklist available.")

       
            if st.button("🗑️ Clear Activity Planning History"):
                storage.clear_activity_plans()
                st.success("Activity planning history cleared!")
                st.rerun()
        
        else:

            st.info("No saved activity plans found.")

        # ==========================

        # FAVOURITE LOCATIONS

        # ==========================

        st.divider()

        st.subheader("✨ Favourite Locations")

        favourites = storage.get_favourites()

        if favourites:

            for index, favourite in enumerate(favourites):

                if isinstance(favourite, dict):

                    location_name = favourite.get("location", str(favourite))

                else:

                    location_name = favourite

                col1, col2 = st.columns([4, 1])

                with col1:

                    st.write(f"📍 {location_name}")

                with col2:

                    if st.button("Remove", key=f"remove_{index}"):

                        storage.remove_favourite(location_name)

                        st.success("Favourite removed!")

                        st.rerun()

        else:

            st.info("No favourite locations saved yet.")

        # ==========================

        # REFRESH

        # ==========================

        st.divider()

        if st.button("🔄 Refresh History"):
            st.success("History refresh successfully✅")

            st.rerun()

    except StorageError as error:

        st.error(f"Storage error: {error}")

    except Exception as error:

        st.error(f"Something went wrong: {error}")

        
