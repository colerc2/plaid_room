#!/usr/bin/python

import csv
import sys

pos= open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/for_cam.csv').read().splitlines()

total_number_pos = len(pos)
number_over_fifteen_hundred = 0
average_amount_of_big_dogs = 0
for item in pos:
    item = item.split(',')
    if float(item[1]) > 1500:
        number_over_fifteen_hundred += 1
        average_amount_of_big_dogs += float(item[1])
average_amount_of_big_dogs = average_amount_of_big_dogs / number_over_fifteen_hundred
print 'Total number of POs: %s' % str(total_number_pos)
print 'Number of POs over 1500: %s' % str(number_over_fifteen_hundred)
print 'Average of big dogs: %s' % str(average_amount_of_big_dogs)
