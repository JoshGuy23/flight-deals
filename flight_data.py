class FlightData:
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
    # if flight price lower, new min price replaced in price list
    # after done, put new prices back into sheets w/ data_manager
    # for each price update, send email
    pass
