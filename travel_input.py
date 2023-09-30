# Create a Python script or web form to collect user input for travel date, start location, and destination.

import openai
import config
import requests
import json 

openai.api_key = config.OPEN_AI_API_KEY
google_places_api_key = config.GOOGLE_PLACES_API_KEY
weatherbit_api_key = config.WEATHER_BIT_API_KEY

# CREDIT to Sentdex
# user_destination = input("Enter a city: ")
user_destination = 'Hanoi'
model_engine = "gpt-3.5-turbo"
user_search_string = f"What is the typical weather in {user_destination} in the month of January?"

completion = openai.ChatCompletion.create(
  model=model_engine,
  messages=[{"role": "user", "content": user_search_string}],
  # max_tokens=30,
  n=1,
  stop=None, 
  temperature=0.5,
)
chatgpt_response = completion.choices[0].message.content
# print("chatgpt_response >> ", chatgpt_response)

message_history = []
user_search_string = f"What is the most famous attraction in this city?"
message_history.append({"role": "user", "content": user_search_string})
# print("message_history only user >> ", message_history)

message_history.append({"role": "assistant", "content": chatgpt_response})
# print("message_history with assistant >> ", message_history)

completion = openai.ChatCompletion.create(
  model=model_engine,
  messages=message_history,
)

chatgpt_response = completion.choices[0].message.content
print("chatgpt_response 2 >> ", chatgpt_response)


#get place id
google_place_id_url=f'https://maps.googleapis.com/maps/api/geocode/json?address={user_destination}&key={google_places_api_key}'
response_google_place_id = requests.get(google_place_id_url)
converted_response = json.loads(response_google_place_id.text)
retreived_place_id = converted_response['results'][0]['place_id']

#get place details. use the place id.
google_place_details_url=f'https://maps.googleapis.com/maps/api/place/details/json?place_id={retreived_place_id}&key={google_places_api_key}'
response_google_place_details = requests.get(google_place_details_url)
converted_response = json.loads(response_google_place_details.text)
retreived_place_details = converted_response['result']

#access the details desired
place_full_name = retreived_place_details["formatted_address"]
place_icon = retreived_place_details["icon"]
place_url = retreived_place_details["url"]
 
print('place_full_name >>', place_full_name)
print('place_icon >>', place_icon)
print('place_url >>', place_url)


# weather testing
place_full_name='hanoi, vn'


weather_data_list = [
    {
        'app_max_temp': 41.3, 'app_min_temp': 25.9, 'clouds': 39, 'clouds_hi': 8, 'clouds_low': 17,
        'clouds_mid': 4, 'datetime': '2023-10-01', 'dewpt': 24.5, 'high_temp': 34.3, 'low_temp': 26,
        'max_dhi': None, 'max_temp': 34.3, 'min_temp': 24.9, 'moon_phase': 0.964344, 'moon_phase_lunation': 0.54,
        'moonrise_ts': 1696160000, 'moonset_ts': 1696120080, 'ozone': 266.8, 'pop': 0, 'precip': 0, 'pres': 1007.7,
        'rh': 77, 'slp': 1009.2, 'snow': 0, 'snow_depth': 0, 'sunrise_ts': 1696114229, 'sunset_ts': 1696157333,
        'temp': 29.3, 'ts': 1696093260, 'uv': 7.5, 'valid_date': '2023-10-01',
        'weather': {'code': 802, 'icon': 'c02d', 'description': 'Scattered clouds'},
        'wind_cdir': 'SSW', 'wind_cdir_full': 'south-southwest', 'wind_dir': 204, 'wind_gust_spd': 1.6, 'wind_spd': 1.4
    }
]


#get weather data
weatherbit_forecast_url = f'https://api.weatherbit.io/v2.0/forecast/daily?city={place_full_name}&key={weatherbit_api_key}'
# print("weatherbit_forecast_url>> ", weatherbit_forecast_url)

response_weatherbit_forecast = requests.get(weatherbit_forecast_url)
converted_weather_response = json.loads(response_weatherbit_forecast.text)
retreived_weather=converted_weather_response["data"][:7]

# CREDIT Chatgpt
class WeatherDay:
  def __init__(self, weather_object):
    self.date = weather_object.get('datetime', None)
    self.min_temp = weather_object.get('min_temp' , None)
    self.max_temp = weather_object.get('max_temp', None)
    self.description = weather_object.get('weather', None).get('description', None)

  def __str__(self):
    return f"Date: {self.date}. Degrees: {self.min_temp}-{self.max_temp}. Description: {self.description}"

weather_instances_list = [WeatherDay(weather_obj) for weather_obj in retreived_weather]

for day in weather_instances_list:
  print(day)


