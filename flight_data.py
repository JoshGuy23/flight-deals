# API Documentation
#   https://tequila.kiwi.com/portal/docs/tequila_api/search_api
#   https://sheety.co/docs/requests.html
# Google Sheet
#   https://docs.google.com/spreadsheets/d/1WyXaXjvrkXv4Kwnbbo9Hvhyux6TDZJVK8VU-0LR7emw/edit#gid=0
# Project Requirements
#   https://www.udemy.com/course/100-days-of-code/learn/lecture/21371844#questions
# This class is responsible for structuring the flight data.
# Get flight_list["data"]
# When getting entries, somehow sort by dest city, keep record with lowest price
# for entry in flight_records
#   get entry["cityCodeFrom"]
#   get entry["cityFrom"]
#   get entry["cityCodeTo"]
#   get entry["cityTo"]
#   get entry["local_departure"]
#   get entry["local_arrival"]
#       times come formatted as "yyyy-mm-ddThh:mm:ss.000Z", 24h format
#   get entry["price"]
# get list of prices and codes from sheet
# if flight price lower, put new prices back into sheets w/ data_manager
# for each price update, send email
from data_manager import DataManager
from notification_manager import NotificationManager


class FlightData:
    def __init__(self, flight_list, city_list):
        manager = DataManager()
        self.flight_data = flight_list["data"]
        self.city_data = city_list
        self.price_list = [manager.get_price(city) for city in self.city_data]
        pass

    def organize_data(self):
        i = 0
        for city in self.city_data:
            city_flights = [entry for entry in self.flight_data if city == entry["cityCodeTo"]]
            if len(city_flights) > 0:
                prices = [flight["price"] for flight in city_flights]
                min_price = min(prices)
                cheapest_flight = [flight for flight in city_flights if flight["price"] == min_price]
                cheapest_flight = cheapest_flight[0]
                current_price = self.price_list[i]
                if min_price < current_price:
                    sender = NotificationManager()
                    from_code = cheapest_flight["cityCodeFrom"]
                    from_city = cheapest_flight["cityFrom"]
                    to_code = cheapest_flight["cityCodeTo"]
                    to_city = cheapest_flight["cityTo"]
                    departure_time = cheapest_flight["local_departure"].split("T")[0]
                    arrival_time = cheapest_flight["local_arrival"].split("T")[0]
                    sender.send_email(price=min_price, from_city=from_city, fc_code=from_code, to_city=to_city,
                                      tc_code=to_code, departure=departure_time, arrival=arrival_time)
            i += 1
