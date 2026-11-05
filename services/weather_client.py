import requests

class WeatherClient:
    def __init__(self):
        self.base_url = "https://api.open-meteo.com/v1/forecast"

    def get_weather(self, latitude, longitude):
        params = {
            "latitude": latitude,
            "longitude": longitude,
            "current": [
                "temperature_2m",
                "relative_humidity_2m",
                "precipitation",
                "wind_speed_10m"
            ],
            "hourly": [
                "precipitation_probability"
            ],
            "timezone": "auto"
        }

        try:
            response = requests.get(self.base_url, params=params, timeout=10)
            response.raise_for_status()
            return response.json()
        except requests.exceptions.RequestException as error:
            print(f"Weather API error: {error}")
            return None