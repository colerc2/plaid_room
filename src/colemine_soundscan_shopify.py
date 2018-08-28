import time
import selenium
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import shopify
from config_stuff import *
import csv

COLEMINE = 0
PLAID_ROOM = 1

class ColemineSoundscan():
    def __init__(self):
        self.driver = None
        self.reset_shopify_connection(COLEMINE)
        self.api_key = 0
        self.api_password = 0

        
    def reset_paypal_browser(self):
        #chromedriver = "/Users/plaidroomrecords/Downloads/chromedriver"
        #chromedriver = "/usr/local/bin/chromedriver"
        #os.environ["webdriver.chrome.driver"] = chromedriver
        #if self.driver is not None:
        #    self.driver.close()
        #self.driver = webdriver.Chrome(chromedriver)

        #self.driver.get("https://www.paypal.com/signin?country.x=US&locale.x=en_US")

        #f = open(PAYPAL_LOGIN_NAME)

        #email = (f.readline()).strip()
        #password = (f.readline()).strip()
        
        #email_line = self.driver.find_element_by_name('login_email')
        #email_line.send_keys(email)
        #password_line = self.driver.find_element_by_name('login_password')
        #password_line.send_keys(password)
        #login_button = self.driver.find_element_by_name('btnLogin')
        #login_button.click()
        #time.sleep(7)
        placeholder = 0
        
        
    def reset_shopify_connection(self, clmn_or_prr):
        if clmn_or_prr == COLEMINE:
            #this needs to be changed to the colemine shopify once it's actually a thing
            #f = open(SHOPIFY_PLAID_ROOM_NAME)
            f = open(SHOPIFY_COLEMINE_NAME)
            #f = open(SHOPIFY_DLO3_NAME)
        else: #plaid room
            f = open(SHOPIFY_PLAID_ROOM_NAME)

        self.api_key = (f.readline()).strip()
        self.api_password = (f.readline()).strip()

        print self.api_key
        print self.api_password

        if clmn_or_prr == COLEMINE:
            shop_url = "https://%s:%s@colemine-records.myshopify.com/admin" % (self.api_key, self.api_password)
            #shop_url = "https://%s:%s@delvon-lamarr-organ-trio.myshopify.com/admin" % (self.api_key, self.api_password)
        else: #plaid room
            shop_url = "https://%s:%s@plaid-room-records-2.myshopify.com/admin" % (self.api_key, self.api_password)

        print shop_url
        shopify.ShopifyResource.set_site(shop_url)

    def get_shopify_order(self, order_number):
        shopify_order = shopify.Order.find(order_number)
        print 'found order'
        return shopify_order

    def generate_list_of_zips(self):
        zips = []
        for page in range(250):
            orders = shopify.Order.find(page=(page+1))
            time.sleep(0.75)
            if len(orders) == 0:
                break
            for order in orders:
                try:
                    if order.shipping_address.country_code == 'US':
                        zip = order.shipping_address.zip[:5]
                        if zip.isdigit() and len(zip) == 5:
                            zips.append(zip)
                except Exception as e:
                    print 'ERROR: %s' % e
        return zips
                    
    
    def get_list_of_orders_for_pre_orders(self, start_date, end_date, pre_orders):
        orders_to_return = []
        for page in range(250):
            print 'page %s' % page
            orders = shopify.Order.find(page=(page+1),created_at_min=start_date,created_at_max=end_date)
            print start_date
            print end_date
            time.sleep(0.75)
            print len(orders)
            if len(orders) == 0:
                break
            for order in orders:
                print order
                try:
                    order_id = 0
                    order_id = order.id
                    for line in order.line_items:
                        print line
                        if line.sku in pre_orders:
                            orders_to_return.append(order)
                            break
                except Exception as e:
                    print 'ERROR: %s' % e
        return orders_to_return

    def get_list_of_orders_for_back_dating(self):
        orders_to_return = []
        soundscan_lines = []
        total_dict = dict()
        for page in range(250):
            orders = shopify.Order.find(page=(page+1))
            time.sleep(0.9)
            #read in mapping
            with open(COLEMINE_MAPPER, 'rb') as f:
                reader = csv.reader(f)
                mapper = list(reader)
            mapper_dict = dict()
            for line in mapper:
                mapper_dict[line[0]] = line[1]
            if len(orders) == 0:
                break
            for order in orders:
                for line in order.line_items:#for each line
                    if line.vendor in mapper_dict:#if it's an actual release
                        try:
                            if order.shipping_address.country_code == 'US':
                                zip_ = order.shipping_address.zip[:5]
                                if zip_.isdigit() and len(zip_) == 5:
                                    for ii in range(int(line.quantity)):
                                        soundscan_lines.append('M3%013d%05dS' % (int(mapper_dict[line.vendor]), int(zip_)))
                                        if line.vendor in total_dict:
                                            total_dict[line.vendor] += 1
                                        else:
                                            total_dict[line.vendor] = 1
                        except Exception as e:
                            print 'ERROR: %s' % e
        for line in soundscan_lines:
            print line
        print '%s%05d%07d' % ('94', int(len(soundscan_lines)), int(len(soundscan_lines)))
        
        for key, value in total_dict.iteritems():
            print '%s - %s' % (key, value)
                                    
                        
        
    def get_list_of_orders_from_beginning(self, start_date, end_date, pre_orders):
        orders_to_return = []
        total_counts = dict()
        for page in range(250):
            print 'page %s' % page
            print start_date
            print end_date
            orders = shopify.Order.find(page=(page+1),created_at_min=start_date,created_at_max=end_date)
#            orders = shopify.Order.find(created_at_min=start_date,created_at_max=end_date)
            print 'after shopify call'
            time.sleep(0.5)
            print len(orders)
            if len(orders) == 0:
                break
            for order in orders:
                orders_to_return.append(order)
                print order
                try:
                    order_id = 0
                    order_id = order.id
                    for line in order.line_items:
                        print 'going through line_items'
                        print line.vendor
                        print line.sku
                        print pre_orders
                        if line.sku in pre_orders:
                            #print '\n\nKICKING THIS ONE BACK\n\n'
                            #ignore any SKU that is a pre-order, those will be counted in another piece of code
                            continue
                        if line.vendor in total_counts:
                            total_counts[line.vendor] += line.quantity
                        else:
                            total_counts[line.vendor] = line.quantity
                        #for key, value in total_counts.iteritems():
                        #    print '%s\t%s' % (key,value)
                except Exception as e:
                    print 'ERROR: %s' % e
        for key, value in total_counts.iteritems():
            print '%s\t%s' % (key,value)
        #for item in orders_to_return:
        #    print item
        return orders_to_return
                            
        
