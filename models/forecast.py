from datetime import datetime

from zoneinfo import ZoneInfo

class Forecast:

    def __init__(self, weather_data, location=None):

        self.weather_data = weather_data or {}

        self.location = location

        self.timezone = self.weather_data.get("timezone", "UTC")

        self.local_now = self._get_local_now()


def _get_local_now(self):

    try:

        return datetime.now(ZoneInfo(self.timezone))

    except (ValueError, KeyError):

        return datetime.now()

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

    valid = [

        value for value in probabilities[:24]

        if isinstance(value, (int, float))

    ]

    return max(valid) if valid else None

def daytime_hours(self, day, start_hour, end_hour):

    hourly = self.get_hourly_forecast()

    times = hourly.get("time", [])

    results = []

    for index, timestamp in enumerate(times):

        try:

            hour_time = datetime.fromisoformat(timestamp)

            if hour_time.date() != day:

                continue

            if not start_hour <= hour_time.hour < end_hour:

                continue

            def get_value(key, default=None):

                values = hourly.get(key, [])

                if index >= len(values):

                    return default

                return values[index]

            results.append(

                ForecastHour(

                    time=hour_time,

                    temperature=get_value("temperature_2m"),

                    apparent_temp=get_value("apparent_temperature"),

                    rain_probability=get_value(

                        "precipitation_probability", 0

                    ),

                    wind_speed=get_value("wind_speed_10m", 0),

                    wind_gusts=get_value("wind_gusts_10m", 0),

                    uv_index=get_value("uv_index", 0),

                    humidity=get_value("relative_humidity_2m", 0),

                    is_thunderstorm=get_value(

                        "is_thunderstorm", False

                    ),

                    description=get_value("weather_code", "Unknown"),

                )

            )

        except (ValueError, TypeError):

            continue

    return results

def to_dict(self):

    return {

        "temperature": self.get_temperature(),

        "humidity": self.get_humidity(),

        "rain_probability": self.get_rain_probability(),

        "wind_speed": self.get_wind_speed()

    }

class ForecastHour:

    def __init__(

        self,

        time,

        temperature,

        apparent_temp,

        rain_probability,

        wind_speed,

        wind_gusts,

        uv_index,

        humidity,

        is_thunderstorm,

        description,

    ):

        self.time = time

        self.temperature = temperature

        self.apparent_temp = apparent_temp

        self.rain_probability = rain_probability

        self.wind_speed = wind_speed

        self.wind_gusts = wind_gusts

        self.uv_index = uv_index

        self.humidity = humidity

        self.is_thunderstorm = bool(is_thunderstorm)

        self.description = str(description)
