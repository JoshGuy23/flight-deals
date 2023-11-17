import requests
import os
from flight_search import FlightSearch


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.header = {
            "Authorization": f"Basic {os.environ["SHEETY_AUTH"]}"
        }
        self.endpoint = "https://api.sheety.co/e07399c5a2dc2b012ac72f6585597114/flightDeals/prices"

    def get_rows(self):
        try:
            response = requests.get(url=self.endpoint, headers=self.header)
            response.raise_for_status()
        except requests.HTTPError:
            print(response.reason)
            pass
        else:
            data = response.json()
            return data

    def fill_codes(self):
        data = self.get_rows()["prices"]
        searcher = FlightSearch()
        for entry in data:
            city = entry["city"]
            row_id = entry["id"]
            iata_code = searcher.get_iata(city)
            put_endpoint = f"{self.endpoint}/{row_id}"
            changes = {
                "price": {
                    "iataCode": iata_code
                }
            }
            try:
                response = requests.put(url=put_endpoint, json=changes, headers=self.header)
                response.raise_for_status()
            except requests.HTTPError:
                pass

    def get_price(self, city):
        data = self.get_rows()["prices"]
        price = [entry["lowestPrice"] for entry in data if entry["iataCode"] == city]
        return price[0]

    def get_cities(self):
        data = self.get_rows()["prices"]
        cities = [entry["iataCode"] for entry in data]
        return cities
