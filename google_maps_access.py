import requests
import json
import time
class GooglePlaces(object):
    def __init__(self, apiKey):
        super(GooglePlaces, self).__init__()
        self.apiKey = apiKey

    def search_places_by_coordinate(self, location, radius, types):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/nearbysearch/json"
        places = []
        params = {
            'location': location,
            'radius': radius,
            'types': types,
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        results =  json.loads(res.content)
        places.extend(results['results'])
        time.sleep(2)
        while "next_page_token" in results:
            params['pagetoken'] = results['next_page_token'],
            res = requests.get(endpoint_url, params = params)
            results = json.loads(res.content)
            places.extend(results['results'])
            time.sleep(2)
        print (places)
        return places

    def get_place_details(self, place_id, fields):
        endpoint_url = "https://maps.googleapis.com/maps/api/place/details/json"
        params = {
            'placeid': place_id,
            'fields': ",".join(fields),
            'key': self.apiKey
        }
        res = requests.get(endpoint_url, params = params)
        place_details =  json.loads(res.content)
        return place_details

if __name__ == '__main__':
    api = GooglePlaces('AIzaSyB6VQWBlXGKUQo4LS4OIjg3GoMUHClD218')

    places = api.search_places_by_coordinate("52.204450, 0.119000", "400", "supermarket")

    output = ['name', 'formatted_address', 'international_phone_number', 'website', 'rating', 'review']

    f = open('output.txt', 'w+')
    for place in places:
        details = api.get_place_details(place['place_id'], output)
        # try:
        #     website = details['result']['website']
        # except KeyError:
        #     website = ""

        try:
            name = details['result']['name']
        except KeyError:
            name = ""

        try:
            address = details['result']['formatted_address']
        except KeyError:
            address = ""

        f.write(name)
        f.write('\n')
        f.write(address)
       
    f.close()