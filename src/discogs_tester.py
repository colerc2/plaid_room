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
    for upc in upcs:
        upc_checked = False
        while(upc_checked == False):
            try:
                #make sure not to exceed discogs API limit
                time.sleep(discogs.rate_limit)
                print '*'*60

                #few quick checks on UPC, then search for it
                upc = discogs.clean_up_upc(upc)
                if(not discogs.does_this_even_make_sense(upc)):
                    #            print '*'*60
                    print 'This UPC (%s) doesn\'t even make sense.' % upc
                    upc_checked = True
                    continue
                results = discogs.search_for_release(upc)

                #make sure result is "valid"
                if results is None or len(results) == 0:
                    #           print '*'*60
                    print 'No match found on discogs for UPC %s.' % upc
                    upc_checked = True
                    continue
            
                #       print '*'*60
                print '%s results found for UPC %s' % (len(results), upc)
                for result in results:
                    print '-'*50
                    print 'ID: \t\t %s' % result.id
                    print 'Title:\t\t %s' % result.title
                    print 'Year:\t\t %s' % result.year
                    print 'Genres:\t\t %s' % (",".join(result.genres))
                    for artist in result.artists:
                        print 'Artist(s):\t\t%s' % artist.name
                        
                number_found = number_found + 1
                upc_checked = True

            except Exception as e:
                number_of_problems = number_of_problems + 1
                print 'Something bad happened, retrying for UPC %s.' % upc

    print '*'*50
    print '*'*50
    print '%s found out of %s' % (number_found, len(upcs))
    print 'Number of times disconnected: %s' % number_of_problems
