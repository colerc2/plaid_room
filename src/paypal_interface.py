#!/usr/bin/python
import paypalrestsdk
import logging
from paypalrestsdk import Invoice
from config_stuff import *

class PaypalInterface():
    def __init__(self, client_secret_filename):
        f = open(client_secret_filename, 'r')
        
        self.client_id = (f.readline()).strip()
        self.client_secret = (f.readline()).strip()
        print "__%s__" % self.client_id
        print "__%s__" % self.client_secret
        logging.basicConfig(level=logging.INFO)

        paypalrestsdk.configure({
            "mode": "live", # sandbox or live
            "client_id": self.client_id,
            "client_secret": self.client_secret })

    def create_invoice(self, items, misc_items, transaction):
        try:
            #first create array of "items"
            paypal_items = []
            for ix, row in enumerate(items):
                name = row[ARTIST_INDEX] + ' - ' + row[TITLE_INDEX]
                name_truncated = name
                if len(name_truncated) > 59:
                    name_truncated = name_truncated[:59]
                description = name + ' - '+ row[FORMAT_INDEX] + ' - ' + row[UPC_INDEX]
                temp_item = {
                    "name": name_truncated,
                    "description": description,
                    "quantity": 1,
                    "unit_price": {
                        "currency": "USD",
                        "value": row[SOLD_FOR_INDEX]
                    }
                }
                if row[TAXABLE_INDEX]==1:
                    temp_item["tax"] = {
                        "name": "Loveland Tax",
                        "percent": 6.5
                    }
                paypal_items.append(temp_item)
            for ix, row in enumerate(misc_items):
                name = row[MISC_ITEM_INDEX] + ' - ' + row[MISC_DESCRIPTION_INDEX]
                name_truncated = name
                if len(name_truncated) > 59:
                    name_truncated = name_truncated[:59]
                description = row[MISC_TYPE_INDEX] + ' - ' + name + ' - ' + row[UPC_INDEX]
                temp_item = {
                    "name": name_truncated,
                    "description": description,
                    "quantity": 1,
                    "unit_price": {
                        "currency": "USD",
                        "value": row[MISC_SOLD_FOR_INDEX]
                    }
                }
                if row[MISC_TAXABLE_INDEX]==1:
                    temp_item["tax"] = {
                        "name": "Loveland Tax",
                        "percent": 6.5
                    }
                paypal_items.append(temp_item)
                  

            if transaction[TRANS_DISCOUNT_PERCENT_INDEX] > 0.001:
                invoice = Invoice({
                    'merchant_info': {
                        "email": "plaidroomrecords@gmail.com",
                    },
                    "billing_info": [{
                        "email": "plaidroomrecords+invoices@gmail.com"
                    }],
                    "items": paypal_items,
                    "discount": {
                        "percent":format(transaction[TRANS_DISCOUNT_PERCENT_INDEX],'.4f')
                    },
                    "tax_calculated_after_discount": True
                })
            else:
                invoice = Invoice({
                    'merchant_info': {
                        "email": "plaidroomrecords@gmail.com",
                    },
                    "billing_info": [{
                        "email": "plaidroomrecords+invoices@gmail.com"
                    }],
                    "items": paypal_items,
                    "tax_calculated_after_discount": True
                })                
            
            if invoice.create():
                print("Invoice[%s] created successfully"%(invoice.id))
            else:
                print(invoice.error)
        except Exception as e:
            print 'Error making paypal invoice, do it by hand brej: %s' % e
