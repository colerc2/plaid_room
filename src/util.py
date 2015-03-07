#!/usr/bin/python

import sys
import sqlite3
import time
from config_stuff import *
import datetime

class Util():
	def __init__(self, primary='real_inventory.db'):
		print 'Primary DB: %s' % primary
		self.db = sqlite3.connect(primary)
		self.db_cursor = self.db.cursor()
                
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
					new_vinyl_gross += (row[SOLD_FOR_INDEX] * ratio)
					new_vinyl_net += ((row[SOLD_FOR_INDEX] - row[PRICE_PAID_INDEX]) * ratio)
				else:
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
                                total_tax_paid += (row[TRANS_TAX_INDEX])
                                total_gross_with_tax += row[TRANS_TOTAL_INDEX]

                stats_to_return = [new_vinyl_gross, used_vinyl_gross, new_vinyl_net, used_vinyl_net, clothing_misc_gross, clothing_misc_net, other_misc_gross, other_misc_net, total_tax_paid]
                        
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

if __name__ == '__main__':
	util = Util(sys.argv[1])
	entered = ''
	while(entered != 'q' and entered != 'quit'):
		entered = raw_input('plaid-room-util > ')
		if entered == 'h' or entered == 'help':
			print '\nh(elp) - display this message'
			print 's(ummary) - display summary of past week'
			print 'd(ay) - display summary of single day'
                        print 'r(ange) - display summary stats for a range'
                        print 'b(est) - display best sellers'
                        print 'doubles - display doubles'
                        print 'distro_oos - display info about titles we get from a certain distributor'
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
                        
                
                        
