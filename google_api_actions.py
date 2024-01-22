import requests
import json
import config

google_places_api_key = config.GOOGLE_PLACES_API_KEY

def import_json_file(file_path):
    with open(file_path, 'r') as json_file:
        data = json.load(json_file)
    return data

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
  # google_nearby_restaurants_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&type=restaurant&radius=16000&key={google_places_api_key}'

  # response_nearby_restaurants_search = requests.get(google_nearby_restaurants_url)
  restaurants_data_path = "sample_response/sample_restaurants.json" # for testing
  
  # converted_nearby_restaurants_search = json.loads(response_nearby_restaurants_search.text)
  

  converted_nearby_restaurants_search = import_json_file(restaurants_data_path)  # for testing 

  nearby_restaurant_results = [restaurant for restaurant in converted_nearby_restaurants_search['results']]

  nearby_restaurant_results_sorted_rating = sorted(nearby_restaurant_results, key=lambda x: x.get('rating', 0), reverse=True)

  restaurant_list_unsorted = []
  for restaurant in nearby_restaurant_results_sorted_rating:
        excluded_types = ['lodging', 'spa', 'gym']
        if (
            not any(excluded_type in restaurant['types'] for excluded_type in excluded_types) 
            and restaurant.get('rating', 0) >= 3.5 
            and restaurant.get('user_ratings_total', 0) > 100
        ):
          restaurant_list_unsorted.append({
            "name": restaurant['name'],
            "rating": restaurant.get('rating', 'N/A'),
            "address": restaurant['vicinity'],
            "lat": restaurant['geometry']['location']['lat'],
            "lng": restaurant['geometry']['location']['lng'],
            "price_level": restaurant.get('price_level', 'N/A'),
            "photos": restaurant.get('photos', [{'html_attributions': []}])[0]['html_attributions'],
            "types": restaurant['types']
      })
          
  return restaurant_list_unsorted
 

#get tourist attractions within 16000 meters / 10 miles
def get_attractions(lat,lng):
  google_nearby_tourist_attraction_url = f'https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lng}&type=tourist_attraction&radius=16000&key={google_places_api_key}'
  response_nearby_attraction_search = requests.get(google_nearby_tourist_attraction_url)
  converted_nearby_attractions_search = json.loads(response_nearby_attraction_search.text)
  nearby_attraction_results = [attraction for attraction in converted_nearby_attractions_search['results']]
  nearby_attraction_results_sorted = sorted(nearby_attraction_results, key=lambda x: x.get('rating', 0), reverse=True)
  attractions_list_unsorted = []
  for attraction in nearby_attraction_results_sorted:
    if attraction.get('rating', 0) >= 3.5 and attraction.get('user_ratings_total', 0) > 200:
      attractions_list_unsorted.append({
        "name": attraction['name'],
        "address": attraction['vicinity'],
        "rating": attraction.get('rating', 'N/A'),
        "lat": attraction['geometry']['location']['lat'],
        "lng": attraction['geometry']['location']['lng'],
        "price_level": attraction.get('price_level', 'N/A'),
        "photos": attraction.get('photos', [{'html_attributions': []}])[0]['html_attributions'],
        "types": attraction['types']

    })


  attractions_list = sorted(  attractions_list_unsorted = [], key=lambda x: x['rating'], reverse=True)

  return attractions_list