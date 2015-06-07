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

    def create_wholesale_invoice(self, items, account, shipping):
        try:
            #first create array of items
            paypal_items = []
            for ix, row in enumerate(items):
                name = ('CLMN-%s' % row[COLE_INV_CATALOG_INDEX])
                description = row[COLE_INV_ARTIST_INDEX] + ' - ' + row[COLE_INV_TITLE_INDEX]
                temp_item = {
                    "name": name,
                    "description": description,
                    "quantity": row[COLE_INV_QTY_SHIPPED_INDEX],
                    "unit_price": {
                        "currency": "USD",
                        "value": format(row[COLE_INV_WHOLESALE_INDEX],'.2f')
                    }
                }
                #temp_item["tax"] = {
                    #"name": "WHOLESALE",
                    #"percent": 0.0
                    #}
                paypal_items.append(temp_item)
            temp_invoice = {
                'merchant_info': {
                    "email": "plaidroomrecords@gmail.com",
                    "first_name": "Terry",
                    "last_name": "Cole",
                    "address": {
                        "line1": "120 Karl Brown Way",
                        "city": "Loveland",
                        "country_code": "US",
                        "postal_code": "45140",
                        "state": "OH",
                        "phone": {
                            "country_code": "1",
                            "national_number" : "5132924219"
                        },      #"phone": "5132924219"
                    },
                    "business_name": "Plaid Room Records / Colemine Records",
                    "website": "http://www.plaidroomrecords.com"
                },
                "billing_info": [{
                    "email": account[COLE_EMAIL_INDEX],
                    #"first_name": account[COLE_BILLING_NAME_INDEX],
                    "business_name": account[COLE_BUSINESS_NAME_INDEX],
                    "address": {
                        "line1": account[COLE_BILLING_LINE_ONE_INDEX],
                        "city": account[COLE_BILLING_CITY_INDEX],
                        "country_code": "US",
                        "postal_code": account[COLE_BILLING_ZIP_INDEX],
                        "state": account[COLE_BILLING_STATE_INDEX],
                        "phone": {
                            "country_code": "1",
                            "national_number" : account[COLE_PHONE_INDEX]
                        },
                    },
                }],
                "shipping_info": {
                    #"first_name": account[COLE_SHIPPING_NAME_INDEX],
                    "business_name": account[COLE_BUSINESS_NAME_INDEX],
                    "address": {
                        "line1": account[COLE_SHIPPING_LINE_ONE_INDEX],
                        "city": account[COLE_SHIPPING_CITY_INDEX],
                        "country_code": "US",
                        "postal_code": account[COLE_SHIPPING_ZIP_INDEX],
                        "state": account[COLE_SHIPPING_STATE_INDEX],
                        "phone": {
                            "country_code": "1",
                            "national_number" : account[COLE_PHONE_INDEX]
                        },
                    },
                },
                "logo_url" : "https://www.paypal.com/us/cgi-bin/?cmd=_stream-logo-image&id=36163477",
                "items": paypal_items,
                "tax_calculated_after_discount": True#,
                #"merchant_memo": ('transaction primary key: %d' % transaction[TRANS_ID_INDEX])
            }
            if shipping > 0.001:
                temp_invoice["shipping_cost"] = {
                    "amount": {
                        "currency": "USD",
                        "value": format(shipping,'.2f')
                    }
                }
            invoice = Invoice(temp_invoice)
            if invoice.create():
                print("Invoice[%s] created successfully"%(invoice.id))
            else:
                print(invoice.error)

            if invoice.send(): # return True or False
                print("Invoice[%s] send successfully" % (invoice.id))
            else:
                print(invoice.error)
        except Exception as e:
            print 'Error making paypal invoice, do it by hand brej: %s' % e
            
                

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
                        "value": format(row[SOLD_FOR_INDEX],'.2f')
                    }
                }
                if row[TAXABLE_INDEX]==1:
                    temp_item["tax"] = {
                        "name": "Loveland Tax",
                        "percent": LOVELAND_TAX_RATE
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
                        "value": format(row[MISC_SOLD_FOR_INDEX],'.2f')
                    }
                }
                if row[MISC_TAXABLE_INDEX]==1:
                    temp_item["tax"] = {
                        "name": "Loveland Tax",
                        "percent": LOVELAND_TAX_RATE
                    }
                paypal_items.append(temp_item)
                  
            temp_invoice = {
                'merchant_info': {
                    "email": "plaidroomrecords@gmail.com",
                },
                "billing_info": [{
                    "email": "plaidroomrecords+invoices@gmail.com"
                }],
                "items": paypal_items,
                "tax_calculated_after_discount": True,
                "merchant_memo": ('transaction primary key: %d' % transaction[TRANS_ID_INDEX])
            }
                
            if transaction[TRANS_DISCOUNT_PERCENT_INDEX] > 0.001:
                temp_invoice["discount"] = {
                    "percent": format(transaction[TRANS_DISCOUNT_PERCENT_INDEX],'.4f')
                }
            if transaction[TRANS_SHIPPING_INDEX] > 0.001:
                temp_invoice["shipping_cost"] = {
                    "amount": {
                        "currency": "USD",
                        "value": format(transaction[TRANS_SHIPPING_INDEX],'.2f')
                    }
                }
            invoice = Invoice(temp_invoice)
            if invoice.create():
                print("Invoice[%s] created successfully"%(invoice.id))
            else:
                print(invoice.error)

            if invoice.send(): # return True or False
                print("Invoice[%s] send successfully" % (invoice.id))
            else:
                print(invoice.error)
        except Exception as e:
            print 'Error making paypal invoice, do it by hand brej: %s' % e
