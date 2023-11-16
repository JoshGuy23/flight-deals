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
                    "IATA Code": iata_code
                }
            }
            try:
                response = requests.put(url=put_endpoint, json=changes, headers=self.header)
                response.raise_for_status()
            except requests.HTTPError:
                pass
