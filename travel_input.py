# Create a Python script or web form to collect user input for travel date, start location, and destination.

import openai
import config
import requests
import json 

openai.api_key = config.OPEN_AI_API_KEY
google_places_api_key = config.GOOGLE_PLACES_API_KEY

# user_destination = input("Enter a city: ")
user_destination = 'Hanoi'
model_engine = "gpt-3.5-turbo"
user_search_string = f"What is the typical weather in {user_destination} in the month of January?"
'''
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
'''

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
