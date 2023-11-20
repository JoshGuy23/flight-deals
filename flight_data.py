from data_manager import DataManager
from notification_manager import NotificationManager


class FlightData:
    # This class is responsible for structuring the flight data.
    def __init__(self, flight_list, city_list):
        # Initializes the class with a list of flights, a list of city IATA codes,
        # and a list of prices corresponding to the IATA codes.
        manager = DataManager()
        self.flight_data = flight_list["data"]
        self.city_data = city_list
        self.price_list = [manager.get_price(city) for city in self.city_data]

    def organize_data(self):
        # Organizes data and sends an email if the flight price is low enough.
        i = 0
        for city in self.city_data:
            # Get all the flights corresponding to the current city.
            city_flights = [entry for entry in self.flight_data if city == entry["cityCodeTo"]]

            if len(city_flights) > 0:
                # Get the cheapest flight price to the current city.
                prices = [flight["price"] for flight in city_flights]
                min_price = min(prices)
                cheapest_flight = [flight for flight in city_flights if flight["price"] == min_price]
                cheapest_flight = cheapest_flight[0]

                # Get the price of the current city from the Google Sheet.
                current_price = self.price_list[i]

                # If the cheapest flight price is cheaper than the price from the Google Sheet, get the necessary
                # information and send an email.
                if min_price < current_price:
                    sender = NotificationManager()
                    route_list = cheapest_flight["route"]
                    stopovers = 0
                    stop_list = ""

                    # If the route has stopovers, get the number of stopovers and get the stop-over cities.
                    if len(route_list) > 1:
                        stopovers += len(route_list) - 1
                        for route in route_list:
                            if route != route_list[-1]:
                                stop_list += route["cityTo"] + ","

                    from_code = cheapest_flight["cityCodeFrom"]
                    from_city = cheapest_flight["cityFrom"]

                    to_code = cheapest_flight["cityCodeTo"]
                    to_city = cheapest_flight["cityTo"]

                    departure_time = cheapest_flight["local_departure"].split("T")[0]
                    arrival_time = cheapest_flight["local_arrival"].split("T")[0]

                    sender.send_email(price=min_price, from_city=from_city, fc_code=from_code, to_city=to_city,
                                      tc_code=to_code, departure=departure_time, arrival=arrival_time,
                                      stop_over=stopovers, via_city=stop_list)

            i += 1

# Notes to self:
# API Documentation
#   https://tequila.kiwi.com/portal/docs/tequila_api/search_api
#   https://sheety.co/docs/requests.html
# Google Sheet
#   https://docs.google.com/spreadsheets/d/1WyXaXjvrkXv4Kwnbbo9Hvhyux6TDZJVK8VU-0LR7emw/edit#gid=0
# Project Requirements
#   https://www.udemy.com/course/100-days-of-code/learn/lecture/21371844#questions

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
