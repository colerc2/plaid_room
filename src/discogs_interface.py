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
        key_file = open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/discogs.key')
        #key_file = open('/Users/bccole1989/Documents/plaid_room_records/add_tabs/plaid_room/discogs.key')
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

    def search_for_artist(self, artist):
        if(self.reconnect_if_necessary()):
            try:
                results = self.client.search(artist, type='artist')
            except Exception as e:
                print 'Failed on the call to discogs client: %s' % e
        else:
            #reconnect failed, oooooOOOOOOOOoooOOOOOOoooooo don't give him the stick
            print 'Some shit is going down, figure out what'
        return results
    
    def search_by_release_number(self, release):
        if(self.reconnect_if_necessary()):
            try:
                results = self.client.release(release)
            except Exception as e:
                print 'Failed on the call to search by release for the discogs client: %s' % e
        else:
            print 'Some shit is going down with your discogs client bro, figure out what'
        return results
    
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

    def process_response(self, results, search_query, upc_needed):
        ii = 0
        rows_to_return = []
        for result in results:
            cols_to_return = ['']*19
            if ii == 20:
                break
                
            worked = [True]*19
            errors = []
            #1 - upc
            try:
                if(upc_needed):
                    cols_to_return[0] = 'PLAID4356783'
                else:
                    cols_to_return[0] = search_query
            except Exception as e:
                worked[0] = False
                errors.append('Error on 0: %s\n' % e)
                
            #2 - artist
            artists_ = []
            try:
                for artist in result.artists:
                    artists_.append(artist.name)
                    cols_to_return[1] = ", ".join(artists_)
            except Exception as e:
                worked[1] = False
                errors.append('Error on 1: %s\n' % e)

            #TODO: this might need some work
            if 'Various' in artists_:
                #TODO: clear table now
                continue
                
            #3 - title
            try:
                cols_to_return[2] = result.title
            except Exception as e:
                worked[2] = False
                errors.append('Error on 2: %s\n' % e)

            #4 - format
            format_ = ''
            try:
                for jj in range(len(result.formats)):
                    if 'qty' in (result.formats[jj]):
                        format_ = format_ + (result.formats[jj])['qty'] + 'x'
                    if 'name' in (result.formats[jj]):
                        format_ = format_ + (result.formats[jj])['name'] + ', '
                    if 'descriptions' in (result.formats[jj]):
                        format_ = format_ +  ", ".join((result.formats[jj])['descriptions'])
                    if jj != (len(result.formats)-1):
                        format_ = format_ + ' + '
                cols_to_return[3] = format_
            except Exception as e:
                #self.print_to_console('Something went wrong when getting the format, fill it in yourself.\n')
                worked[3] = False
                errors.append('Error on 3: %s\n' % e)
            rows_to_return.append(cols_to_return)
            ii = ii + 1
        return rows_to_return

            
    def scrape_price(self, release_id, prices):
        #first, get weird and search for the release id on discogs
        release_url = 'http://www.discogs.com/release/%s' % release_id
        try:
            release_search_url = 'http://www.discogs.com/search/?q=%s&type=release' % str(release_id)
            user_agent = 'Mozilla/36.0 (Macintosh; U; Intel Mac OS X 10_10_1; en-US)'        
            user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_10_1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
            headers = { 'User-Agent' : user_agent }
            print 'requesting search page'
            req = urllib2.Request(release_search_url,None,headers)
            search_term = 'release/%s' % str(release_id)
            print search_term
            response = urllib2.urlopen(req)
            still_together = response.read()
            print '*'*50
            print '*'*50
            for line in still_together.splitlines():
                if search_term in line:
                    quoted = re.findall(r'"([^"]*)"', line)
                    if len(quoted[0]) > 0:
                        release_url = 'http://www.discogs.com%s' % quoted[0]
            print '*'*50
            print release_search_url
            for line_ in response:
                if 'http' in line_:
                    print line_
                line = line_.rstrip()
                
            
        except Exception as e:
            print 'some shit when down while trying to search for the release on discogs (price scraper): %s' % e
        
        #user_agent = 'Mozilla/36.0 (Macintosh; U; Intel Mac OS X 10_10_1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
        user_agent = 'Mozilla/5.0 (Macintosh; U; Intel Mac OS X 10_10_1; en-US) AppleWebKit/534.3 (KHTML, like Gecko) Chrome/6.0.472.63 Safari/534.3'
        #user_agent = 'Mozilla/36.0 (Macintosh; U; Intel Mac OS X 10_10_1; en-US)'        
        headers = { 'User-Agent' : user_agent }
        try:
            print 'requesting page %s' % datetime.datetime.now()
            req = urllib2.Request(release_url, None, headers)
            print 'urlopen(req) %s - %s' % (datetime.datetime.now(), release_url)
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
