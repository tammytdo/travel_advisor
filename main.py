# Create a Python script or web form to collect user input for travel date, start location, and destination.

import openai
import config
import requests
import json 
from flask import Flask, request, jsonify
from flask_cors import CORS

from openai_actions import get_typical_weather
from google_api_actions  import (
    get_place_id,
    get_place_details,
    get_restaurants,
    get_attractions
)
from weather_actions import get_weather_data

app = Flask(__name__)
CORS(app, resources={r"/*": {"origins": "http://localhost:3000"}})

@app.route('/getCityData', methods=['GET'])
def get_city_data():
  print('Searching... ... ...')
  user_destination = request.args.get('user_destination')
  month = request.args.get('month')
  lat = 47.608013 # for testing
  lng = -122.335167 # for testing

  # typical_weather = get_typical_weather(user_destination, month)
  # place_id = get_place_id(user_destination)
  # place_details = get_place_details(place_id)
  # lat, lon = place_details[2], place_details[3]
  restaurants_list = get_restaurants(lat, lng)
  # attractions_list = get_attractions(lat, lon)
  # upcoming_weather = get_weather_data(user_destination)

  # response = {
  #   'city' : request.args.get('user_destination'),
  #   'lat' : place_details[2],
  #   'lng' : place_details[3],
  #   'typical_weather' : typical_weather,
  #   'upcoming_weather' : upcoming_weather,
  #   'attractions' : attractions_list,
  #   'restaurants' : restaurants_list
  #   }
  
  response = {
  'city' : "Seattle",
  'lat' : 47.608013,
  'lng' : -122.335167,
  # 'typical_weather' : typical_weather,
  # 'upcoming_weather' : upcoming_weather,
  # 'attractions' : attractions_list,
  'restaurants' : restaurants_list
  }
  
  print(response)
  return response

if __name__ == '__main__':
  print('hi py')
  app.run(port=config.PORT, debug=True)
