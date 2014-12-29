import paypalrestsdk
import logging
from paypalrestsdk import Invoice

logging.basicConfig(level=logging.INFO)

paypalrestsdk.configure({
  "mode": "live", # sandbox or live
    "client_id": "",
  "client_secret": "" })

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
