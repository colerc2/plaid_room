#!/usr/bin/python

import sys
import sqlite3
import time
from config_stuff import *
import datetime
import locale
import csv
import discogs_client
from discogs_interface import DiscogsClient
import math
from colemine_soundscan_shopify import ColemineSoundscan
from shopify_interface import ShopifyInterface
import random
import re
from receipt_printer import ReceiptPrinter

class Util():
	def __init__(self, primary='real_inventory_copy.db'):
		print 'Primary DB: %s' % primary
		self.db = sqlite3.connect(primary)
		self.db_cursor = self.db.cursor()
		locale.setlocale( locale.LC_ALL, '')
		self.discogs = DiscogsClient()#discogs api
                #shopify connect
                self.shopify_interface = ShopifyInterface()
                self.receipt_printer = ReceiptPrinter(TEMP_RECEIPT_FILE_NAME)

	def import_alliance_order(self):
		order = open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/config/PLS89388384.csv').read().splitlines()
		upc_column = 2
		qty_column = 7
		price_column = 9
		for item in order:
			print item
			print

        def add_new_release_tag(self):
                list_of_stuff_to_update = []
                count = 0
                for row in self.db_cursor.execute('SELECT * FROM online_inventory ORDER BY date_added DESC'):
                        count += 1
                        if count > 67:
                                break
                        if ',New Release' not in row[ONLINE_SHOPIFY_TAGS]:
                                print row[ONLINE_ARTIST]
                                tags = row[ONLINE_SHOPIFY_TAGS]
                                tags = tags + ',New Release'
                                #tags = tags + ',Audiophile'
                                list_of_stuff_to_update.append((0,tags,row[ONLINE_ID]))
                for row in list_of_stuff_to_update:
                        self.db_cursor.execute('UPDATE online_inventory SET sync = ? WHERE id = ?', (row[0], row[2]))
                        self.db_cursor.execute('UPDATE online_inventory SET shopify_tags = ? WHERE id = ?', (row[1], row[2]))
                self.db.commit()

                        
        def remove_older_new_releases_from_site(self):
                list_of_stuff_to_update = []
                count = 0
                for row in self.db_cursor.execute('SELECT * FROM online_inventory ORDER BY date_added DESC'):
                        if ',New Release' in row[ONLINE_SHOPIFY_TAGS]:
                                count = count + 1
                                if count > 125:
                                        print row[ONLINE_ARTIST]
                                        tags = row[ONLINE_SHOPIFY_TAGS]
                                        tags = tags.replace(',New Release','')
                                        list_of_stuff_to_update.append((0, tags, row[ONLINE_ID]))
                for row in list_of_stuff_to_update:
                        self.db_cursor.execute('UPDATE online_inventory SET sync = ? WHERE id = ?', (row[0], row[2]))
                        self.db_cursor.execute('UPDATE online_inventory SET shopify_tags = ? WHERE id = ?', (row[1], row[2]))
                self.db.commit()
                        
        def get_qoh(self):
                qoh = dict()
                for row in self.db_cursor.execute('SELECT * FROM inventory'):
                        if row[UPC_INDEX] in qoh:
                                qoh[row[UPC_INDEX]] += 1
                        else:
                                qoh[row[UPC_INDEX]] = 1
                return qoh
                        
                        
        def remove_dupes_for_doubles(self):
                list_of_stuff_to_update = []
                upcs = set()
                qoh = self.get_qoh()
                for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE reserved_two = ?', (NEEDS_PUT_OUT,)):
                        upc = row[UPC_INDEX]
                        if upc in upcs:
                                list_of_stuff_to_update.append((ALREADY_OUT, row[NEW_ID_INDEX]))
                        elif upc not in qoh:
                                list_of_stuff_to_update.append((ALREADY_OUT, row[NEW_ID_INDEX]))
                        else:
                                upcs.add(upc)
                for row in list_of_stuff_to_update:
                        self.db_cursor.execute('UPDATE sold_inventory SET reserved_two = ? WHERE id = ?' , (row))
                self.db.commit()
                        
        def remove_dupes_for_ordering(self):
                list_of_stuff_to_update = []
                upcs = set()
                for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE reorder_state = ? ORDER BY date_sold DESC', (NEEDS_REORDERED,)):
                        upc = row[UPC_INDEX]
                        if upc in upcs:
                                print upc
                                list_of_stuff_to_update.append((REORDERED, row[NEW_ID_INDEX]))
                        elif row[NEW_USED_INDEX] == 'Used':
                                list_of_stuff_to_update.append((REORDERED, row[NEW_ID_INDEX]))
                        else:
                              upcs.add(upc)
                for row in list_of_stuff_to_update:
                        print row
                        self.db_cursor.execute('UPDATE sold_inventory SET reorder_state = ? WHERE id = ?', (row))
                self.db.commit()

        def print_doubles_for_spreadsheet(self):
                #print doubles so i can print out to a spreadsheet
                need_to_put_out = []
                for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold DESC')):
                        if self.xint(row[RESERVED_TWO_INDEX]) == NEEDS_PUT_OUT:
                               if row[DISTRIBUTOR_INDEX] != 'Colemine':
                                        need_to_put_out.append(row)
                for row in need_to_put_out:
                        #figure out how many we have left of this item
                        in_stock_count = 0
                        for ix_db, row_db in enumerate(self.db_cursor.execute('SELECT * FROM inventory WHERE upc=?', (row[UPC_INDEX],))):
                                in_stock_count += 1
                        print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (str(in_stock_count),str(row[SOLD_FOR_INDEX]),row[ARTIST_INDEX],row[TITLE_INDEX],row[UPC_INDEX],row[NEW_USED_INDEX],row[DISTRIBUTOR_INDEX],row[GENRE_INDEX])
                return

        def fix_ups(self):
                list_of_stuff_to_update = []
                for ix, row in enumerate(self.db_cursor.execute('SELECT * from sold_online_status')):
                        if 'UPS' in row[ONLINE_SS_SHIPPING_METHOD]:
                                list_of_stuff_to_update.append(('UPS Ground',row[ONLINE_SS_ID]))
                for row in list_of_stuff_to_update:
                        self.db_cursor.execute('UPDATE sold_online_status SET shipping_method = ? WHERE id = ?', row)
                self.db.commit()
                        
                return
                
                
	#this method should be left blank unless some one time operation needs to be done
	def custom_temp_operation(self):

                self.db_cursor.execute('DELETE FROM inventory WHERE id = ?', ('148229',))
		self.db.commit()
                return


                
        
        
        
                for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold DESC')):
                        compare = (datetime.datetime.strptime(str(row[DATE_SOLD_INDEX]),"%Y-%m-%d %H:%M:%S"))
                        if compare.year < 2018:
                                continue
                        if 'shopify' in row[SOLD_NOTES_INDEX]:
                                continue
                        if compare.weekday() == 0:#Monday
                                if compare.hour > 19 and compare.hour < 22:
                                        print 'Monday-%i-%i\t%.2f' % (compare.month,compare.day,row[SOLD_FOR_INDEX])
                        elif compare.weekday() == 1:#tuesday
                                if compare.hour > 19 and compare.hour < 22:
                                        print 'Tuesday-%i-%i\t%.2f' % (compare.month,compare.day,row[SOLD_FOR_INDEX])
                        elif compare.weekday() == 2:#wed
                                if compare.hour > 19 and compare.hour < 22:
                                        print 'Wednesday-%i-%i\t%.2f' % (compare.month,compare.day,row[SOLD_FOR_INDEX])
                        elif compare.weekday() == 3:#thurs
                                if compare.hour > 19 and compare.hour < 22:
                                        print 'Thursday-%i-%i\t%.2f' % (compare.month,compare.day,row[SOLD_FOR_INDEX])
 
                return

                
                #item_lines = []
                #trans_with_id = None
                #for row in self.db_cursor.execute('SELECT * FROM transactions WHERE id = ?', (9052,)):
                #        trans_with_id = list(row)
                #        print row
                #for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE transaction_id = ?', (9052,)):
                #        item_lines.append(list(row))
                #self.receipt_printer.print_receipt(item_lines,[],trans_with_id)
                #return
                
                
                #let's update the tags on each of the items on the website
                #9.8 11.3
                #read in blowout sale percentages
                #reader = csv.reader(open(BLOWOUT_PERCENTAGE_FILE))
                #self.new_percentages = {}
                #for row in reader:
                #        key = row[0]
                #        self.new_percentages[key] = int(row[1])

                #count = 0
                #new_tags = ''
                #for key, value in self.new_percentages.iteritems():
                #        count += 1
                #        print count
                #        if count > 8554:
                #                break
                #        con = False
                #        for row in self.db_cursor.execute('SELECT * FROM online_inventory WHERE upc = ?', (key,)):
                #                if 'NEWSALE' in row[ONLINE_SHOPIFY_TAGS]:
                #                        con = True
                #                new_tags = row[ONLINE_SHOPIFY_TAGS] + ',' + 'NEWSALE' + str(value)
                #        if con == True:
                #                print '%s already done' % key
                #                continue
                #        self.db_cursor.execute('UPDATE online_inventory SET shopify_tags = ? WHERE upc = ?', (new_tags,key))
                #        self.db.commit()
                #        for row in self.db_cursor.execute('SELECT * FROM online_inventory WHERE upc = ?', (key,)):
                #                self.shopify_interface.create_or_update_catalog_item(list(row))
                #                print 'updated %s' % key
                #                time.sleep(0.75)

                #this is here to fix the qoh after using the mass ringer outer at RSD
                #upcs = set()
                #qoh = self.get_qoh()
                #for row in self.db_cursor.execute('SELECT * FROM online_inventory'):
                #        if row[ONLINE_UPC] in qoh:
                #                if qoh[row[ONLINE_UPC]] != row[ONLINE_QOH]:
                #                        upcs.add(row[ONLINE_UPC])
                #                        print '%s - %s' % (row[ONLINE_ARTIST],row[ONLINE_TITLE])
                #        else:#qty is 0
                #                if row[ONLINE_QOH] != 0:
                #                        upcs.add(row[ONLINE_UPC])
                #                        print '%s - %s' % (row[ONLINE_ARTIST],row[ONLINE_TITLE])                                  
                #for upc in upcs:
                #        print 'updating...%s...' % upc
                #        self.upc_qty_change_update_the_site(upc)
                #        time.sleep(0.75)
                #return
                
                #update weights of each item on site
                qoh = self.get_qoh()
                count = 0
                for row in self.db_cursor.execute('SELECT * FROM online_inventory ORDER BY date_added DESC'):
                #for row in self.db_cursor.execute('SELECT * FROM online_inventory'):
                        count += 1
                        qty = 0
                        if row[ONLINE_UPC] in qoh:
                               qty = qoh[row[ONLINE_UPC]]
                        row_list = list(row)
                        row_list[ONLINE_QOH] = qty
                        if count > 6000 and count <= 7000:
                                self.shopify_interface.create_or_update_catalog_item(row_list)
                                print 'updated %s - %s - %s - %s' % (str(count),row_list[ONLINE_ARTIST],row_list[ONLINE_TITLE], row_list[ONLINE_QOH])
                                time.sleep(0.75)
                        
                
                #print stuff to cull new
                #qty_sold = dict()
                #for row in self.db_cursor.execute('SELECT * from sold_inventory'):
                #        if row[UPC_INDEX] in qty_sold:
                #                qty_sold[row[UPC_INDEX]] += 1
                #        else:
                #                qty_sold[row[UPC_INDEX]] = 1
                #qoh = dict()
                #for row in self.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ?', ('New',)):
                #        if row[UPC_INDEX] in qoh:
                #                qoh[row[UPC_INDEX]] += 1
                #        else:
                #                qoh[row[UPC_INDEX]] = 1
                #already_done = set()
                #for row in self.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ?', ('New',)):
                #        qoh_ = 0
                #        if row[UPC_INDEX] in already_done:
                #                continue
                #        if row[UPC_INDEX] in qoh:
                #                qoh_ = qoh[row[UPC_INDEX]]
                #        sold = 0
                #        if row[UPC_INDEX] in qty_sold:
                #                sold = qty_sold[row[UPC_INDEX]]
                #        print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[UPC_INDEX],qoh_,sold,row[DATE_ADDED_INDEX],row[ARTIST_INDEX],row[TITLE_INDEX],row[FORMAT_INDEX])
                #        already_done.add(row[UPC_INDEX])
                
                #list_of_stuff_to_update = []
                #for row in self.db_cursor.execute('SELECT * FROM sold_inventory'):
                #        if 'BF2017' in row[FORMAT_INDEX]:
                                #list_of_stuff_to_update.append((REORDERED, row[NEW_ID_INDEX]))
                #                list_of_stuff_to_update.append((ALREADY_OUT, row[NEW_ID_INDEX]))
                #                print '%s - %s - %s' % (row[ARTIST_INDEX], row[TITLE_INDEX], row[UPC_INDEX])
                #for row in list_of_stuff_to_update:
                        #self.db_cursor.execute('UPDATE sold_inventory SET reorder_state = ? WHERE id = ?', (row))
                #        self.db_cursor.execute('UPDATE sold_inventory SET reserved_two = ? WHERE id = ?', (row))
                #self.db.commit()
		#placeholder = 0
                #total = 0
                #list_of_stuff_to_update = []
                #for row in self.db_cursor.execute('SELECT * from sold_inventory'):
                #        if 'RSD2017' in row[FORMAT_INDEX]:
                #                list_of_stuff_to_update.append((
                #for row in self.db_cursor.execute('SELECT * from sold_inventory'):
                #        if 'sundaypowerout' in row[SOLD_NOTES_INDEX]:
                #                list_of_stuff_to_update.append(('2016-07-30 12:00:00', row[NEW_ID_INDEX]))
                #                total += row[SOLD_FOR_INDEX]
                #                print row
                #print total
                #list_of_stuff_to_update.append(('2016-07-30 12:00:00', ))
                #for row in list_of_stuff_to_update:
                #        self.db_cursor.execute('UPDATE sold_inventory SET date_sold = ? WHERE id = ?', (row))
                #self.db.commit()
                #self.db_cursor.execute('DELETE FROM sold_inventory WHERE upc = ?', ('PLAID080658',))
		#self.db.commit()
                #self.db_cursor.execute('UPDATE sold_online_status SET upc = ? WHERE upc = ?', ('634457537019','602547762986'))
                #self.db.commit()
                #self.db_cursor.execute('UPDATE online_inventory SET format = ? WHERE format = ?', ('LP Vinyl', 'LP'))
                #self.db.commit()
                #self.db_cursor.execute('UPDATE online_inventory SET shopify_desc = ?', ('',))
                #self.db.commit()
                #self.db_cursor.execute('UPDATE online_inventory SET genre = ? WHERE genre = ?', ('Pop / Rock', 'Pop/Rock'))
                #self.db.commit()
                #self.db_cursor.execute('UPDATE pre_order_inventory SET format = ?', ('LP Vinyl',))
                #self.db.commit()
                #list_of_stuff_to_update = []
                #for row in self.db_cursor.execute('SELECT * from sold_inventory WHERE distributor = ?', ('Looney T Birds',)):
                #        if '2016' in row[DATE_ADDED_INDEX]:
                #                list_of_stuff_to_update.append(('Looney T Birds 2', row[NEW_ID_INDEX]))
                #                print '%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[PRICE_INDEX], row[FORMAT_INDEX], row[YEAR_INDEX], row[LABEL_INDEX], row[DATE_ADDED_INDEX], row[DISCOGS_RELEASE_NUMBER_INDEX])
                #for row in list_of_stuff_to_update:
                #        self.db_cursor.execute('UPDATE sold_inventory SET distributor = ? WHERE id = ?', (row))
                #self.db.commit()
                #FUCKFUCK
                #self.db_cursor.execute('UPDATE sold_online_status SET street_date = ? WHERE shopify_id = ?', ('2017-09-08', '5447133010'))
                #self.db.commit()
                #for row in self.db_cursor.execute('SELECT * FROM website_pending_transactions WHERE checked_out = ?', (0,)):
                #        print row
                #self.db_cursor.execute('UPDATE website_pending_transactions SET checked_out = ? WHERE id = ?', (1,1336))
                #self.db.commit()
                #self.db_cursor.execute('DELETE FROM inventory WHERE id = ?', ('107038',))
		#self.db.commit()
                #self.db_cursor.execute('DELETE FROM inventory WHERE id = ?', ('107037',))
		#self.db.commit()
                #self.db_cursor.execute('DELETE FROM sold_inventory WHERE id = ?', ('67236',))
                #elf.db.commit()
                #FIXING ALABAMA SHAKES UPC
		#old_upc = '710882226718'
		#new_upc = '880882226718'
                #self.db_cursor.execute('UPDATE inventory SET taxable = ? WHERE taxable = ?', (1,0))
                #self.db.commit()
		#self.db_cursor.execute('UPDATE sold_inventory SET format = ? WHERE id = ?', ('2xVinyl, LP, Album, Limited Edition','79251'))
		#self.db.commit()
		#self.db_cursor.execute('UPDATE sold_inventory SET new_used = ? WHERE upc = ?', ('New', new_upc))
		#self.db.commit()
                #umg_deal = open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/config/umg_deal.csv').read().splitlines()
                #for upc in umg_deal:
                #        upc = upc.strip()
                #        count = 0
                #        for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc = ?', (upc,)):
                #                count += 1
                #        sold_count = 0
                #        for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc = ?', (upc,)):
                #                sold_count += 1
                #        print '%s\t%s\t%s' % (upc,count,sold_count)
                #carolina_soul = open('/Users/plaidroomrecords/Documents/purchases/carolina_soul_may_2017.csv').read().splitlines()
                #for sku in carolina_soul:
                #        sku_s = sku.strip()
                #        for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc = ?', (sku_s,)):
                #                print '%s\t%s\t%s\t%s\t%s\t%s\t%s' % (row[UPC_INDEX],row[ARTIST_INDEX],row[TITLE_INDEX],row[PRICE_INDEX],row[PRICE_PAID_INDEX],row[DISTRIBUTOR_INDEX],row[DISCOGS_RELEASE_NUMBER_INDEX])
		#checking our double game
		#current_inventory = open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/inventory_01_18_17').read().splitlines()
		#temp_inventory = list()
		#for item in current_inventory:
                #        temp_inventory.append(item.strip())
		#current_inventory = temp_inventory
		#print current_inventory
		#print current_inventory --------------------
                #count = 0
		#for row in self.db_cursor.execute('SELECT * from inventory'):
                #	 if 'PLAID' not in row[UPC_INDEX] and 'PRR' not in row[UPC_INDEX]:
		#		 if row[NEW_USED_INDEX] == 'New':
		#			 if str(row[UPC_INDEX]) not in current_inventory:
		#				 placeholder = 0
                #                                 count += 1
		#				 print '%i ; %s ; %s ; %s ; %s' % (count, row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[FORMAT_INDEX])
                #self.db_cursor.execute('UPDATE inventory SET price_paid = ? WHERE id = ?', ('7.5', '80658'))
                #self.db.commit()
		#total = 0
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Phil',)):
		#	 total += float(row[PRICE_PAID_INDEX])
			#	print '%s\t%s\t%s\t%s' % (row[ARTIST_INDEX], row[TITLE_INDEX], str(row[PRICE_INDEX]/2.0), str(row[DISCOGS_RELEASE_NUMBER_
		#print total
                #list_of_updates = []
                #for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE reorder_state = ?', (NEEDS_REORDERED,)):
                #        if 'shopify' in row[SOLD_NOTES_INDEX]:
                #                if row[RESERVED_ONE_INDEX] == '':
                #                        print '%s - %s - %s' % (row[ARTIST_INDEX],row[TITLE_INDEX], row[RESERVED_ONE_INDEX])
                #                        list_of_updates.append((row[DISTRIBUTOR_INDEX],row[NEW_ID_INDEX]))
                #print list_of_updates
                #for row in list_of_updates:
                #        self.db_cursor.execute('UPDATE sold_inventory SET reserved_one = ? WHERE id = ?', (row))
                #self.db.commit()
		#pricing some distro to a percentage of selling price
		#list_of_stuff_to_update = []
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Tom Luce 2',)):
		#	 price = math.ceil((float(row[PRICE_INDEX]) * 0.367) * 100)/100.0
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Tom Luce',)):
		#	 price = math.ceil((float(row[PRICE_INDEX]) * 0.31) * 100)/100.0
		#	 price = math.ceil((float(row[PRICE_INDEX])*100)/2.0)/100.0
		#	 list_of_stuff_to_update.append((price, row[ID_INDEX]))
		#for row in list_of_stuff_to_update:
		#	 self.db_cursor.execute('UPDATE inventory SET price_paid = ? WHERE id = ?', row)
		#self.db_cursor.execute('UPDATE inventory SET price_paid WHERE distributor = ?', ('Used', 'Thomas'))
		#self.db.commit()
		#total = 0
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Cat Fever',)):
		#	 total += float(row[PRICE_PAID_INDEX])
		#print total
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Brett',)):
		#	 print '%s;%s;%s;%s;%s' % (row[ARTIST_INDEX], row[TITLE_INDEX], row[PRICE_PAID_INDEX],row[PRICE_INDEX],row[DATE_ADDED_INDEX])
		#list_of_stuff_to_update = []
		#for row in self.db_cursor.execute('SELECT * FROM sold_inventory'):
		#	 list_of_stuff_to_update.append((row[DISTRIBUTOR_INDEX], row[NEW_ID_INDEX]))
		#for row in list_of_stuff_to_update:
		#	 self.db_cursor.execute('UPDATE sold_inventory SET reserved_one = ? WHERE id = ?', row)
		#self.db.commit()
		#file_name = '/Users/plaidroomrecords/Documents/pos_software/plaid_room/config/catalogs/City Hall.csv'
		#file_name = '/Users/plaidroomrecords/Documents/pos_software/plaid_room/config/catalogs/Baker and Taylor.csv'
		#with open(file_name, 'rb') as f:
		#	 data = [row for row in csv.reader(f.read().splitlines())]
		#count = 0
		#for row in data:
		#	 [upc, price] = row[0].split()
		#	 for row in self.db_cursor.execute('SELECT * FROM inventory'):
		#		 if row[UPC_INDEX] in upc:
		#			 difference = float(price) - row[PRICE_PAID_INDEX]
		#			 if difference > 0 and difference < 1:
					#if float(price) < (row[PRICE_PAID_INDEX]-0):
	       #				 print ('%s - %s - %f - New price: %s' % (row[ARTIST_INDEX], row[TITLE_INDEX], row[PRICE_PAID_INDEX], price))
		#				 count += 1
		#print count
		#for row in self.db_cursor.execute('SELECT * FROM inventory'):
		#	 if 'Reggae' in row[GENRE_INDEX]:
		#		 if row[NEW_USED_INDEX] == 'Used':
		#			 print '%s - %s - %s' % (row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX])
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor=?', ('Daptone',)):
		#	 print '%s;%s;%s;%s;%s;%s' % (row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[PRICE_INDEX], row[PRICE_PAID_INDEX], row[DATE_ADDED_INDEX].replace(' ',';'))
		#for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE distributor=?', ('Daptone',)):
		#	 print '%s;%s;%s;%s;%s;%s' % (row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[PRICE_INDEX], row[PRICE_PAID_INDEX], row[DATE_ADDED_INDEX].replace(' ',';'))
		#figuring out what has the shittest margins in the shop
		#list_of_shitty_shit = []
		#for row in self.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ?', ('New',)):
		#	 profit = row[PRICE_INDEX] - row[PRICE_PAID_INDEX]
		#	 margin = profit / row[PRICE_INDEX]
		#	 print '%s\t%s\t%s\t%s\t%s' % (margin, profit, row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX])
			#list_of_shitty_shit.append((margin,profit,row[UPC_INDEX],row[ARTIST_INDEX],row[TITLE_INDEX]))
		#for ii in range(1000):
		#	 print 'PRRLTB%05d' % ii

                #for row in self.db_cursor.execute('SELECT * FROM inventory WHERE taxable = ?', (-1,)):
                #        print '%s\t%s\t%s' % (row[ARTIST_INDEX], row[TITLE_INDEX], row[FORMAT_INDEX])


		placeholder = 0

        def colemine_soundscan(self, list_of_dates):
                colemine_soundscan = ColemineSoundscan()
                print 'object initialized, getting ready to crunch numbers'
                #are there any pre-orders we need to be checking skus for?
                #read in pre-order file
                with open(COLEMINE_PRE_ORDER_FILE_NAME, 'rb') as f:
                        reader = csv.reader(f)
                        pre_order_list = list(reader)
                print list_of_dates
                pre_order_cross_check = []
                pre_order_cross_check_pre_date = []
                for title in pre_order_list:
                        print title[1]
                        split_date = title[1].split('-')
                        split_date = datetime.date(int(split_date[0]), int(split_date[1]), int(split_date[2]))
                        if split_date in list_of_dates:
                                pre_order_cross_check.append(title[0])
                        elif split_date > datetime.date.today():
                                pre_order_cross_check_pre_date.append(title[0])
                        #also, if the pre order is in the future, 
                print pre_order_cross_check
                end_date = list_of_dates[0] + datetime.timedelta(days=1)
                sold = colemine_soundscan.get_list_of_orders_from_beginning(list_of_dates[-1],end_date, pre_order_cross_check)
                
                start_date = list_of_dates[0] - datetime.timedelta(days=40)
                sold_pre_orders = colemine_soundscan.get_list_of_orders_for_pre_orders(start_date, end_date, pre_order_cross_check)
                #grab list of zips
                with open(COLEMINE_ZIP_CODE_FILE, 'rb') as f:
                        reader = csv.reader(f)
                        zip_codes = list(reader)
                #print zip_codes
                #now that i have a list of all the stuff, i need to format it in the way that makes soundscan happy
                soundscan_lines = []
                for order in sold:
                        #find zip code for this order
                        zip_code = 0
                        try:
                                if order.shipping_address.country_code == 'US':
                                        zip_ = order.shipping_address.zip[:5]
                                        if zip_.isdigit() and len(zip_) == 5:
                                                zip_code = zip_
                                if zip_code == 0:
                                        zip_code = zip_codes[int(re.sub("[^0-9]", "", order.name))][0]
                        except Exception as e:
                                print 'Exception: %s\n\n\n\n' % e
                                zip_code = '45140'
                        for line in order.line_items:
                                for ii in range(line.quantity):
                                        if line.sku is not None:
                                                if len(line.sku) > 11:
                                                        if line.sku not in pre_order_cross_check:
                                                                if line.sku not in pre_order_cross_check_pre_date:
                                                                        soundscan_lines.append('M3%013d%05dS' % (int(line.sku), int(zip_code)))
                for order in sold_pre_orders:
                        zip_code = 0
                        try:
                                if order.shipping_address.country_code == 'US':
                                        zip_ = order.shipping_address.zip[:5]
                                        if zip_.isdigit() and len(zip_) == 5:
                                                zip_code = zip_
                                if zip_code == 0:
                                        zip_code = zip_codes[int(re.sub("[^0-9]", "", order.name))][0]
                        except Exception as e:
                                zip_code = '45140'
                        for line in order.line_items:
                                for ii in range(int(line.quantity)):
                                        if line.sku in pre_order_cross_check:
                                                soundscan_lines.append('M3%013d%05dS' % (int(line.sku), int(zip_code)))
                #print header
                separate = list_of_dates[0].isoformat().split('-')
                print '92403001406%s' % (list_of_dates[0].strftime("%y%m%d"))
                for line in soundscan_lines:
                        print line
                #print footer
                print '%s %d %d' % ('94', int(len(soundscan_lines)), int(len(soundscan_lines)))
                
                #colemine_soundscan.get_list_of_orders_for_back_dating()
                #generate pool of zip codes
                #zip_file = open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/config/zip_codes.csv', 'w')
                #random_zips = []
                #zips = colemine_soundscan.generate_list_of_zips()
                #random_zips.append(zips)
                #for ii in zips:
                #        print ii
                #        random_zips.append(ii)
                #for ii in range(100000):
                #        random_zips.append(random.choice(zips))
                #random_zips = zips + random_zips
                #for zip_ in random_zips:
                #        zip_file.write("%s\n" % zip_)

                
        def upc_qty_change_update_the_site(self, upc):
                try:
                        qoh = self.get_qoh()
                        exists = False
                        upc_on_hand = 0
                        if upc in qoh:
                                upc_on_hand = qoh[upc]
                         #is it in the database?
                        for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM online_inventory WHERE upc = ?', (upc,))):
                                self.shopify_interface.update_qoh(row[ONLINE_SHOPIFY_ID], upc_on_hand)
                                exists = True
                                break
                        if exists:
                                self.db_cursor.execute('UPDATE online_inventory SET qoh = ? WHERE upc = ?', (upc_on_hand,upc))
                                self.db.commit()
                except Exception as e:
                        print 'Exception while trying to update qoh on website: %s' % e
            
                        
        def soundscan(self, list_of_dates):
                upcs = dict()
                db_results = []
                online_results = []
                pre_upcs = set()
                print list_of_dates
                for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_online_status')):
                        online_results.append(row)
                for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory WHERE new_used = ? ORDER BY date_sold DESC', ('New',))):
                        db_results.append(row)
                for date_ in list_of_dates:
                        print 'matching date %s' % date_
                        separate = date_.isoformat().split('-')
                        desired_date = datetime.date(int(separate[0]), int(separate[1]), int(separate[2]))
                        for ix, row in enumerate(db_results):
                                date_sold = (datetime.datetime.strptime(str(row[DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S")).date()
                                if date_sold == desired_date:
                                        if row[UPC_INDEX].isdigit():
                                                if 'shopify_pre_order' not in row[SOLD_NOTES_INDEX]:
                                                        if row[UPC_INDEX] in upcs:
                                                                upcs[row[UPC_INDEX]] += 1
                                                        else:
                                                                upcs[row[UPC_INDEX]] = 1
                        for ix, row in enumerate(online_results):
                                #for this batch, it doesn't matter when they sold, it just matters when the street date is
                                try:
                                        date_pre_ordered = (datetime.datetime.strptime(str(row[ONLINE_SS_STREET_DATE]), "%Y-%m-%d")).date()
                                        if date_pre_ordered == desired_date:
                                                pre_upcs.add(row[ONLINE_SS_UPC])
                                except Exception as e:
                                        print 'no pre-order date'
                for pre_upc in pre_upcs:
                        qty_sold = 0
                        for ix, row in enumerate(db_results):
                                if row[UPC_INDEX] == pre_upc:
                                        qty_sold += 1
                        if qty_sold > 0:
                                if pre_upc.isdigit():
                                        upcs[pre_upc] = qty_sold
                #print header
                separate = list_of_dates[0].isoformat().split('-')
                print '92090000746%s' % (list_of_dates[0].strftime("%y%m%d"))
                #print date
                total = 0
                for key, value in upcs.iteritems():
                        print 'I3%013d%05d' % (int(key),value)
                        total += value
		#print footer
                print '%s    %s    %s' % ('94', str(len(upcs)), str(total))
                
                #find out dates
                #for row in self.db_cursor.execute('SELECT * FROM sold_inventory'):
                        
                

	def import_csv(self):
		stuff_to_insert = open('/Users/plaidroomrecords/Documents/pos_software/plaid_room/config/looney_adds.csv')
		csv_f = csv.reader(stuff_to_insert)

		for row_file in csv_f:
			if row_file[0] == 'UPC':
				continue
			if row_file[1] != '' and row_file[2] != '' and row_file[3] != '':#if all the info is filled out
				found = False
				for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory WHERE upc = ?', (row_file[0],))):
					print '%s found in inventory' % row_file[0]
					found = True
				if not found:#not already in inventory, add it
					db_item = [''] * 22
					curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
					genre = ''
					if row_file[7] == 'C':
						genre = 'Country'
					if row_file[7] == 'S':
						genre = 'Soul'
					if row_file[7] == 'R':
						genre = 'R&B'
					if row_file[7] == 'G':
						genre = 'Garage'
					if row_file[7] == 'RK':
						genre = 'Rockabilly'
					try:
						db_item[UPC_INDEX] = self.xstr(row_file[0])
						db_item[ARTIST_INDEX] = self.xstr(row_file[1])
						db_item[TITLE_INDEX] = self.xstr(row_file[2])
						db_item[FORMAT_INDEX] = self.xstr('1xVinyl, 7", 45RPM')
						db_item[PRICE_INDEX] = self.xfloat(row_file[5])
						db_item[PRICE_PAID_INDEX] = self.xfloat(0.01)
						db_item[NEW_USED_INDEX] = self.xstr('Used')
						db_item[DISTRIBUTOR_INDEX] = self.xstr('Looney T Birds 45s')
						db_item[LABEL_INDEX] = self.xstr(row_file[3])
						db_item[GENRE_INDEX] = self.xstr(genre)
						db_item[YEAR_INDEX] = self.xint(0)
						db_item[DATE_ADDED_INDEX] = curr_time
						db_item[DISCOGS_RELEASE_NUMBER_INDEX] = self.xint(-1)
						db_item[REAL_NAME_INDEX] = ''
						db_item[PROFILE_INDEX] = ''
						db_item[VARIATIONS_INDEX] = ''
						db_item[ALIASES_INDEX] = ''
						db_item[TRACK_LIST_INDEX] = ''
						db_item[NOTES_INDEX] = self.xstr(('Condition: %s\nNotes: %s' % (row_file[4],row_file[6])))
						db_item[TAXABLE_INDEX] = 1
						db_item[RESERVED_ONE_INDEX] = 'Merged from Tom spreadsheet'
						db_item[RESERVED_TWO_INDEX] = ''
						self.db_cursor.execute('INSERT INTO inventory (upc, artist, title, format, price, price_paid, new_used, distributor, label, genre, year, date_added, discogs_release_number, real_name, profile, variations, aliases, track_list, notes, taxable, reserved_one, reserved_two) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', tuple(db_item))
						self.db.commit()
						time.sleep(0.5)
					except Exception as e:
						print 'priblem adding item to inventory: %s' % e
						return


		list_of_shitty_shit = []
		for row in self.db_cursor.execute('SELECT * FROM inventory WHERE new_used = ?', ('New',)):
			profit = row[PRICE_INDEX] - row[PRICE_PAID_INDEX]
			margin = profit / row[PRICE_INDEX]
			print '%s\t%s\t%s\t%s\t%s' % (margin, profit, row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX])
			#list_of_shitty_shit.append((margin,profit,row[UPC_INDEX],row[ARTIST_INDEX],row[TITLE_INDEX]))
		placeholder = 0


	def print_doubles_that_havent_sold_well(self):
		#grab a list of all the upcs in inventory
		upcs = []
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory ORDER BY date_added')):
			upcs.append(row[UPC_INDEX])
		#make a histogram out of them braj
		upc_hist = self.histogram(upcs)
		items = [(v, k) for k, v in upc_hist.items()]
		items.sort()
		items.reverse() 	    # so largest is first
		upc_hist = [(k, v) for v, k in items]
		count = 0
		upcs_that_are_done = []
		#loop through each one
		for key, value in upc_hist:
			if key in upcs_that_are_done:
				continue
			upcs_that_are_done.append(key)
			#if we don't have more than 1 in inventory, eh, fuck off m8
			if value < 2:
				continue
			count = 0
			for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc=?', (key,))):
				count += 1
			#it's never sold if the count is zero
			if count == 0:
				for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory WHERE upc=?', (key,))):
					#date_time_sold = (datetime.datetime.strptime(str(), "%Y-%m-%d %H:%M:%S"))
					date_time_sold = datetime.datetime.now()#.strftime("%Y-%m-%d %H:%M:%S")
					date_time_added = (datetime.datetime.strptime(str(row[DATE_ADDED_INDEX]), "%Y-%m-%d %H:%M:%S"))
					time_delta = date_time_sold - date_time_added
					days_in_shop = round(float(time_delta.days) + (time_delta.seconds/3600.0)/24.0,1)
					if row[NEW_USED_INDEX] == 'New':
						print '%s;%s;%s;%s;%s;%s;%s' % (row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[FORMAT_INDEX], str(value), str(days_in_shop),str(row[PRICE_PAID_INDEX]))



	def find_stuff_to_sell_on_discogs(self):
		placeholder = 0
		shit_to_sell = []
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory')):
			if ix > 20:
				break
			placehodler = 0
			discogs_release_no = row[DISCOGS_RELEASE_NUMBER_INDEX]
			if discogs_release_no != 1 and row[NEW_USED_INDEX] == 'New':
				prices = [0,0,0]
				self.discogs.scrape_price(discogs_release_no, prices)
				time.sleep(5)
				avg_price = float(prices[1])
				if avg_price > float(row[PRICE_INDEX]):
					shit_to_sell.append('%s - %s - %s online - %s in our shop' % (row[ARTIST_INDEX], row[TITLE_INDEX], locale.currency(avg_price), locale.currency(row[PRICE_INDEX])))
		for item in shit_to_sell:
			print item

	def remove_item(self, key):
		self.db_cursor.execute('DELETE FROM sold_inventory WHERE id = ?', (key,))
		self.db.commit()

	def remove_misc_item(self, key):
		self.db_cursor.execute('DELETE FROM sold_misc_inventory WHERE id = ?', (key,))
		self.db.commit()

	def remove_transaction(self, key):
		self.db_cursor.execute('DELETE FROM transactions WHERE id = ?', (key,))
		self.db.commit()

	def histogram(self, L):
		d = {}
		for x in L:
			if x in d:
				d[x] += 1
			else:
				d[x] = 1
		return d

	def best_sellers(self, top_how_many=25):
		upcs = []
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold ASC')):
			upcs.append(row[UPC_INDEX])
		upc_hist = self.histogram(upcs)
		items = [(v, k) for k, v in upc_hist.items()]
		items.sort()
		items.reverse() 	    # so largest is first
		upc_hist = [(k, v) for v, k in items]
		count = 0
		for key, value in upc_hist:
			if 'PLAID' in key:
				continue
			for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc=?', (key,))):
				print '%d - %s - %s - %s' % (value, key, row[ARTIST_INDEX], row[TITLE_INDEX])
				break
			count += 1
			if count > top_how_many:
				break

	def tell_me_doubles(self):
		upcs = []
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory ORDER BY date_added ASC')):
			upcs.append(row[UPC_INDEX])
		upc_hist = self.histogram(upcs)
		count = 0
		for key, value in upc_hist.items():
			if value > 1:
				count += 1
				for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory WHERE upc=?', (key,))):
					print '%d - %s - %s - %s' % (value, key, row[ARTIST_INDEX], row[TITLE_INDEX])
					break
		print 'Number of doubles: %d' % count


	def summary_by_range(self, list_of_dates):
		new_vinyl_gross = 0
		used_vinyl_gross = 0
		new_vinyl_net = 0
		used_vinyl_net = 0
		clothing_misc_gross = 0
		clothing_misc_net = 0
		other_misc_gross = 0
		other_misc_net = 0
		total_tax_paid = 0
                total_gift_cards_redeemed = 0
                total_shipping = 0
		for date_ in list_of_dates:
			separate = date_.isoformat().split('-')
			returned_stats = self.summary_by_day(separate[0], separate[1], separate[2])
			new_vinyl_gross += returned_stats[0]
			used_vinyl_gross += returned_stats[1]
			new_vinyl_net += returned_stats[2]
			used_vinyl_net += returned_stats[3]
			clothing_misc_gross += returned_stats[4]
			clothing_misc_net += returned_stats[5]
			other_misc_gross += returned_stats[6]
			other_misc_net += returned_stats[7]
			total_tax_paid += returned_stats[8]
                        total_gift_cards_redeemed += returned_stats[12]
                        total_shipping += returned_stats[13]


		print '-'*50
		print '\tTotal Gross Income w/ GCs: %s' % str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross)
                print '\tTotal Gross Income w/o GCs: %s' % str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross - total_gift_cards_redeemed)
                print '\t\tVinyl Gross Income: %s' % str(new_vinyl_gross + used_vinyl_gross)
		print '\t\t\tNew Vinyl Gross Income: %s' % str(new_vinyl_gross)
		print '\t\t\tUsed Vinyl Gross Income: %s' % str(used_vinyl_gross)
		print '\t\tMisc Gross Income: %s' % str(clothing_misc_gross + other_misc_gross)
		print '\t\t\tClothing Gross Income: %s' % str(clothing_misc_gross)
		print '\t\t\tOther Misc. Gross Income: %s' % str(other_misc_gross)
		print '\tTotal Net Income: %s' % str(new_vinyl_net + used_vinyl_net + clothing_misc_net + other_misc_net)
		print '\t\tVinyl Net Income: %s' % str(new_vinyl_net + used_vinyl_net)
		if new_vinyl_gross == 0 or used_vinyl_gross == 0:
			placeholder = 0
		else:
			print '\t\t\tNew Vinyl Net Income: %s - margin: %s' % (str(new_vinyl_net), str(new_vinyl_net/(new_vinyl_gross)*100))
			print '\t\t\tUsed Vinyl Net Income: %s - margin: %s' % (str(used_vinyl_net), str(used_vinyl_net/used_vinyl_gross*100))
		print '\t\tMisc Net Income: %s' % str(clothing_misc_net + other_misc_net)
		print '\t\t\tClothing Net Income: %s' % str(clothing_misc_net)
		print '\t\t\tOther Misc. Net Income: %s' % str(other_misc_net)
		print '\tTotal Tax Paid: %s' % str(total_tax_paid)
		#print '\tThese two numbers should be close: (%s, %s)' % (str(total_gross_with_tax),str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross+total_tax_paid))
                print '\tTotal Shipping: %s' % str(total_shipping)
		print '\n'
		print '-'*50


        def monthly_stats(self):
                curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                history = dict()
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold ASC')):
                        date_sold = row[DATE_SOLD_INDEX]
                        date_sold = date_sold.split('-')
                        #print date_sold
                        old = history['%s-%s-%s' % (date_sold[1],date_sold[0],row[NEW_USED_INDEX])]
                        history['%s-%s-%s' % (date_sold[1],date_sold[0],row[NEW_USED_INDEX])] += row[SOLD_FOR_INDEX]
                print history
                        
                        
	#gives basic stats about a single day, including:
	#   - total gross income
	#      - vinyl gross income
	#	  - new vinyl gross income
	#	  - used vinyl gross income
	#      - misc. gross income
	#	  - clothing gross income
	#	  - other misc gross income
	#   - total net income
	#      - vinyl net income
	#	  - new vinyl net income
	#	  - used vinyl net income
	#      - misc. net income
	#	  - clothing net income
	#	  - other misc net income
	#   - total tax paid
	def summary_by_day(self, year, month, day):
		new_vinyl_qty = 0
		used_vinyl_qty = 0
		new_vinyl_gross = 0
		used_vinyl_gross = 0
		new_vinyl_net = 0
		used_vinyl_net = 0
		clothing_misc_gross = 0
		clothing_misc_net = 0
		other_misc_gross = 0
		other_misc_net = 0
		total_tax_paid = 0
		desired_date = datetime.date(int(year), int(month), int(day))
                total_gift_cards = 0
		number_of_transactions = 0
                shipping = 0
		#build a list of crap to iterate over first because doing nested cursors hurts sqlite3
		db_results = []
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold DESC')):
			db_results.append(row)
		for ix, row in enumerate(db_results):
		 	date_sold = (datetime.datetime.strptime(str(row[DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S")).date()
			if date_sold == desired_date:
				#get extra discount from transaction table
				trans_id = int(row[TRANSACTION_ID_INDEX])
				trans_discount = 0.0
				for ix_trans, discount in enumerate(self.db_cursor.execute('SELECT discount_percent FROM transactions WHERE id=?', (trans_id,))):
					trans_discount = float(discount[0])
				ratio = (100-trans_discount)/100.0
				if row[NEW_USED_INDEX] == 'New':
					new_vinyl_qty += 1
					new_vinyl_gross += (row[SOLD_FOR_INDEX] * ratio)
					new_vinyl_net += ((row[SOLD_FOR_INDEX] - row[PRICE_PAID_INDEX]) * ratio)
				else:
					used_vinyl_qty += 1
					used_vinyl_gross += (row[SOLD_FOR_INDEX] * ratio)
					used_vinyl_net += ((row[SOLD_FOR_INDEX] - row[PRICE_PAID_INDEX]) * ratio)
		db_results = []
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_misc_inventory ORDER BY date_sold ASC')):
			db_results.append(row)
		for ix, row in enumerate(db_results):
			date_sold = (datetime.datetime.strptime(str(row[MISC_DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S")).date()
			if date_sold == desired_date:
				#get extra discount from transaction table
				trans_id = int(row[MISC_TRANSACTION_ID_INDEX])
				trans_discount = 0.0
				for ix_trans, discount in enumerate(self.db_cursor.execute('SELECT discount_percent FROM transactions WHERE id=?', (trans_id,))):
					trans_discount = float(discount[0])
				ratio = (100-trans_discount)/100.0
				if row[MISC_TYPE_INDEX] == 'Clothing':
					clothing_misc_gross += (row[MISC_SOLD_FOR_INDEX] * ratio)
					clothing_misc_net += ((row[MISC_SOLD_FOR_INDEX] - row[MISC_PRICE_PAID_INDEX]) * ratio)
				else:
					other_misc_gross += (row[MISC_SOLD_FOR_INDEX] * ratio)
					other_misc_net += ((row[MISC_SOLD_FOR_INDEX] - row[MISC_PRICE_PAID_INDEX]) * ratio)

		total_gross_with_tax = 0
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM transactions ORDER BY date_sold')):
			date_sold = (datetime.datetime.strptime(str(row[TRANS_DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S")).date()
			if date_sold == desired_date:
				number_of_transactions += 1
				total_tax_paid += (row[TRANS_TAX_INDEX])
				total_gross_with_tax += row[TRANS_TOTAL_INDEX]
                                split_sentence = row[TRANS_RESERVED_ONE_INDEX].split()
                                shipping += row[TRANS_SHIPPING_INDEX]
                                if len(split_sentence) > 1:
                                        if 'shopify' not in split_sentence:
                                                total_gift_cards += (float(split_sentence[4][:-1]) - float(split_sentence[22][:-1]))

		stats_to_return = [new_vinyl_gross, used_vinyl_gross, new_vinyl_net, used_vinyl_net, clothing_misc_gross, clothing_misc_net, other_misc_gross, other_misc_net, total_tax_paid, new_vinyl_qty, used_vinyl_qty, number_of_transactions, total_gift_cards, shipping]

		print '\nDate: %s-%s-%s' % (str(year),str(month),str(day))
		print '\tTotal Gross Income(including gift cards): %s' % str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross)
                print '\tTotal Gross Income(excluding gift cards): %s' % str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross - total_gift_cards) 
                print '\t\tVinyl Gross Income: %s' % str(new_vinyl_gross + used_vinyl_gross)
		print '\t\t\tNew Vinyl Gross Income: %s' % str(new_vinyl_gross)
		print '\t\t\tUsed Vinyl Gross Income: %s' % str(used_vinyl_gross)
		print '\t\tMisc Gross Income: %s' % str(clothing_misc_gross + other_misc_gross)
		print '\t\t\tClothing Gross Income: %s' % str(clothing_misc_gross)
		print '\t\t\tOther Misc. Gross Income: %s' % str(other_misc_gross)
		print '\tTotal Net Income: %s' % str(new_vinyl_net + used_vinyl_net + clothing_misc_net + other_misc_net)
		print '\t\tVinyl Net Income: %s' % str(new_vinyl_net + used_vinyl_net)
		if new_vinyl_gross == 0 or used_vinyl_gross == 0:
			placeholder = 0
		else:
			print '\t\t\tNew Vinyl Net Income: %s - margin: %s' % (str(new_vinyl_net), str(new_vinyl_net/(new_vinyl_gross)*100))
			print '\t\t\tUsed Vinyl Net Income: %s - margin: %s' % (str(used_vinyl_net), str(used_vinyl_net/used_vinyl_gross*100))
		print '\t\tMisc Net Income: %s' % str(clothing_misc_net + other_misc_net)
		print '\t\t\tClothing Net Income: %s' % str(clothing_misc_net)
		print '\t\t\tOther Misc. Net Income: %s' % str(other_misc_net)
		print '\tTotal Tax Paid: %s' % str(total_tax_paid)
		print '\tThese two numbers should be close: (%s, %s)' % (str(total_gross_with_tax),str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross+total_tax_paid))
		print '\n'

		return stats_to_return

	def get_all_distros(self):
		distros = set()
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory')):
			distros.add(row[DISTRIBUTOR_INDEX])
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory')):
			distros.add(row[DISTRIBUTOR_INDEX])
		return list(distros)

	def distro_stock_info(self, distro):
		#first, loop through the sold and the current inventories and get a list of every UPC we've ever had from that distro
		upcs = set()
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM inventory WHERE distributor=?', (distro,))):
			upcs.add(row[UPC_INDEX])
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory WHERE distributor=?', (distro,))):
			upcs.add(row[UPC_INDEX])
		pairs_to_print = []
		#loop through upcs and shit out a ton of statistics on each release
		for upc in upcs:
			artist = ''
			title = ''
			number_of_times_sold = 0
			for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc=?', (upc,)):
				if artist == '':
					artist = row[ARTIST_INDEX]
					title = row[TITLE_INDEX]
				number_of_times_sold += 1
			left_in_stock = 0
			for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc=?', (upc,)):
				if artist == '':
					artist = row[ARTIST_INDEX]
					title = row[TITLE_INDEX]
				left_in_stock += 1
			#average price from this distro
			prices = []
			for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc=? AND distributor=?', (upc,distro)):
				prices.append(row[PRICE_PAID_INDEX])
			for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc=? AND distributor=?', (upc,distro)):
				prices.append(row[PRICE_PAID_INDEX])
			avg_price = float(sum(prices)) / float(len(prices))
			#do we ever get from other distros
			other_distros = set()
			for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc=?', (upc,)):
				if row[DISTRIBUTOR_INDEX] != distro:
					other_distros.add(row[DISTRIBUTOR_INDEX])
			for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc=?', (upc,)):
				if row[DISTRIBUTOR_INDEX] != distro:
					other_distros.add(row[DISTRIBUTOR_INDEX])
			string_to_print = '%i in stock - %i sold - %0.2f paid on average - %s - %s - %s' % (left_in_stock, number_of_times_sold, avg_price, upc, artist, title)
			price_paid_other = 0
			for other_distro in other_distros:
				for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc=? AND distributor=?', (upc,other_distro)):
					if price_paid_other == 0:
						price_paid_other = row[PRICE_PAID_INDEX]
				for row in self.db_cursor.execute('SELECT * FROM sold_inventory WHERE upc=? AND distributor=?', (upc,other_distro)):
					if price_paid_other == 0:
						price_paid_other = row[PRICE_PAID_INDEX]
				addition_to_string = '\n\tSometimes get from %s for %f (%f more than %s)' % (other_distro, price_paid_other, (price_paid_other-avg_price), distro)
				string_to_print += addition_to_string

			tuple_to_add_to_list = (left_in_stock, string_to_print)
			pairs_to_print.append(tuple_to_add_to_list)
			#print '%s - %s - %i sold - %i left in stock - %f paid on average' % (artist, title, number_of_times_sold, left_in_stock, avg_price)
		for ii in range(0,100):
			for item in pairs_to_print:
				if item[0] == ii:
					print item[1]
		print ''

	def show_me_new_with_plaid_skus(self):
		for row in self.db_cursor.execute('SELECT * FROM inventory WHERE new_used=?', ('New',)):
			if 'PLAID' in row[UPC_INDEX] and '7\"' not in row[FORMAT_INDEX] and '45 RPM' not in row[FORMAT_INDEX]:
				print '\t%s - %s - %s' % (row[ARTIST_INDEX], row[TITLE_INDEX], row[FORMAT_INDEX])

	def generate_db_for_date_and_time(self, year, month, day, hour=0, minute=0):
		specified_db = []
		at_moment = datetime.datetime(year, month, day, hour, minute)
		for row in self.db_cursor.execute('SELECT * FROM inventory'):
			#if len(specified_db)%100 == 0:
				#print '%d - current' % len(specified_db)
                        try:
                                time_put_in = (datetime.datetime.strptime(str(row[DATE_ADDED_INDEX]), "%Y-%m-%d %H:%M:%S"))
			except Exception as e:
				 print e
				 print row
			if time_put_in < at_moment:
				specified_db.append(list(row))
		for row in self.db_cursor.execute('SELECT * FROM sold_inventory'):
                        #print row
			if len(specified_db)%100 == 0:
                                shit = 0
                                #print '%d - sold' % len(specified_db)
                        #print row[DATE_ADDED_INDEX]
			time_put_in = (datetime.datetime.strptime(str(row[DATE_ADDED_INDEX]), "%Y-%m-%d %H:%M:%S"))
			time_sold = (datetime.datetime.strptime(str(row[DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S"))
			if ((at_moment > time_put_in) and (at_moment < time_sold)):
				specified_db.append(list(row))
		new_vinyl_qty = 0
		used_vinyl_qty = 0
		new_vinyl_costs = 0
		new_vinyl_prices = 0
		used_vinyl_costs = 0
		used_vinyl_prices = 0
		new_vinyl_skus = set()
		for row in specified_db:
			if row[NEW_USED_INDEX] == 'New':
				new_vinyl_qty += 1
				new_vinyl_costs += row[PRICE_PAID_INDEX]
				new_vinyl_prices += row[PRICE_INDEX]
				new_vinyl_skus.add(row[UPC_INDEX])
			else:
				used_vinyl_qty += 1
				used_vinyl_costs += row[PRICE_PAID_INDEX]
				used_vinyl_prices += row[PRICE_INDEX]
		print '\t Summary for %s-%s-%s %s:%s' % (str(year), str(month), str(day), str(hour), str(minute))
		print '\t\t\t Total Vinyl: %d, %s paid, %s priced' % (new_vinyl_qty+used_vinyl_qty, locale.currency(new_vinyl_costs+used_vinyl_costs), locale.currency(new_vinyl_prices+used_vinyl_prices))
		print '\t\t\t New Vinyl: %d, %s paid, %s priced' % (new_vinyl_qty, locale.currency(new_vinyl_costs), locale.currency(new_vinyl_prices))
		print '\t\t\t Used Vinyl: %d, %s paid, %s priced' % (used_vinyl_qty, locale.currency(used_vinyl_costs), locale.currency(used_vinyl_prices))
		print '-'*50
		stats_to_return = [new_vinyl_qty, new_vinyl_costs, new_vinyl_prices, used_vinyl_qty, used_vinyl_costs, used_vinyl_prices, len(new_vinyl_skus), (new_vinyl_qty+used_vinyl_qty), (new_vinyl_costs+used_vinyl_costs), (new_vinyl_prices+used_vinyl_prices)]
		return stats_to_return

	def xstr(self,s):
		if s is None:
			return ''
		return str(s)

	def xint(self, i):
		if (i is None) or (i == ''):
			return -1
		return int(i)

	def xfloat(self, f):
		if (f is None) or (f == ''):
			return -1
		return float(f)



if __name__ == '__main__':
	util = Util(sys.argv[1])
	entered = ''
	while(entered != 'q' and entered != 'quit'):
		entered = raw_input('plaid-room-util > ')
		if entered == 'custom_temp':
			util.custom_temp_operation()
		if entered == 'h' or entered == 'help':
			print '\nh(elp) - display this message'
			print 's(ummary) - display summary of past week'
			print 'd(ay) - display summary of single day'
			print 'r(ange) - display summary stats for a range'
			print 'b(est) - display best sellers'
			print 'doubles - display doubles'
			print 'distro_oos - display info about titles we get from a certain distributor'
			print 'remove_item - remove item from item history'
			print 'remove_misc_item - remove misc. item from history'
			print 'remove_transaction - remove transaction from history'
			print 'what_to_sell - find stuff to sell on discogs'
			print 't(ime_machine) - stats about db at any point in time'
			print 'time_travel_range - time travel through a range with a summary at the end'
			print 'new_with_plaid_sku - list all the shit someone might have fucked up'
			print 'import_alliance - import an alliance order'
			print 'shit_selling_doubles - self explanatory'
                        print 'soundscan - generate soundscan report'
                        print 'colemine_soundscan - generate colemine soundscan IMO report'
                        print 'remove_dupes_for_ordering - remove duplicate UPCs for ordering expedition'
                        print 'remove_dupes_for_doubles - remove duplicates and items with quantity zero from doubles'
                        print 'remove_nr - remove any new releases older than 100 releases'
                        print 'add_nr - add new release tag to some amount of new releases'
                        print 'fix_ups - fix registered trade mark issue in ups ground'
		elif entered == 's' or entered =='summary':
			print 'doing stuff to things'
		elif entered == 'd' or entered == 'day':
			print '\tPlease enter date in following format: yyyy-mm-dd'
			entered_date = raw_input('plaid-room-util/summary_by_day > ')
			entered_date = entered_date.split('-')
			util.summary_by_day(entered_date[0], entered_date[1], entered_date[2])
		elif entered == 'r' or entered == 'range':
			print '\tPlease enter the starting date in the following format: yyyy-mm-dd'
			start_date = raw_input('plaid-room-util/summary_by_range > ')
			start_date = start_date.split('-')
			start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
			print '\tPlease enter the ending date in the following format:	 yyyy-mm-dd'
			end_date = raw_input('plaid-room-util/summary_by_range > ')
			end_date = end_date.split('-')
			end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
			delta_dates = (end_date - start_date)
			delta_dates = int(delta_dates.days) + 1
			date_list = [end_date - datetime.timedelta(days=x) for x in range(0, delta_dates)]
			util.summary_by_range(date_list)
			#for date_ in date_list:
			#	 print date_
		elif entered == 'b' or entered == 'best':
			number_to_display = int(raw_input('plaid-room-util/best_sellers > '))
			util.best_sellers(number_to_display)
		elif entered == 'doubles':
			util.tell_me_doubles()
		elif entered == 'what_to_sell':
			util.find_stuff_to_sell_on_discogs()
		elif entered == 'distro_oos':
			#first make a list of every distributor we've ever used, and have the user choose one
			print 'Here\'s all the distributors bro:'
			distros = util.get_all_distros()
			for distro in distros:
				print '\t%s' % distro
			print 'Which distributor? (Use capitals as shown above!!)'
			distro = raw_input('plaid-room-util/distro_oos > ')
			if distro not in distros:
				print 'what distributor is that!?'
				continue
			util.distro_stock_info(distro)
		elif entered == 'remove_item':
			to_remove = int(raw_input('plaid-room-util/remove_item > '))
			util.remove_item(to_remove)
		elif entered == 'remove_misc_item':
			to_remove = int(raw_input('plaid-room-util/remove_misc_item > '))
			util.remove_misc_item(to_remove)
		elif entered == 'remove_transaction':
			to_remove = int(raw_input('plaid-room_util/remove_transaction > '))
			util.remove_transaction(to_remove)
		elif entered == 'import_alliance':
			util.import_alliance_order()
		elif entered == 'import_csv':
			util.import_csv()
                elif entered == 'remove_dupes_for_ordering':
                        util.remove_dupes_for_ordering()
                elif entered == 'remove_dupes_for_doubles':
                        util.remove_dupes_for_doubles()
                elif entered == 'remove_nr':
                        util.remove_older_new_releases_from_site()
                elif entered == 'add_nr':
                        util.add_new_release_tag()
                elif entered == 'monthly':
                        util.monthly_stats()
                elif entered == 'colemine_soundscan':
                        print '\tPlease enter the starting date in the following format: yyyy-mm-dd'
			start_date = raw_input('plaid-room-util/colemine-soundscan > ')
			start_date = start_date.split('-')
			start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
			print '\tPlease enter the ending date in the following format:	 yyyy-mm-dd'
			end_date = raw_input('plaid-room-util/colemine-soundscan > ')
			end_date = end_date.split('-')
			end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
			delta_dates = (end_date - start_date)
			delta_dates = int(delta_dates.days) + 1
			date_list = [end_date - datetime.timedelta(days=x) for x in range(0, delta_dates)]
                        util.colemine_soundscan(date_list)
                elif entered == 'soundscan':
                        print '\tPlease enter the starting date in the following format: yyyy-mm-dd'
			start_date = raw_input('plaid-room-util/soundscan > ')
			start_date = start_date.split('-')
			start_date = datetime.date(int(start_date[0]), int(start_date[1]), int(start_date[2]))
			print '\tPlease enter the ending date in the following format:	 yyyy-mm-dd'
			end_date = raw_input('plaid-room-util/soundscan > ')
			end_date = end_date.split('-')
			end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
			delta_dates = (end_date - start_date)
			delta_dates = int(delta_dates.days) + 1
			date_list = [end_date - datetime.timedelta(days=x) for x in range(0, delta_dates)]
                        util.soundscan(date_list)
		elif entered == 't' or entered == 'time_machine':
			print '\tPlease enter the date/time in the following format: yyyy-mm-dd-hh-mm'
			travel_to_time = raw_input('plaid-room-util/time_machine > ')
			travel_to_time = travel_to_time.split('-')
			util.generate_db_for_date_and_time(int(travel_to_time[0]), int(travel_to_time[1]), int(travel_to_time[2]), int(travel_to_time[3]), int(travel_to_time[4]))
		elif entered == 'time_travel_range':
			hours = [8, 11, 14, 17, 20]
			#hours = [8]
			print 'Please enter the start date in the following format: yyyy-mm-dd'
			travel_to_time_start = raw_input('plaid-room-util/time_travel_range > ')
			print 'Please enter the end date in the following format: yyyy-mm-dd'
			travel_to_time_end = raw_input('plaid-room-util/time_travel_range > ')
			travel_to_time_start = travel_to_time_start.split('-')
			travel_to_time_start = datetime.date(int(travel_to_time_start[0]), int(travel_to_time_start[1]), int(travel_to_time_start[2]))
			travel_to_time_end = travel_to_time_end.split('-')
			travel_to_time_end = datetime.date(int(travel_to_time_end[0]), int(travel_to_time_end[1]), int(travel_to_time_end[2]))
			delta_dates = (travel_to_time_end - travel_to_time_start)
			delta_dates = int(delta_dates.days) + 1
			date_list = [travel_to_time_end - datetime.timedelta(days=x) for x in range(0, delta_dates)]
			new_cumulative = 0
			used_cumulative = 0
			total_stats = []
			stats_temp = []
			weekly_stats = []
			this_monday = 0
			week_new_gross = 0
			week_used_gross = 0
			week_new_net = 0
			week_used_net = 0
			week_clothing_gross = 0
			week_clothing_net = 0
			week_misc_gross = 0
			week_misc_net = 0
			week_taxes = 0
			week_new_qty = 0
			week_used_qty = 0
			week_transactions = 0
			week_total_gross = 0
			week_total_net = 0
			last_item = date_list[0]
			for date_item in reversed(date_list):
				daily_stats = util.summary_by_day(date_item.year, date_item.month, date_item.day)
				#daily number crunching
				new_cumulative += daily_stats[9]
				used_cumulative += daily_stats[10]
				total_gross = daily_stats[0] + daily_stats[1] + daily_stats[4] + daily_stats[6]
				total_net = daily_stats[2] + daily_stats[3] + daily_stats[5] + daily_stats[7]
				#weekly number crunching
				if date_item.weekday() == 0:#it's monday dawg
					if this_monday == 0:#first time through, stuff hasn't been initialized, so initialize and then skip this week
						this_monday = date_item
					else:
						#first, save last weeks stats
						stats_temp = []
						stats_temp = [this_monday.isoformat(), week_new_gross, week_used_gross, week_new_net, week_used_net, week_clothing_gross, week_clothing_net, week_misc_gross, week_misc_net, week_taxes, week_new_qty, week_used_qty, week_transactions, week_total_gross, week_total_net]
						weekly_stats.append(stats_temp)
						this_monday = date_item
					week_new_gross = daily_stats[0]
					week_used_gross = daily_stats[1]
					week_new_net = daily_stats[2]
					week_used_net = daily_stats[3]
					week_clothing_gross = daily_stats[4]
					week_clothing_net = daily_stats[5]
					week_misc_gross = daily_stats[6]
					week_misc_net = daily_stats[7]
					week_taxes = daily_stats[8]
					week_new_qty = daily_stats[9]
					week_used_qty = daily_stats[10]
					week_transactions = daily_stats[11]
					week_total_gross = total_gross
					week_total_net = total_net
				else:
					week_new_gross += daily_stats[0]
					week_used_gross += daily_stats[1]
					week_new_net += daily_stats[2]
					week_used_net += daily_stats[3]
					week_clothing_gross += daily_stats[4]
					week_clothing_net += daily_stats[5]
					week_misc_gross += daily_stats[6]
					week_misc_net += daily_stats[7]
					week_taxes += daily_stats[8]
					week_new_qty += daily_stats[9]
					week_used_qty += daily_stats[10]
					week_transactions += daily_stats[11]
					week_total_gross += total_gross
					week_total_net += total_net
					#is this the last time we loop through
					if last_item == date_item:
						stats_temp = [this_monday.isoformat(), week_new_gross, week_used_gross, week_new_net, week_used_net, week_clothing_gross, week_clothing_net, week_misc_gross, week_misc_net, week_taxes, week_new_qty, week_used_qty, week_transactions, week_total_gross, week_total_net]
						weekly_stats.append(stats_temp)
				for hour in hours:
					stats_temp = []
					to_append = util.generate_db_for_date_and_time(date_item.year, date_item.month, date_item.day, hour, 0)
					stats_temp.append(date_item.isoformat()+(" %02d:%02d"%(hour,0)))
					stats_temp += (to_append)
					stats_temp += (daily_stats)
					stats_temp.append(total_gross)
					stats_temp.append(total_net)
					stats_temp.append(new_cumulative)
					stats_temp.append(used_cumulative)
					total_stats.append(stats_temp)


			print 'Date,New Vinyl Qty,New Vinyl Cost,New Vinyl Price,Used Vinyl Qty,Used Vinyl Cost,Used Vinyl Price,No. New Titles,New Gross,Used Gross,New Net,Used Net,Clothing Gross,Clothing Net,Misc Gross, Misc Net,Taxes,New Qty,Used Qty,Total Gross,Total Net'
			with open('/Users/plaidroomrecords/Documents/pos_software/time_travel.csv', 'wb') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				#spamwriter.writerow(['Spam'] * 5 + ['Baked Beans'])
				#spamwriter.writerow(['Spam', 'Lovely Spam', 'Wonderful Spam'])
				spamwriter.writerow(['Date','New Vinyl Qty','New Vinyl Cost','New Vinyl Price','Used Vinyl Qty','Used Vinyl Cost','Used Vinyl Price','No. New Titles','Total Qty','Total Cost','Total Price','New Gross','Used Gross','New Net','Used Net','Clothing Gross','Clothing Net','Misc Gross','Misc Net','Taxes','New Qty Sold','Used Qty Sold','No. Transactions','Total Gross','Total Net','New Cumulative','Used Cumulative'])
				#for line in total_stats:
				spamwriter.writerows(total_stats)
			with open('/Users/plaidroomrecords/Documents/pos_software/week_time_travel.csv', 'wb') as csvfile:
				spamwriter = csv.writer(csvfile, delimiter=',',quoting=csv.QUOTE_MINIMAL)
				spamwriter.writerow(['Week Start Date','New Gross','Used Gross','New Net','Used Net','Clothing Gross','Clothing Net','Misc Gross','Misc Net','Taxes','New Qty Sold','Used Qty Sold','No. Transactions','Week Gross','Week Net'])
				spamwriter.writerows(weekly_stats)
				#spamwriter.writerows(line)
					#for item in line:
						#print item,
						#print ',',
		elif entered == 'new_with_plaid_sku':
			util.show_me_new_with_plaid_skus()
		elif entered == 'shit_selling_doubles':
			util.print_doubles_that_havent_sold_well()
                elif entered == 'fix_ups':
                        util.fix_ups()
