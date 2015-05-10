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

class Util():
	def __init__(self, primary='real_inventory.db'):
		print 'Primary DB: %s' % primary
		self.db = sqlite3.connect(primary)
                self.db_cursor = self.db.cursor()
                locale.setlocale( locale.LC_ALL, '')
                self.discogs = DiscogsClient()#discogs api
                
        #this method should be left blank unless some one time operation needs to be done
        def custom_temp_operation(self):
                placeholder = 0
                #FIXING ALABAMA SHAKES UPC
                #old_upc = '710882226718'
                #new_upc = '880882226718'
                #self.db_cursor.execute('UPDATE sold_inventory SET upc = ? WHERE upc = ?', (new_upc,old_upc))
                #self.db.commit()
                #self.db_cursor.execute('UPDATE sold_inventory SET new_used = ? WHERE upc = ?', ('New', new_upc))
                #self.db.commit()
                #checking our double game
                #current_inventory = open('/Users/plaidroomrecords/Desktop/inventory_checker.txt').read().splitlines()
                #print current_inventory --------------------
                #for row in self.db_cursor.execute('SELECT * from inventory'):
                #        if 'PLAID' not in row[UPC_INDEX] and 'PRR' not in row[UPC_INDEX]:
                #if row[NEW_USED_INDEX] == 'New' and '7\"' not in row[FORMAT_INDEX] and 'CD' not in row[FORMAT_INDEX]:
                #                        if str(row[UPC_INDEX]) not in current_inventory:
                #                                placeholder = 0
                #                                print '%s - %s - %s - %s' % (row[UPC_INDEX], row[ARTIST_INDEX], row[TITLE_INDEX], row[FORMAT_INDEX])
                #total = 0
                #for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Phil',)):
                #        total += float(row[PRICE_PAID_INDEX])
                        #       print '%s\t%s\t%s\t%s' % (row[ARTIST_INDEX], row[TITLE_INDEX], str(row[PRICE_INDEX]/2.0), str(row[DISCOGS_RELEASE_NUMBER_
                #print total
                        
                #pricing some distro to a percentage of selling price
                list_of_stuff_to_update = []
                for row in self.db_cursor.execute('SELECT * FROM inventory WHERE distributor = ?', ('Phil',)):
                        #price = math.ceil((float(row[PRICE_INDEX]) * 0.4) * 100)/100.0
                        price = math.ceil((float(row[PRICE_INDEX])*100)/2.0)/100.0
                        list_of_stuff_to_update.append((price, row[ID_INDEX]))
                for row in list_of_stuff_to_update:
                        self.db_cursor.execute('UPDATE inventory SET price_paid = ? WHERE id = ?', row)
                #self.db_cursor.execute('UPDATE inventory SET price_paid WHERE distributor = ?', ('Used', 'Thomas'))
                self.db.commit()
                
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
                items.reverse()             # so largest is first
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


                print '-'*50
                print '\tTotal Gross Income: %s' % str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross)
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
		print '\n'
                print '-'*50
                        
                        
                
	#gives basic stats about a single day, including:
	#   - total gross income
	#      - vinyl gross income
	#         - new vinyl gross income
	#         - used vinyl gross income
	#      - misc. gross income
	#         - clothing gross income
	#         - other misc gross income 
	#   - total net income
	#      - vinyl net income
	#         - new vinyl net income
	#         - used vinyl net income
	#      - misc. net income
	#         - clothing net income
	#         - other misc net income
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
                number_of_transactions = 0
                #build a list of crap to iterate over first because doing nested cursors hurst sqlite3
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

                stats_to_return = [new_vinyl_gross, used_vinyl_gross, new_vinyl_net, used_vinyl_net, clothing_misc_gross, clothing_misc_net, other_misc_gross, other_misc_net, total_tax_paid, new_vinyl_qty, used_vinyl_qty, number_of_transactions]
                        
		print '\nDate: %s-%s-%s' % (str(year),str(month),str(day))
		print '\tTotal Gross Income: %s' % str(new_vinyl_gross + used_vinyl_gross + clothing_misc_gross + other_misc_gross)
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
                        if len(specified_db)%100 == 0:
                                print '%d - current' % len(specified_db)
                        time_put_in = (datetime.datetime.strptime(str(row[DATE_ADDED_INDEX]), "%Y-%m-%d %H:%M:%S"))
                        if time_put_in < at_moment:
                                specified_db.append(list(row))
                for row in self.db_cursor.execute('SELECT * FROM sold_inventory'):
                        if len(specified_db)%100 == 0:
                                print '%d - sold' % len(specified_db)
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
                stats_to_return = [new_vinyl_qty, new_vinyl_costs, new_vinyl_prices, used_vinyl_qty, used_vinyl_costs, used_vinyl_prices, len(new_vinyl_skus)]
                return stats_to_return

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
                        print '\tPlease enter the ending date in the following format:   yyyy-mm-dd'
                        end_date = raw_input('plaid-room-util/summary_by_range > ')
                        end_date = end_date.split('-')
                        end_date = datetime.date(int(end_date[0]), int(end_date[1]), int(end_date[2]))
                        delta_dates = (end_date - start_date)
                        delta_dates = int(delta_dates.days) + 1
                        date_list = [end_date - datetime.timedelta(days=x) for x in range(0, delta_dates)]
                        util.summary_by_range(date_list)
                        #for date_ in date_list:
                        #        print date_
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
                                spamwriter.writerow(['Date','New Vinyl Qty','New Vinyl Cost','New Vinyl Price','Used Vinyl Qty','Used Vinyl Cost','Used Vinyl Price','No. New Titles','New Gross','Used Gross','New Net','Used Net','Clothing Gross','Clothing Net','Misc Gross','Misc Net','Taxes','New Qty Sold','Used Qty Sold','No. Transactions','Total Gross','Total Net','New Cumulative','Used Cumulative'])
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

