class Forecast:
    def __init__(self, weather_data):
        self.weather_data = weather_data

    def get_current_weather(self):
        return self.weather_data.get("current", {})
    
    def get_hourly_forecast(self):
        return self.weather_data.get("hourly", {})

    def get_temperature(self):
        return self.get_current_weather().get("temperature_2m")

    def get_humidity(self):
        return self.get_current_weather().get("relative_humidity_2m")

    def get_wind_speed(self):
        return self.get_current_weather().get("wind_speed_10m")

    def get_rain_probability(self):
        probabilities = self.get_hourly_forecast().get(
            "precipitation_probability", []
        )

        next_24_hours = probabilities[:24]
        valid_values = [
            value for value in next_24_hours
            if isinstance(value, (int, float))
        ]
        return max(valid_values) if valid_values else None
    def to_dict(self):
        return {
            "temperature": self.get_temperature(),
            "humidity": self.get_humidity(),
            "rain_probability": self.get_rain_probability(),
            "wind_speed": self.get_wind_speed()
        }