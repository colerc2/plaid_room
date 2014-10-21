#!/usr/bin/python

import discogs_client
import urllib2
import time
import csv
import urlparse
import re
import datetime

class DiscogsClient():
    def __init__(self):
        #get info from .key file
        key_file = open('/Users/bccole1989/Documents/plaid_room_records/plaid_room/discogs.key')
        self.consumer_key = key_file.readline().rstrip('\n')
        self.consumer_secret = key_file.readline().rstrip('\n')
        self.access_token = key_file.readline().rstrip('\n')
        self.access_secret = key_file.readline().rstrip('\n')
        #request_token_url = key_file.readline()
        #authorize_url = key_file.readline()
        #authorize_token = key_file.readline()

        #user_agent = 'plaid_room_records_interface/1.0'
        #consumer = oauth.Consumer(consumer_key, consumer_secret)
        #client = oauth.Client(consumer)
        #resp, content = client.request(request_token_url, 'POST', headers={'User-Agent': user_agent})
        #if resp['status'] != '200':
        #    raise Exception('Invalid response{0}.'.format(resp['status
        
        self.rate_limit = 1.1
        self.connected = False
        #try to connect
        try:
            self.client = discogs_client.Client('plaid_room_records_interface/1.0', self.consumer_key, self.consumer_secret, self.access_token, self.access_secret)
            #self.client.set_consumer_key(consumer_key, consumer_secret)
            #self.client.get_authorize_url()
            #self.client.get_access_token('ZwNlCmaWYq')
            #print self.client.get_access_token()
            self.connected = True
        except Exception as e:
            #TODO: be more specific about errors and maybe display a pop up window here?
            print 'Problem establishing connection with discogs interface: %s' % e

    def reconnect_if_necessary(self):
        if(not self.connected):
            #first, make sure we aren't exceeding discogs API's rate limit
            time.sleep(self.rate_limit)
            print 'Attempting to reconnect to discogs API'
            try:
                self.client = discogs_client.Client('plaid_room_records_interface/1.0', self.consumer_key, self.consumer_secret, self.access_token, self.access_secret)
                self.connected = True
                print 'Attempted connection was successful'
            except e:
                #TODO: be more specific about errors and maybe display a pop up window here?
                print 'Problem establishing connection with discogs interface: %s' % e
                self.connected = False
        return self.connected

 
        #If connected, search for release
    def search_for_release(self, upc):
        if(self.reconnect_if_necessary()):
            try:
                results = self.client.search(upc, type='release')
            except Exception as e:
                print 'Failed on the call to discogs client: %s' % e
        else:
            #reconnect failed, throw some error breh
            print 'Some shit is going down, figure out what'
        return results

        #Get rid of weird chars and white space
    def clean_up_upc(self, upc):
        new_upc = re.sub(r"\D", "", upc)
        new_upc = new_upc.strip()
        return new_upc
        
        #Make sure it's a valid length for UPC/EAN
    def does_this_even_make_sense(self, upc):
        #first get rid of anything that isn't a number
        if (len(upc) != 12 and len(upc) != 13):
            return False
        else:
            return True
            
    def scrape_price(self, release_id, prices):
        release_url = 'http://www.discogs.com/release/%s' % release_id
        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_6_4; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
        headers = { 'User-Agent' : user_agent }
        try:
            print 'requesting page %s' % datetime.datetime.now()
            req = urllib2.Request(release_url, None, headers)
            print 'urlopen(req) %s' % datetime.datetime.now()
            response = urllib2.urlopen(req)
            grab_low = False
            grab_mid = False
            grab_high = False
            print 'compiling %s' % datetime.datetime.now()
            non_decimal = re.compile(r'[^\d.]+')
            print 'before for %s' % datetime.datetime.now()
            for line_ in response:
                line = line_.rstrip()
                if(grab_low):
                    grab_low = False
                    prices[0] = (line.strip()).replace("$", "")
                    prices[0] = non_decimal.sub('', prices[0])
                if(grab_mid):
                    grab_mid = False
                    prices[1] = (line.strip()).replace("$", "")
                    prices[1] = non_decimal.sub('', prices[1])
                if(grab_high):
                    grab_high = False
                    prices[2] = (line.strip()).replace("$", "")
                    prices[2] = non_decimal.sub('', prices[2])
                    break
                if(line.find('Lowest') != -1):
                    grab_low = True
                if(line.find('Median') != -1):
                    grab_mid = True
                if(line.find('Highest') != -1):
                    grab_high = True
        except Exception as e:
            print 'Some error occured while trying to scrape the price from %s: %s' % (release_url, e)
    
    #recursive (or naaa?) function to display artists
    def display_artist(self, artist, tabs):
        #print artist.decode('utf-8')
        print 'Artist:%s\t %s' % (tabs,artist.name)
        #hard coded work around uh gross oh well
        if artist.name == 'Various':
            return
        if artist.real_name is not None:
            print 'Real Name:%s%s' % (tabs,artist.real_name)
        if artist.profile is not None:
            print 'Profile:%s%s' % (tabs,artist.profile)
        if artist.name_variations is not None:
            print 'Variations:%s%s' % (tabs,(", ".join(artist.name_variations)))
        #print 'Variations:%s%s' % (tabs,artist.name_variations)
        #print artist.name_variations
        if artist.aliases is not None:
            alias_list = []
            for alias in artist.aliases:
                alias_list.append(alias.name)
            print 'Aliases: %s%s' % (tabs, (", ".join(alias_list)))
        return
