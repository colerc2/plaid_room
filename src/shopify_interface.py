#!/usr/bin/python
import shopify
from config_stuff import *
import sqlite3
import time
import datetime
from pprint import pprint

class ShopifyInterface():
    def __init__(self):
        #self.db = sqlite3.connect(DB_FILE)
        #self.db_cursor = self.db.cursor()
        
        f = open(SHOPIFY_PLAID_ROOM_NAME, 'r')

        self.api_key = (f.readline()).strip()
        self.api_password = (f.readline()).strip()
        
        shop_url = "https://%s:%s@plaid-room-records-2.myshopify.com/admin" % (self.api_key, self.api_password)
        shopify.ShopifyResource.set_site(shop_url)


    def get_item(self, id):
        product = shopify.Product.find(id)
        return product

    #this function takes an item formatted from the pre-order table in the DB, and updates or creates it on shopify,
    #and also returns the shopify product when it's done
    def create_or_update_item(self, row):#aka sync
        if row[PRE_SHOPIFY_ID] is None or row[PRE_SHOPIFY_ID] == '':#if it doesn't exist
            try:
                new_product = shopify.Product()
                street_date_formatted_for_america = datetime.datetime.strptime(row[PRE_STREET_DATE], "%Y-%m-%d")
                street_date_formatted_for_america = street_date_formatted_for_america.strftime("%m/%d/%Y")
                new_product.title = "<b>%s</b><br><i>%s</i><br>Release Date : %s" % (row[PRE_ARTIST], row[PRE_TITLE], street_date_formatted_for_america)
                new_product.product_type = "LP"#default for now, might change later
                new_product.tags = row[PRE_SHOPIFY_TAGS]
                new_product.body_html = row[PRE_SHOPIFY_DESC]
                pprint (vars(new_product))
                if row[PRE_ACTIVE] == 0:
                    new_product.published_at = None
                new_product.published_scope = 'web'
                v = shopify.Variant()
                v.price = row[PRE_SALE_PRICE]
                v.barcode = row[PRE_UPC]
                v.product_id = new_product.id
                new_product.variants = [v]
                success = new_product.save()
                pprint (vars(new_product))
                print
            except Exception as e:
                print 'error in the shopify:create_or_update_item func: %s' % e
                return None
            if success == False:
                return None
            time.sleep(0.5)
            return new_product
            
            
            
        
        
#if __name__ == '__main__':
#    shopify_interface = ShopifyInterface()
#    orders = shopify.Order.find()
    
    
    #for order in orders:
    #    details = shopify.Order.get(shopify.Order.get_id(order))
    #    print details['shipping_address']

#    upcs = set()
#    for row in shopify_interface.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ? ORDER BY date_added DESC LIMIT 250', ('New',)):
#        if row[UPC_INDEX] in upcs:
#            time.sleep(1)
#            continue
#        new_product = shopify.Product()
#        new_product.title = "<b>%s</b><br><i>%s</i>" % (row[ARTIST_INDEX], row[TITLE_INDEX])
#        new_product.product_type = "LP"
#        new_product.tags = "Format_LP,Pre-Order_09/23/16,Pre-Orders"
#        v = shopify.Variant()
#        v.price = row[PRICE_INDEX]
#        v.barcode = row[UPC_INDEX]
#        v.product_id = new_product.id
#        new_product.variants = [v]
#        success = new_product.save()
#        time.sleep(1)
#        upcs.add(row[UPC_INDEX])
        
        
