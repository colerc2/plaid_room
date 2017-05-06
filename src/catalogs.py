#!/usr/bin/python

import csv
import os
import re
import sqlite3
from config_stuff import *

class Catalogs():
    def __init__(self, catalogs_path, distributors):
        self.non_decimal = re.compile(r'[^\d.]+')
        self.catalog = []
        self.catalog_dict = {}
        for distro in distributors:
            file_name = catalogs_path + distro + '.csv'
            if not os.path.exists(file_name):
                print '%s does not exist' % distro
                continue
            with open(file_name, 'rb') as f:
                print file_name
                data = [row for row in csv.reader(f.read().splitlines())]
            #print data
            print '%s - %d' % (distro, len(data))
            for row in data:
                print row
                if row[0] == '886976651817':
                    print self.filter_non_numeric(row[0])
                self.catalog.append([distro, self.filter_non_numeric(row[0]), self.xfloat(self.filter_non_numeric(row[1]))])
                #create a dict with a list of tuples as the value, and upc as the key
                upc = self.filter_non_numeric(row[0])
                if upc in self.catalog_dict:
                    if distro in self.catalog_dict[upc]:#probably just skip her
                        placeholder = 0
                    else:#if this distro doesn't exist for this upc, make it exist
                        self.catalog_dict[upc][distro] = self.xfloat(self.filter_non_numeric(row[1]))
                else:
                    self.catalog_dict[upc] = {}
                    self.catalog_dict[upc][distro] = self.xfloat(self.filter_non_numeric(row[1]))
            #now, the painful part
            #for db_row in self.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ?
        #for row in self.catalog:
            #print row

    def get_catalog(self):
        return self.catalog

    def add_current_db(self, db):
        db_cursor = db.cursor()
        for row in db_cursor.execute('SELECT * FROM inventory WHERE new_used = ?', ('New',)):
            upc = row[UPC_INDEX]
            distro = row[DISTRIBUTOR_INDEX]
            price = row[PRICE_PAID_INDEX]
            if upc in self.catalog_dict:
                if distro in self.catalog_dict[upc]:#probably just skip her
                    placeholder = 0
                else:#if this distro doesn't exist for this upc, make it exist
                    self.catalog_dict[upc][distro] = price
            else:
                self.catalog_dict[upc] = {}
                self.catalog_dict[upc][distro] = price
        for row in db_cursor.execute('SELECT * FROM sold_inventory WHERE new_used = ?', ('New',)):
            upc = row[UPC_INDEX]
            distro = row[DISTRIBUTOR_INDEX]
            price = row[PRICE_PAID_INDEX]
            if upc in self.catalog_dict:
                if distro in self.catalog_dict[upc]:#probably just skip her
                    placeholder = 0
                else:#if this distro doesn't exist for this upc, make it exist
                    self.catalog_dict[upc][distro] = price
            else:
                self.catalog_dict[upc] = {}
                self.catalog_dict[upc][distro] = price
        return True
                
    def get_catalog_dict(self):
        return self.catalog_dict
    
    def filter_non_numeric(self, str_):
        return self.non_decimal.sub('', str_)
    
    def xfloat(self, f):
        if (f is None) or (f == ''):
            return -1
        return float(f)

