import streamlit as st

from pages.home import show_home_page

def main():

    st.set_page_config(

        page_title="Weather Risk & Outdoor Activity Planner",

        page_icon="🌦️",

        layout="wide"

    )

    show_home_page()

if __name__ == "__main__":

    main()
