# This file will need to use the DataManager,FlightSearch, FlightData,
# NotificationManager classes to achieve the program requirements.
from data_manager import DataManager
from flight_search import FlightSearch
from flight_data import FlightData

data = DataManager()
# data.fill_codes()

city = input("What city are you in right now? ")
state = input("What state are you in right now? ")

f = FlightSearch()
location = f.get_location(city=city, state=state)
lat = round(float(location[0]["lat"]), 2)
lon = round(float(location[0]["lon"]), 2)

km = int(input("In what kilometer radius do you want to search for airports? "))
from_list = [lat, lon, km]

city_list = data.get_cities()
flight_list = f.get_flights(start=from_list, city_list=city_list)

f_data = FlightData(flight_list=flight_list, city_list=city_list)
f_data.organize_data()
