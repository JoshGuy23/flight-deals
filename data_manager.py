import requests
import os


class DataManager:
    # This class is responsible for talking to the Google Sheet.
    def __init__(self):
        self.header = {
            "Authorization": f"Basic {os.environ["SHEETY_AUTH"]}"
        }
        self.get_endpoint = "https://api.sheety.co/e07399c5a2dc2b012ac72f6585597114/flightDeals/prices"

    def get_rows(self):
        try:
            response = requests.get(url=self.get_endpoint, headers=self.header)
            response.raise_for_status()
        except requests.HTTPError:
            pass
        else:
            data = response.json()
            return data
