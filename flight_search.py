import requests
import os
import datetime
from dateutil.relativedelta import relativedelta


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.header = {
            "apikey": os.environ["TEQUILA_KEY"]
        }
        self.endpoint = "https://api.tequila.kiwi.com"
        self.geo_endpoint = "https://geocode.maps.co/search"
        tomorrow_unformatted = datetime.date.today() + datetime.timedelta(days=1)
        six_months_unformatted = tomorrow_unformatted + relativedelta(months=+6)
        self.tomorrow = str(tomorrow_unformatted.strftime("%d/%m/%Y"))
        self.six_months = str(six_months_unformatted.strftime("%d/%m/%Y"))

    def get_iata(self, city):
        search_endpoint = f"{self.endpoint}/locations/query"
        parameters = {
            "term": city,
            "locale": "en-US",
            "location_types": "city"
        }
        try:
            response = requests.get(url=search_endpoint, params=parameters, headers=self.header)
            response.raise_for_status()
        except requests.HTTPError:
            print("Error")
            return "null"
        else:
            iata_code = response.json()["locations"][0]["code"]
            return iata_code

    def get_flights(self, start, city_list):
        # get list of cities in main, then call
        search_endpoint = f"{self.endpoint}/v2/search"
        dest_cities = ""
        for city in city_list:
            dest_cities += city
            if city != city_list[-1]:
                dest_cities += ","
        parameters = {
            "fly_from": f"{start[0]}-{start[1]}-{start[2]}km",
            "fly_to": dest_cities,
            "date_from": self.tomorrow,
            "date_to": self.six_months,
            "one_for_city": 1,
            "one_per_date": 1
        }
        try:
            response = requests.get(url=search_endpoint, params=parameters, headers=self.header)
            response.raise_for_status()
        except requests.HTTPError:
            print("Error")
            print(response.reason)
            pass
        else:
            data = response.json()
            return data

    def get_location(self, city, state):
        parameters = {
            "city": city,
            "state": state
        }
        try:
            response = requests.get(url=self.geo_endpoint, params=parameters)
            response.raise_for_status()
        except requests.HTTPError:
            pass
        else:
            data = response.json()
            return data
