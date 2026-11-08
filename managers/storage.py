import streamlit as st

def show_history_page():

    """Display previous weather searches and activity plans."""

    st.title("📋 Weather History")

    st.write(

        "View your previous weather searches "

        "and outdoor activity plans."

    )

    st.divider()

    try:

        storage = StorageManager()

        # SEARCH HISTORY

        st.subheader("🔍 Search History")

        searches = storage.get_search_history()

        if searches:

            for index, record in enumerate(searches):

                with st.expander(

                    f"📍 {record.get('location', 'Unknown location')} "

                    f"- {record.get('activity', 'Unknown activity')}"

                ):

                    st.write(

                        f"**Date:** {record.get('searched_at', 'Unknown')}"

                    )

                    st.write(f"**Activity:** {record.get('activity', 'N/A')}")

                    if record.get("details"):

                        st.json(record["details"])

            if st.button("🗑️ Clear Search History"):

                storage.clear_search_history()

                st.success("Search history cleared!")

                st.rerun()

        else:

            st.info("No previous weather searches found.")

        st.divider()

        # ACTIVITY PLANNING HISTORY

        st.subheader("🏃 Activity Planning History")

        plans = storage.get_activity_plans()

        if plans:

            for index, record in enumerate(plans):

                plan = record.get("plan", {})

                with st.expander(

                    f"Activity Plan {index + 1}"

                ):

                    st.write(

                        f"**Saved:** {record.get('saved_at', 'Unknown')}"

                    )

                    st.json(plan)

        else:

            st.info("No saved activity plans found.")

        st.divider()

        # FAVOURITE LOCATIONS

        st.subheader("⭐ Favourite Locations")

        favourites = storage.get_favourites()

        if favourites:

            for index, favourite in enumerate(favourites):

                location = favourite.get("location", "Unknown")

                col1, col2 = st.columns([3, 1])

                with col1:

                    st.write(f"📍 {location}")

                with col2:

                    if st.button(

                        "Remove",

                        key=f"remove_favourite_{index}"

                    ):

                        storage.remove_favourite(location)

                        st.success(f"{location} removed.")

                        st.rerun()

        else:

            st.info("No favourite locations saved yet.")

    except StorageError as error:

        st.error(f"Unable to load history: {error}")

    except Exception as error:

        st.error(f"An unexpected error occurred: {error}")

    st.divider()

    if st.button("🔄 Refresh History"):

        st.rerun()
