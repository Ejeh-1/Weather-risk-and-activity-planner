"""
activity_risk_analyzer.py
Module: AI Risk Analysis
Project: Weather Risk & Outdoor Activity Planner

What this module does:
1. Takes weather data (temperature, humidity, rain chance, wind speed)
2. Compares it with the limits of the chosen activity
3. Gives a risk level: Safe, Manageable, Risky or Should Be Avoided
4. Asks the Gemini API to explain the result in simple words
"""

import os
import requests

# Optional: load the API key from a .env file (pip install python-dotenv)
try:
    from dotenv import load_dotenv
    load_dotenv()
except ImportError:
    pass  # if dotenv is not installed we just use normal environment variables


# ---------------------------------------------------------------
# LIMITS FOR EACH ACTIVITY
# If the weather goes past a limit, the activity gets risk points.
#   max_temp  = too hot above this (degrees C)
#   min_temp  = too cold below this (degrees C)
#   max_rain  = rain probability above this is a problem (%)
#   max_wind  = wind speed above this is a problem (km/h)
#   max_humidity = humidity above this is a problem (%)
# ---------------------------------------------------------------
ACTIVITY_LIMITS = {
    "football":  {"max_temp": 32, "min_temp": 10, "max_rain": 40, "max_wind": 30, "max_humidity": 85},
    "jogging":   {"max_temp": 30, "min_temp": 5,  "max_rain": 50, "max_wind": 35, "max_humidity": 80},
    "farming":   {"max_temp": 35, "min_temp": 10, "max_rain": 60, "max_wind": 40, "max_humidity": 90},
    "picnic":    {"max_temp": 33, "min_temp": 15, "max_rain": 20, "max_wind": 25, "max_humidity": 85},
    "travelling": {"max_temp": 38, "min_temp": 0,  "max_rain": 60, "max_wind": 50, "max_humidity": 95},
    "outdoor events": {"max_temp": 34, "min_temp": 12, "max_rain": 30, "max_wind": 30, "max_humidity": 85},
}

# Gemini settings
GEMINI_MODEL = "gemini-2.5-flash"
GEMINI_URL = "https://generativelanguage.googleapis.com/v1beta/models/" + GEMINI_MODEL + ":generateContent"


class ActivityRiskAnalyzer:
    """Checks how risky an outdoor activity is for given weather."""

    def __init__(self, api_key=None):
        # Use the key we are given, otherwise look for GEMINI_API_KEY
        if api_key:
            self.api_key = api_key
        else:
            self.api_key = os.getenv("GEMINI_API_KEY")

    # -----------------------------------------------------------
  