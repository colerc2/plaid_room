#!/usr/bin/python
import paypalrestsdk
import logging
from paypalrestsdk import Invoice

class PaypalInterface():
    def __init__(self, client_id_, client_secret_):
        self.client_id = client_id_
        self.client_secret = client_secret_
        logging.basicConfig(level=logging.INFO)

        paypalrestsdk.configure({
            "mode": "live", # sandbox or live
            "client_id": self.client_id,
            "client_secret": self.client_secret })

    def create_invoice(self, items):
        
invoice = Invoice({
    'merchant_info': {
        "email": "plaidroomrecords@gmail.com",
    },
    "billing_info": [{
        "email": "plaidroomrecords+invoices@gmail.com"
    }],
    "items": [{
        "name": "Seu Jorge - Stuff",
        "quantity": 1,
        "unit_price": {
            "currency": "USD",
            "value": 19.99
        }
    },{
        "name": "Dr. Dog - Be The Void",
        "quantity": 1,
        "unit_price": {
            "currency": "USD",
            "value": 14.99
        }
    }],
})

if invoice.create():
    print("Invoice[%s] created successfully"%(invoice.id))
else:
    print(invoice.error)
