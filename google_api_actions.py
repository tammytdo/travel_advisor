import requests
import json
import config

google_places_api_key = config.GOOGLE_PLACES_API_KEY

def get_place_id(user_dest):
  google_place_id_url=f'https://maps.googleapis.com/maps/api/geocode/json?address={user_dest}&key={google_places_api_key}'
  response_google_place_id = requests.get(google_place_id_url)
  converted_place_id_response = json.loads(response_google_place_id.text)
  retreived_place_id = converted_place_id_response['results'][0]['place_id']
  return retreived_place_id

def get_place_details(place_id):
  google_place_details_url=f'https://maps.googleapis.com/maps/api/place/details/json?place_id={place_id}&key={google_places_api_key}'
  response_google_place_details = requests.get(google_place_details_url)
  converted_place_full_details_response = json.loads(response_google_place_details.text)
  retreived_place_full_details = converted_place_full_details_response['result']

  place_full_name = retreived_place_full_details["formatted_address"]
  place_url = retreived_place_full_details["url"]
  place_lat = retreived_place_full_details['geometry']['location']['lat']
  place_lng = retreived_place_full_details['geometry']['location']['lng']
  details_list = [place_full_name, place_url, place_lat, place_lng]
  return details_list

#get restaurants within 16000 meters / 10 miles
def get_restaurants(lat,lng):
  google_nearby_restaurants_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&type=restaurant&radius=16000&key={google_places_api_key}'
  response_nearby_restaurants_search = requests.get(google_nearby_restaurants_url)
  converted_nearby_restaurants_search = json.loads(response_nearby_restaurants_search.text)
  nearby_restaurant_results = [restaurant for restaurant in converted_nearby_restaurants_search['results']]
  nearby_restaurant_results_sorted = sorted(nearby_restaurant_results, key=lambda x: x.get('rating', 0), reverse=True)

  restaurant_list = []
  for restaurant in nearby_restaurant_results_sorted:
      restaurant_list.append({
          "name": restaurant['name'],
          "rating": restaurant.get('rating', 'N/A'),
          "address": restaurant['vicinity'],
          "lat": restaurant['geometry']['location']['lat'],
          "lng": restaurant['geometry']['location']['lng']
      })

  return restaurant_list

#get tourist attractions within 16000 meters / 10 miles
def get_attractions(lat,lng):
  google_nearby_tourist_attraction_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&type=tourist_attraction&radius=16000&key={google_places_api_key}'
  response_nearby_attraction_search = requests.get(google_nearby_tourist_attraction_url)
  converted_nearby_attractions_search = json.loads(response_nearby_attraction_search.text)
  nearby_attraction_results = [attraction for attraction in converted_nearby_attractions_search['results']]
  nearby_attraction_results_sorted = sorted(nearby_attraction_results, key=lambda x: x.get('rating', 0), reverse=True)
  attractions_list = []
  for attraction in nearby_attraction_results_sorted:
      attractions_list.append({
        "name": attraction['name'],
        "address": attraction['vicinity'],
        "rating": attraction.get('rating', 'N/A'),
        "lat": attraction['geometry']['location']['lat'],
        "lng": attraction['geometry']['location']['lng']
    })

  return attractions_list