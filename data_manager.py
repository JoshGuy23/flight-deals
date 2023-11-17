import requests
import os
from flight_search import FlightSearch


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        # Initializes the header and endpoint needed to interface with the Google Sheet.
        self.header = {
            "Authorization": f"Basic {os.environ["SHEETY_AUTH"]}"
        }
        self.endpoint = "https://api.sheety.co/e07399c5a2dc2b012ac72f6585597114/flightDeals/prices"

    def get_rows(self):
        # Gets the data from the Google Sheet.
        try:
            response = requests.get(url=self.endpoint, headers=self.header)
            response.raise_for_status()
        except requests.HTTPError:
            print(response.reason)
        else:
            data = response.json()
            return data

    def fill_codes(self):
        # Fill in any missing IATA codes in the Google Sheet.
        data = self.get_rows()["prices"]
        searcher = FlightSearch()

        for entry in data:
            # Get the current row.
            city = entry["city"]
            row_id = entry["id"]

            # Get the IATA code of the city in the current row.
            iata_code = searcher.get_iata(city)
            put_endpoint = f"{self.endpoint}/{row_id}"
            changes = {
                "price": {
                    "iataCode": iata_code
                }
            }
            # Put the IATA code in the corresponding row of the Google Sheet.
            try:
                response = requests.put(url=put_endpoint, json=changes, headers=self.header)
                response.raise_for_status()
            except requests.HTTPError:
                print(response.reason)

    def get_price(self, city):
        # Get the corresponding price of a city from the Google Sheet.
        data = self.get_rows()["prices"]
        price = [entry["lowestPrice"] for entry in data if entry["iataCode"] == city]
        return price[0]

    def get_cities(self):
        # Get a list of cities from the Google Sheet
        data = self.get_rows()["prices"]
        cities = [entry["iataCode"] for entry in data]
        return cities
