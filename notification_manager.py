import smtplib
import os


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        # Initializes the class with the sending email & password and the user to receive the email.
        self.sender = "dwdeathwolf@gmail.com"
        self.password = os.environ["APP_PASS"]
        self.receiver = "jhecker2001@gmail.com"

    def send_email(self, price, from_city, fc_code, to_city, tc_code, departure, arrival):
        # Sends an email to the user.
        # price - The cheapest flight price to the destination.
        # from_city - The departure city.
        # fc_code - The IATA code of the departure location.
        # to_city - The destination city.
        # tc_code - The IATA code of the destination city.
        # departure - The departure date of the flight.
        # arrival - The arrival date of the flight.

        with smtplib.SMTP(host="smtp.gmail.com", port=587) as connection:
            connection.starttls()
            connection.login(user=self.sender, password=self.password)
            connection.sendmail(
                from_addr=self.sender,
                to_addrs=self.receiver,
                msg=f"Subject:Low price alert!\n\n"
                    f"Only {price} euros to fly from {from_city}-{fc_code} to {to_city}-{tc_code},"
                    f" from {departure} to {arrival}."
            )
