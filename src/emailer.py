#!/usr/bin/python

import smtplib

class Emailer():
    def __init__(self, email, password_file, sending_to):
        self.email = email
        self.password_file = password_file
        self.sending_to = sending_to

        f = open(password_file, 'r')
        self.password = f.readline()

    def send_email(self, text):
        self.email_server = smtplib.SMTP("smtp.gmail.com", 587)
        self.email_server.starttls()
        self.email_server.login(self.email, self.password)
        self.email_server.sendmail(self.email, self.sending_to, text)
        self.email_server.quit()
