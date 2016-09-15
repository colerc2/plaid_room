#!/usr/bin/python
import shopify
from config_stuff import *
import sqlite3
import time


class ShopifyInterface():
    def __init__(self):
        self.db = sqlite3.connect(DB_FILE)
        self.db_cursor = self.db.cursor()
        
        f = open(SHOPIFY_FILE_NAME, 'r')

        self.api_key = (f.readline()).strip()
        self.api_password = (f.readline()).strip()
        
        shop_url = "https://%s:%s@plaid-room-records-2.myshopify.com/admin" % (self.api_key, self.api_password)
        shopify.ShopifyResource.set_site(shop_url)

if __name__ == '__main__':
    shopify_interface = ShopifyInterface()
    orders = shopify.Order.find()
    
    
    #for order in orders:
    #    details = shopify.Order.get(shopify.Order.get_id(order))
    #    print details['shipping_address']

    upcs = set()
    for row in shopify_interface.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ? ORDER BY date_added DESC LIMIT 250', ('New',)):
        if row[UPC_INDEX] in upcs:
            time.sleep(1)
            continue
        new_product = shopify.Product()
        new_product.title = "<b>%s</b><br><i>%s</i>" % (row[ARTIST_INDEX], row[TITLE_INDEX])
        new_product.product_type = "LP"
        new_product.tags = "Format_LP,Pre-Order_09/23/16,Pre-Orders"
        #print new_product.variant
        #variant.barcode = row[UPC_INDEX]
        #variant.price = row[PRICE_INDEX]
        v = shopify.Variant()
        v.price = row[PRICE_INDEX]
        v.barcode = row[UPC_INDEX]
        v.product_id = new_product.id
        #v.save()
        new_product.variants = [v]
        success = new_product.save()
        #new_product.variants = v
        #new_prodcut.price = row[PRICE_INDEX]
        #new_product.variant.price = float(row[PRICE_INDEX])
        time.sleep(1)
        upcs.add(row[UPC_INDEX])
        #print row[ARTIST_INDEX]
        
        
