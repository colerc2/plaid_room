#!/usr/bin/python

import csv
import os
import re

class Catalogs():
    def __init__(self, catalogs_path, distributors):
        self.non_decimal = re.compile(r'[^\d.]+')
        self.catalog = []
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
                #print row
                self.catalog.append([distro, self.filter_non_numeric(row[0]), self.xfloat(self.filter_non_numeric(row[1]))])
        #for row in self.catalog:
            #print row

    def get_catalog(self):
        return self.catalog
    
    def filter_non_numeric(self, str_):
        return self.non_decimal.sub('', str_)
    
    def xfloat(self, f):
        if (f is None) or (f == ''):
            return -1
        return float(f)

