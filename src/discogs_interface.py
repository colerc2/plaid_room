#!/usr/bin/python

import discogs_client
import urllib2
import time
import csv

class DiscogsClient():
    def __init__(self):
        self.connected = False
        #try to connect
        try:
            self.client = discogs_client.Client('Plaid Room Interface')
            self.connected = True
            break
        except:
            #TODO: be more specific about errors and maybe display a pop up window here?
            print 'Problem establishing connection with discogs interface'
    
    def search_for_release(self, upc):
        reconnect_if_necessary()

    def reconnect_if_necessary(self):
        if(self.connected):
            return
        else:
            
