#!/usr/bin/python

import sys
import sqlite3
from config_stuff import *
import time

class CustomQueries():
    def __init__(self, primary):
        print 'Primary DB: %s' % primary
        self.db = sqlite3.connect(primary)
        
    def how_many_doubles(self):
        placeholder = 0
        
if __name__ == '__main__':
    query_doubles = CustomQueries(sys.argv[1])
    query_doubles.how_many_doubles()
