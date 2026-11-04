import streamlit as st

def main():

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

    st.info("Our weather planning system is coming soon!")

if __name__ == "__main__":

    main()
