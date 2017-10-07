#!/usr/bin/python
import time
import selenium
from selenium import webdriver
import os
from selenium.webdriver.common.keys import Keys
import shopify
from config_stuff import *

COLEMINE = 0
PLAID_ROOM = 1

class MediaMail():
    def __init__(self):
        self.driver = None
        self.reset_shopify_connection(COLEMINE)
        self.reset_paypal_browser()
        self.api_key = 0
        self.api_password = 0

        
    def reset_paypal_browser(self):
        #chromedriver = "/Users/plaidroomrecords/Downloads/chromedriver"
        chromedriver = "/usr/local/bin/chromedriver"
        os.environ["webdriver.chrome.driver"] = chromedriver
        if self.driver is not None:
            self.driver.close()
        self.driver = webdriver.Chrome(chromedriver)

        self.driver.get("https://www.paypal.com/signin?country.x=US&locale.x=en_US")

        f = open(PAYPAL_LOGIN_NAME)

        email = (f.readline()).strip()
        password = (f.readline()).strip()
        try:
            email_line = self.driver.find_element_by_name('login_email')
            email_line.send_keys(email)
            password_line = self.driver.find_element_by_name('login_password')
            password_line.send_keys(password)
            login_button = self.driver.find_element_by_name('btnLogin')
            login_button.click()
            time.sleep(7)
        except Exception as e:
            print 'fuck this new paypal shit'
        
    def reset_shopify_connection(self, clmn_or_prr):
        if clmn_or_prr == COLEMINE:
            #this needs to be changed to the colemine shopify once it's actually a thing
            #f = open(SHOPIFY_PLAID_ROOM_NAME)
            f = open(SHOPIFY_COLEMINE_NAME)
        else: #plaid room
            f = open(SHOPIFY_PLAID_ROOM_NAME)

        self.api_key = (f.readline()).strip()
        self.api_password = (f.readline()).strip()

        print self.api_key
        print self.api_password

        if clmn_or_prr == COLEMINE:
            shop_url = "https://%s:%s@colemine-records.myshopify.com/admin" % (self.api_key, self.api_password)
        else: #plaid room
            shop_url = "https://%s:%s@plaid-room-records-2.myshopify.com/admin" % (self.api_key, self.api_password)

        print shop_url
        shopify.ShopifyResource.set_site(shop_url)

    def get_shopify_order(self, order_number):
        shopify_order = shopify.Order.find(order_number)
        print 'found order'
        return shopify_order

    def send_to_paypal(self, order):
        self.driver.get("https://www.paypal.com/shiplabel/create/")
        #self.driver.switchTo().window(self.driver.getWindowHandle())
        time.sleep(3)
        addressee_name = self.driver.find_element_by_name('addresseeName')
        addressee_name.send_keys(order.shipping_address.attributes["name"])
        
        street1 = self.driver.find_element_by_name('street1')
        street1.send_keys(order.shipping_address.attributes["address1"])

        street2 = self.driver.find_element_by_name('street2')
        if order.shipping_address.attributes["address2"] is not None:
            print 'something here bossman'
            street2.send_keys(order.shipping_address.attributes["address2"])

        city = self.driver.find_element_by_name('city')
        city.send_keys(order.shipping_address.attributes["city"])

        zip_postal = self.driver.find_element_by_name('postalCode')
        zip_postal.send_keys(order.shipping_address.attributes["zip"])

        state = self.driver.find_element_by_name('stateOrProvince')
        state.click()
        state.send_keys(order.shipping_address.attributes["province"])
        state.send_keys('\t\t')

        email = self.driver.find_element_by_name('email')
        email.send_keys(order.email)

        pay_button = self.driver.find_element_by_name('SaveToAddress')
        pay_button.click()

        service_type = self.driver.find_element_by_name('serviceType')
        #service_type.click()
        service_type.send_keys("m\t")

        package_type = self.driver.find_element_by_name('packageType')
        #package_type.click()
        package_type.send_keys("p\t")

        full_address = '%s\n%s\n%s, %s\n%s' % (order.shipping_address.attributes["name"], order.shipping_address.attributes["address1"], order.shipping_address.attributes["city"], order.shipping_address.attributes["province"], order.shipping_address.attributes["country"]) 
        
        return full_address
        
        #email = self.driver.find_element_by_name('
        

    
        
#chromedriver = "/Users/plaidroomrecords/Downloads/chromedriver"
#os.environ["webdriver.chrome.driver"] = chromedriver
#driver = webdriver.Chrome(chromedriver)
#driver.get("http://stackoverflow.com")
#driver.get("http://www.paypal.com/shiplabel/create/")
#driver.get("https://www.paypal.com/signin?country.x=US&locale.x=en_US")

#address = driver.find_element_by_name("addresseename")
#address.send_keys("Terry Faggot Cole")

#email_line = driver.find_element_by_name('login_email')
#email_line.send_keys("")
#password_line = driver.find_element_by_name('login_password')
#password_line.send_keys("")
#login_button = driver.find_element_by_name('btnLogin')
#login_button.click()
#time.sleep(10)
#print 'done sleeping'
#driver.get("https://www.paypal.com/shiplabel/create/")
#time.sleep(5)
#addressee_name = driver.find_element_by_name('addresseeName')
#addressee_name.send_keys('Tracy Cole')

#street1 = driver.find_element_by_name('street1')
#addressee_name.send_keys('4401 Graydon Drive')

#submit_button.click()

#driver.quit()

#chromedriver = 'C:\\chromedriver.exe'
#browser = webdriver.Chrome(chromedriver)
#browser = webdriver.Firefox()

#browser.get('http://www.google.com')
#browser.get('http://www.paypal.com/shiplabel/create/')
#print 'got website'

#username = selenium.find_element_by_id("addresseename")
#password = selenium.find_element_by_id("password")
#print 'found addresseename'

#username.send_keys("I love Jazz")
#print 'sent keys'
#password.send_keys("Pa55worD")
