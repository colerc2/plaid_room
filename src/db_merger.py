#!/usr/bin/python

import sys
import sqlite3
from barcode_printer import BarcodePrinter
from config_stuff import *
import time

class DBMerger():
    def __init__(self, primary, secondary):
        print 'Primary DB: %s' % primary
        print 'Secondary DB: %s' % secondary
        self.primary = sqlite3.connect(primary)
        self.secondary = sqlite3.connect(secondary)
        self.primary_cursor = self.primary.cursor()
        self.secondary_cursor = self.secondary.cursor()


    def merge_them(self):
        #print 'Primary last row id: %i' % self.primary_cursor.lastrowid
        for ix, row in enumerate(self.secondary_cursor.execute('SELECT * FROM inventory ORDER BY date_added ASC')):
            without_key = list(row[:-1])
            if 'PLAID' in without_key[UPC_INDEX]:
                without_key[UPC_INDEX] = 'BLANK'
                without_key[RESERVED_ONE_INDEX] = 'merged from laptop DB 2.12.15'
            try:
                self.primary_cursor.execute('INSERT INTO inventory (upc, artist, title, format, price, price_paid, new_used, distributor, label, genre, year, date_added, discogs_release_number, real_name, profile, variations, aliases, track_list, notes, taxable, reserved_one, reserved_two) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tuple(without_key))
                self.primary.commit()
            except Exception as e:
                print 'problem adding item to inventory: %s' % e
                print row
                continue
            #check if barcode needs updated
            code = without_key[UPC_INDEX]
            if code == 'BLANK' or code == '':
                last_row_id = self.primary_cursor.lastrowid
                code = 'PLAID%06d' % last_row_id
                self.primary_cursor.execute('UPDATE inventory SET upc = ? WHERE id = ?', (code, last_row_id))
                self.primary.commit()
        #print 'Primary last row id (after changes): %i' % self.primary_cursor.lastrowid


    def tester(self):
        count = 0
        #print 'Primary last row id: %i' % self.primary_cursor.lastrowid
        for ix, row in enumerate(self.primary_cursor.execute('SELECT * FROM inventory ORDER BY date_added ASC')):
            count += 1
        print 'Size of primary: %i' % count
        count = 0
        for ix, row in enumerate(self.secondary_cursor.execute('SELECT * FROM inventory ORDER BY date_added ASC')):
            print row[ARTIST_INDEX]
            #time.sleep(1)
            count += 1
        print 'Size of secondary: %i' % count


if __name__ == '__main__':
    if len(sys.argv) != 3:
        print 'Not enough command line args'
        sys.exit()
    db_merge = DBMerger(sys.argv[1], sys.argv[2])
    #db_merge.tester()
    db_merge.merge_them()
        
