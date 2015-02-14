#!/usr/bin/python

import sys
import sqlite3
from barcode_printer import BarcodePrinter
from config_stuff import *
import time

class MassBarcodePrinter():
        def __init__(self, db, start, stop):
		self.db = sqlite3.connect(db)
		self.db_cursor = self.db.cursor()
		self.start = start
		self.stop = stop
		self.barcode_printer = BarcodePrinter()

	def print_em(self):
		for key in range(int(self.start), int(self.stop)):
			for row in self.db_cursor.execute('SELECT * FROM inventory where id = ?', (key,)):
                                print 'now printing: %s, %i' %  (row[ARTIST_INDEX],key)
				self.barcode_printer.print_barcode(row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[PRICE_INDEX])
				break
			time.sleep(5)


if __name__ == '__main__':
	if len(sys.argv) != 4:
		print 'Not enough command line args'
		sys.exit()
	mass_print = MassBarcodePrinter(sys.argv[1], sys.argv[2], sys.argv[3])
	mass_print.print_em()
