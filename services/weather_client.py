import requests  # Imports the requests library for making HTTP requests

class WeatherClient:
    """Handles communication with the Open-Meteo weather API."""

def __init__(self):
    # Stores the API endpoint used to retrieve weather forecasts
    self.base_url = "https://api.open-meteo.com/v1/forecast"
def get_weather(self, latitude, longitude):
    # Prepares the parameters to send to the weather API
    params = {
        "latitude": latitude,  # Geographical latitude of the location
        "longitude": longitude,  # Geographical longitude of the location
        # Requests the current weather conditions
        "current": [
            "temperature_2m",
            "relative_humidity_2m",
            "precipitation",
            "wind_speed_10m",
            "weather_code"
        ],
        # Requests hourly weather information for risk analysis
        "hourly": [
            "temperature_2m",
            "apparent_temperature",
            "precipitation_probability",
            "wind_speed_10m",
            "wind_gusts_10m",
            "uv_index",
            "relative_humidity_2m",
            "weather_code"
        ],
        "forecast_days": 7,  # Retrieves forecasts for seven days
        "timezone": "auto"  # Automatically detects the location's timezone
    }
    try:
        # Sends a GET request to the Open-Meteo API
        response = requests.get(
            self.base_url,
            params=params,
            timeout=10  # Stops waiting if the request takes too long
        )
        # Checks whether the API request was successful
        response.raise_for_status()
        # Converts the JSON response into a Python dictionary
        return response.json()
    except requests.exceptions.RequestException as error:
        # Handles network errors and unsuccessful API requests
        print(f"Weather API error: {error}")
        return None
    except ValueError as error:
        # Handles errors when the response contains invalid JSON
        print(f"Invalid weather API response: {error}")
        return None
