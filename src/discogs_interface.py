#!/usr/bin/python

import discogs_client
import urllib2
import time
import csv
import re

class DiscogsClient():
    def __init__(self):
        self.rate_limit = 2
        self.connected = False
        #try to connect
        try:
            self.client = discogs_client.Client('Plaid Room Interface')
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
                self.client = discogs_client.Client('Plaid Room Interface')
                self.connected = True
                print 'Attempted connection was successful'
            except e:
                #TODO: be more specific about errors and maybe display a pop up window here?
                print 'Problem establishing connection with discogs interface: %s' % e
                self.connected = False
        return self.connected

 
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

    def clean_up_upc(self, upc):
        new_upc = re.sub(r"\D", "", upc)
        new_upc = new_upc.strip()
        return new_upc
        
    def does_this_even_make_sense(self, upc):
        #first get rid of anything that isn't a number
        if (len(upc) != 12 and len(upc) != 13):
            return False
        else:
            return True

