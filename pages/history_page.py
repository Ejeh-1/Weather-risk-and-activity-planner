import streamlit as st

def show_history_page():

    """Display previous weather searches and activity plans."""

    st.title("📋 Weather History")

    st.write(

        "View your previous weather searches "

        "and outdoor activity plans."

    )

    st.divider()

    st.subheader("🔍 Search History")

    st.info(

        "Your previous weather searches will appear here "

        "when history storage is connected."

    )

    st.divider()

    st.subheader("🏃 Activity Planning History")

    st.info(

        "Your saved outdoor activity plans will appear here "

        "when storage functionality is connected."

    )

    st.divider()

    st.subheader("⭐ Favourite Locations")

    st.info(

        "Your favourite locations will appear here "

        "when the storage system is connected."

    )

    st.divider()

    if st.button("🔄 Refresh History"):

        st.rerun()
