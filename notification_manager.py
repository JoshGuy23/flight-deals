import smtplib
import os
from data_manager import DataManager


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        # Initializes the class with the sending email & password and the list of users to receive emails.
        self.sender = "dwdeathwolf@gmail.com"
        self.password = os.environ["APP_PASS"]
        manager = DataManager()
        self.email_list = manager.get_emails()

    def send_email(self, price, from_city, fc_code, to_city, tc_code, departure, arrival, stop_over, via_city):
        # Sends emails to users on the mailing list.
        # price - The cheapest flight price to the destination.
        # from_city - The departure city.
        # fc_code - The IATA code of the departure location.
        # to_city - The destination city.
        # tc_code - The IATA code of the destination city.
        # departure - The departure date of the flight.
        # arrival - The arrival date of the flight.
        # stop_over - The number of stop-overs from from_city to to_city.
        # via_city - The list of cities stopped at during the flight.

        if stop_over > 0:
            stop_msg = f"\n\nFlight has {stop_over} stop overs, via {via_city}."
        else:
            stop_msg = ""

        for receiver in self.email_list:
            with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
                connection.starttls()
                connection.login(user=self.sender, password=self.password)
                connection.sendmail(
                    from_addr=self.sender,
                    to_addrs=receiver,
                    msg=f"Subject:Low price alert!\n\n"
                        f"Only {price} euros to fly from {from_city}-{fc_code} to {to_city}-{tc_code},"
                        f" from {departure} to {arrival}.{stop_msg}"
                )
