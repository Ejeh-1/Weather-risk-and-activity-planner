import requests  # Imports the requests library for making HTTP requests
from exceptions import WeatherDataError

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
            response = requests.get(
                self.base_url,

                params=params,

                timeout=20

            )

            response.raise_for_status()

            data = response.json()

            if not isinstance(data, dict):

                raise WeatherDataError(

                    "The weather API returned an invalid response."

                )

            if not isinstance(data.get("current"), dict):

                raise WeatherDataError(

                    "Current weather information is missing."

                )

            if not isinstance(data.get("hourly"), dict):

                raise WeatherDataError(

                    "Hourly weather information is missing."

                )

            return data

        except requests.exceptions.RequestException as error:

            raise WeatherDataError(

                "Unable to connect to the weather service. Please check your internet connection."

            ) from error

        except ValueError as error:

            raise WeatherDataError(

                "The weather service returned invalid JSON data."

            ) from error
