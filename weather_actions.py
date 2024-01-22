import requests
import config
from models import WeatherDay

weatherbit_api_key = config.WEATHER_BIT_API_KEY

def get_weather_data(destination):
  weatherbit_forecast_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={destination}&key={weatherbit_api_key}'

  response_weatherbit_forecast = requests.get(weatherbit_forecast_url)
  converted_weather_response = response_weatherbit_forecast.json()
  retreived_weather=converted_weather_response.get('data', [])[:7]
  weather_instances_list = [WeatherDay(weather_obj) for weather_obj in retreived_weather]

  return [weather.to_json() for weather in weather_instances_list]
