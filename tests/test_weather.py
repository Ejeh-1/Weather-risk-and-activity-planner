from services.weather_client import WeatherClient
from models.forecast import Forecast

client = WeatherClient()
data = client.get_weather(9.0765, 7.3986)
if data:
    forecast = Forecast(data)

    print("weather dictionary:", forecast.to_dict())


    print("Temperature:", forecast.get_temperature(), "°C")
    print("Humidity:", forecast.get_humidity(), "%")
    print("Wind speed:", forecast.get_wind_speed(), "km/h")
    print("Rain probability:", forecast.get_rain_probability())
else:
    print("Could not retrieve weather data.")