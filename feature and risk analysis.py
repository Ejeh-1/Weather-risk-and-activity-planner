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
    # Step 1: calculate risk points
    # -----------------------------------------------------------
    def calculate_risk_points(self, activity, weather):
        """
        activity: name of the activity, e.g. "football"
        weather: dictionary like
            {"temperature": 30, "humidity": 70, "rain_probability": 20, "wind_speed": 15}
        Returns: (total_points, list_of_reasons)
        """
        # Make the activity name lowercase so "Football" and "football" both work
        activity = activity.strip().lower()

        if activity not in ACTIVITY_LIMITS:
            raise ValueError("Unknown activity: " + activity)

        limits = ACTIVITY_LIMITS[activity]
        points = 0
        reasons = []  # will hold the problems we find

        temp = weather["temperature"]
        humidity = weather["humidity"]
        rain = weather["rain_probability"]
        wind = weather["wind_speed"]

        # --- Temperature too hot ---
        if temp > limits["max_temp"]:
            points += 1
            reasons.append("It is hot (" + str(temp) + "°C)")
            if temp > limits["max_temp"] + 5:  # way too hot
                points += 1
                reasons.append("The heat is extreme")

        # --- Temperature too cold ---
        if temp < limits["min_temp"]:
            points += 1
            reasons.append("It is cold (" + str(temp) + "°C)")
            if temp < limits["min_temp"] - 5:  # way too cold
                points += 1
                reasons.append("The cold is extreme")

        # --- Rain ---
        if rain > limits["max_rain"]:
            points += 1
            reasons.append("High chance of rain (" + str(rain) + "%)")
            if rain > 80:  # almost sure to rain
                points += 1
                reasons.append("Rain is almost certain")

        # --- Wind ---
        if wind > limits["max_wind"]:
            points += 1
            reasons.append("Strong wind (" + str(wind) + " km/h)")
            if wind > limits["max_wind"] + 20:  # very strong wind
                points += 1
                reasons.append("The wind is dangerously strong")

        # --- Humidity ---
        if humidity > limits["max_humidity"]:
            points += 1
            reasons.append("Very high humidity (" + str(humidity) + "%)")

        return points, reasons

    # -----------------------------------------------------------
    # Step 2: turn points into a risk level
    # -----------------------------------------------------------
    def get_risk_level(self, points):
        """Convert risk points into one of the four risk levels."""
        if points <= 1:
            return "Safe"
        elif points <= 3:
            return "Manageable"
        elif points <= 5:
            return "Risky"
        else:
            return "Should Be Avoided"

    # -----------------------------------------------------------
    # Step 3: ask Gemini to explain
    # -----------------------------------------------------------
    def get_ai_explanation(self, activity, weather, risk_level, reasons):
        """
        Sends the result to the Gemini API and returns a short explanation.
        If anything goes wrong we return a simple backup message
        so the app does not crash.
        """
        # Backup explanation (used when AI is not available)
        if len(reasons) > 0:
            backup = "Risk level is " + risk_level + ". Problems: " + ", ".join(reasons) + "."
        else:
            backup = "Risk level is " + risk_level + ". The weather looks good for " + activity + "."

        # No key = no AI
        if not self.api_key:
            return backup + " (AI explanation unavailable: no API key found.)"

        # Write the question (prompt) for Gemini
        prompt = (
            "You are a weather safety assistant. "
            "Activity: " + activity + ". "
            "Weather: temperature " + str(weather["temperature"]) + "°C, "
            "humidity " + str(weather["humidity"]) + "%, "
            "rain chance " + str(weather["rain_probability"]) + "%, "
            "wind speed " + str(weather["wind_speed"]) + " km/h. "
            "Risk level: " + risk_level + ". "
            "In 3 or 4 simple sentences, explain why this activity has this risk level "
            "and what the person should be careful about."
        )

        # The data format Gemini expects
        body = {"contents": [{"parts": [{"text": prompt}]}]}
        headers = {
            "Content-Type": "application/json",
            "x-goog-api-key": self.api_key,
        }

        try:
            response = requests.post(GEMINI_URL, headers=headers, json=body, timeout=15)
            response.raise_for_status()  # raises an error for bad status codes
            data = response.json()
            text = data["candidates"][0]["content"]["parts"][0]["text"]
            return text.strip()

        except requests.exceptions.Timeout:
            return backup + " (AI explanation timed out.)"
        except requests.exceptions.ConnectionError:
            return backup + " (No internet connection for AI explanation.)"
        except requests.exceptions.HTTPError as error:
            return backup + " (AI service error: " + str(error) + ")"
        except (KeyError, IndexError, ValueError):
            return backup + " (Could not read the AI response.)"

    # -----------------------------------------------------------
    # Main method: this is what the group leader will call
    # -----------------------------------------------------------
    def analyze(self, activity, weather, use_ai=True):
        """
        Full analysis. Returns a dictionary:
        {
            "activity": ...,
            "risk_level": ...,
            "risk_points": ...,
            "reasons": [...],
            "explanation": ...
        }
        """
        points, reasons = self.calculate_risk_points(activity, weather)
        level = self.get_risk_level(points)

        if use_ai:
            explanation = self.get_ai_explanation(activity, weather, level, reasons)
        else:
            explanation = "Risk level is " + level + "."

        return {
            "activity": activity,
            "risk_level": level,
            "risk_points": points,
            "reasons": reasons,
            "explanation": explanation,
        }


# ---------------------------------------------------------------
# Test area: runs only when you run this file directly
#   python activity_risk_analyzer.py
# ---------------------------------------------------------------
if __name__ == "__main__":
    analyzer = ActivityRiskAnalyzer()

    test_weather = {
        "temperature": 36,
        "humidity": 88,
        "rain_probability": 70,
        "wind_speed": 20,
    }

    result = analyzer.analyze("Football", test_weather)

    print("Activity:", result["activity"])
    print("Risk level:", result["risk_level"])
    print("Points:", result["risk_points"])
    print("Reasons:", result["reasons"])
    print("Explanation:", result["explanation"])
