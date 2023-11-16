import requests
import os


class FlightSearch:
    # This class is responsible for talking to the Flight Search API.
    def __init__(self):
        self.apikey = os.environ["TEQUILA_KEY"]
        self.endpoint = "https://api.tequila.kiwi.com/"

    def get_iata(self, city):
        search_endpoint = f"{self.endpoint}locations/query"
        parameters = {
            "apikey": self.apikey,
            "term": city,
            "locale": "en-US",
            "location_types": "city"
        }
        try:
            response = requests.get(url=search_endpoint, params=parameters)
            response.raise_for_status()
        except requests.HTTPError:
            return "null"
        else:
            iata_code = response.json()["locations"][0]["code"]
            return iata_code
