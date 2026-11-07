from dataclasses import dataclass
from datetime import datetime, date
from zoneinfo import ZoneInfo


WEATHER_DESCRIPTIONS = {
    0: "Clear sky",
    1: "Mainly clear",
    2: "Partly cloudy",
    3: "Overcast",
    45: "Fog",
    48: "Depositing rime fog",
    51: "Light drizzle",
    53: "Moderate drizzle",
    55: "Dense drizzle",
    56: "Freezing drizzle",
    57: "Heavy freezing drizzle",
    61: "Slight rain",
    63: "Moderate rain",
    65: "Heavy rain",
    66: "Freezing rain",
    67: "Heavy freezing rain",
    71: "Slight snow",
    73: "Moderate snow",
    75: "Heavy snow",
    77: "Snow grains",
    80: "Slight rain showers",
    81: "Moderate rain showers",
    82: "Violent rain showers",
    85: "Slight snow showers",
    86: "Heavy snow showers",
    95: "Thunderstorm",
    96: "Thunderstorm with slight hail",
    99: "Thunderstorm with heavy hail"
    }

@dataclass
class ForecastHour:
    """Stores weather information for a particular hour."""

    time: datetime
    temperature: float
    apparent_temp: float
    rain_probability: float
    wind_speed: float
    wind_gusts: float
    uv_index: float
    humidity: float
    is_thunderstorm: bool
    description: str

class Forecast:
    """Processes current and hourly weather forecast data."""

    def __init__(self, weather_data, location=None):
        # Stores the weather information returned by the API
        self.weather_data = weather_data or {}
        # Stores the location associated with the forecast
        self.location = location
        # Gets the timezone provided by the weather API
        self.timezone = self.weather_data.get("timezone", "UTC")
        # Gets the current local time for the forecast location
        self.local_now = self._get_local_now()
    def _get_local_now(self):
        """Returns the current time in the forecast location's timezone."""
        try:
            # Uses the location's timezone when it is valid
            return datetime.now(ZoneInfo(self.timezone))
        except (ValueError, TypeError, KeyError):
            # Falls back to the computer's local time
            return datetime.now()
    def get_current_weather(self):
        """Returns the current weather information."""
        return self.weather_data.get("current", {})
    def get_hourly_forecast(self):
        """Returns the hourly forecast information."""
        return self.weather_data.get("hourly", {})
    def get_temperature(self):
        """Returns the current temperature."""
        return self.get_current_weather().get("temperature_2m")
    def get_humidity(self):
        """Returns the current relative humidity."""
        return self.get_current_weather().get(
            "relative_humidity_2m"
        )
    def get_wind_speed(self):
        """Returns the current wind speed."""
        return self.get_current_weather().get("wind_speed_10m")
    def get_rain_probability(self):
        """Returns the highest rain probability in the next 24 hours."""
        probabilities = self.get_hourly_forecast().get(
            "precipitation_probability", []
        )
        # Selects the next 24 hourly rain probability values
        next_24_hours = probabilities[:24]
        # Keeps only valid numeric values
        valid_values = [
            value for value in next_24_hours
            if isinstance(value, (int, float)) 
            and not isinstance(value, bool)
        ]
        # Returns the highest probability, or None if unavailable
        return max(valid_values) if valid_values else None
    def get_weather_description(self, weather_code):
        """Converts a weather code into a readable description."""
        if weather_code is None:
            return "Unknown"
        return WEATHER_DESCRIPTIONS.get(
            weather_code, "Unknown weather condition"
        )
    def daytime_hours(self, day, start_hour, end_hour):
        """
        Returns hourly forecasts within the requested date
        and activity time range.
        """
        hourly = self.get_hourly_forecast()
        # Gets the timestamps for the hourly forecast
        times = hourly.get("time", [])
        results = []
        # Processes each available hourly forecast
        for index, timestamp in enumerate(times):
            try:
                # Converts the timestamp into a datetime object
                hour_time = datetime.fromisoformat(timestamp)
                # Skips forecasts that do not match the requested date
                if hour_time.date() != day:
                    continue
                # Skips hours outside the requested time range
                if not start_hour <= hour_time.hour < end_hour:
                    continue
                # Retrieves a weather value at the current index
                def get_value(key):
                    values = hourly.get(key, [])
                    if index >= len(values):
                        return None
                    return values[index]
                # Retrieves the weather code for this hour
                weather_code = get_value("weather_code")
                # Determines whether thunderstorms are expected
                is_thunderstorm = weather_code in (95, 96, 99)
                # Converts the weather code into readable text
                description = self.get_weather_description(
                    weather_code
                )
                # Creates an object containing this hour's weather data
                forecast_hour = ForecastHour(
                    time=hour_time,
                    temperature=get_value("temperature_2m"),
                    apparent_temp=get_value("apparent_temperature"),
                    rain_probability=get_value(
                        "precipitation_probability"
                    ),
                    wind_speed=get_value("wind_speed_10m"),
                    wind_gusts=get_value("wind_gusts_10m"),
                    uv_index=get_value("uv_index"),
                    humidity=get_value("relative_humidity_2m"),
                    is_thunderstorm=is_thunderstorm,
                    description=description
                )
                # Adds the hourly forecast to the results
                results.append(forecast_hour)
            except (ValueError, TypeError):
                # Skips timestamps that cannot be processed
                continue
        return results
    def to_dict(self):
        """Returns the current weather information as a dictionary."""
        return {
            "temperature": self.get_temperature(),
            "humidity": self.get_humidity(),
            "rain_probability": self.get_rain_probability(),
            "wind_speed": self.get_wind_speed()
        }
