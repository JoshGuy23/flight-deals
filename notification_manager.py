import smtplib
import os


class NotificationManager:
    # This class is responsible for sending notifications with the deal flight details.
    def __init__(self):
        self.sender = "dwdeathwolf@gmail.com"
        self.password = os.environ["APP_PASS"]
        self.receiver = "jhecker2001@gmail.com"

    def send_email(self, price, from_city, fc_code, to_city, tc_code, departure, arrival):
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
