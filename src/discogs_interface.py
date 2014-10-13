#!/usr/bin/python

import discogs_client
import urllib2
import time
import csv

class DiscogsClient():
    def __init__(self):
        self.rate_limit = 1
        self.connected = False
        #try to connect
        try:
            self.client = discogs_client.Client('Plaid Room Interface')
            self.connected = True
            break
        except e:
            #TODO: be more specific about errors and maybe display a pop up window here?
            print 'Problem establishing connection with discogs interface: %s' % e
    
    def search_for_release(self, upc):
        if(reconnect_if_necessary()):
            
        else:
            #reconnect failed, throw some error breh

    def reconnect_if_necessary(self):
        if(!self.connected):
            #first, make sure we aren't exceeding discogs API's rate limit
            time.sleep(self.rate_limit)
            try:
                self.client = discogs_client.Client('Plaid Room Interface')
                self.connected = True
                break
            except e:
                #TODO: be more specific about errors and maybe display a pop up window here?
                print 'Problem establishing connection with discogs interface: %s' % e
                self.connected = False
        return self.connected
