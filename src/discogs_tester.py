#!/usr/bin/python

import discogs_client
import time
from discogs_interface import DiscogsClient
import csv


if __name__ == "__main__":
    #create discogs object
    discogs = DiscogsClient()
    
    #grab all fat beats catalog
    f = open('txt_files/fat_beats_catalog.txt')
    upcs = f.readlines()
    f.close()

    number_of_problems = 0
    number_found = 0
    #grab info from discogs
    times_checked = 0
    for upc in upcs:
        upc_checked = False
        while(upc_checked == False):
            try:
                if(times_checked > 4):
                    times_checked = 0
                    upc_checked = True
                    continue

                #make sure not to exceed discogs API limit
                time.sleep(discogs.rate_limit)
                print '*'*60

                #few quick checks on UPC, then search for it
                upc = discogs.clean_up_upc(upc)
                if(not discogs.does_this_even_make_sense(upc)):
                    print 'This UPC (%s) doesn\'t even make sense.' % upc
                    upc_checked = True
                    continue
                results = discogs.search_for_release(upc)

                #make sure result is "valid"
                if results is None or len(results) == 0:
                    print 'No match found on discogs for UPC %s.' % upc
                    upc_checked = True
                    continue
            
                #display results in terminal
                print '%s results found for UPC %s' % (len(results), upc)
                for result in results:
                    print '-'*50
                    print 'ID: \t\t %s' % result.id
                    print 'Title:\t\t %s' % result.title
                    print 'Year:\t\t %s' % result.year
                    print 'Genres:\t\t %s' % (", ".join(result.genres))
                    prices = [None] * 3
                    discogs.scrape_price(result.id, prices)
                    if prices[0] != None:
                        print 'Price:\t\t %s, %s, %s' % (prices[0], prices[1], prices[2])
                    for artist in result.artists:
                        discogs.display_artist(artist, '\t')
                    label_list = []
                    for label in result.labels:
                        label_list.append(label.name)
                    print 'Label:\t\t%s' % (", ".join(label_list))
                    print 'Track List:'
                    for t in result.tracklist:
                        print '\t Track %s - %s - %s' % (t.position, t.duration, t.title)

                    print 'Notes:\t\t %s' % (result.notes)
                
                        
                number_found = number_found + 1
                upc_checked = True
                times_checked = 0

            except Exception as e:
                number_of_problems = number_of_problems + 1
                print 'Something bad happened, retrying for UPC %s: %s' % (upc, e)
                times_checked = times_checked + 1
                time.sleep(2)

    print '*'*50
    print '*'*50
    print '%s found out of %s' % (number_found, len(upcs))
    print 'Number of times disconnected: %s' % number_of_problems
