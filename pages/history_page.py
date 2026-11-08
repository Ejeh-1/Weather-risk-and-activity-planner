import streamlit as st

from managers.storage import StorageManager, StorageError

def show_history_page():

    st.title("📋 Weather History")

    st.write(

        "View your previous weather searches "

        "and outdoor activity plans."

    )

    storage = StorageManager()

    try:

        # Search History

        st.divider()

        st.subheader("🔍 Search History")

        searches = storage.get_search_history()

        if searches:

            for search in searches:

                st.write(search)

        else:

            st.info("No previous weather searches found.")

        if st.button("🗑️ Clear Search History"):

            storage.clear_search_history()

            st.success("Search history cleared!")

            st.rerun()

        # Activity Plans

        st.divider()

        st.subheader("🏃 Activity Planning History")

        plans = storage.get_activity_plans()

        if plans:

            for plan in plans:

                st.write(plan)

        else:

            st.info("No saved activity plans found.")

        # Favourite Locations

        st.divider()

        st.subheader("⭐ Favourite Locations")

        favourites = storage.get_favourites()

        if favourites:

            for favourite in favourites:

                st.write(favourite)

            location_to_remove = st.selectbox(

                "Select a favourite to remove",

                favourites

            )

            if st.button("Remove Favourite"):

                storage.remove_favourite(location_to_remove)

                st.success("Favourite removed!")

                st.rerun()

        else:

            st.info("No favourite locations saved.")

        if st.button("🔄 Refresh History"):

            st.rerun()

    except StorageError as error:

        st.error(f"Storage error: {error}")

    except Exception as error:

        st.error(f"Something went wrong: {error}")
