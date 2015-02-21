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


        def best_sellers(self):
                upcs = []
                for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold ASC')):
                        upcs.append(row[UPC_INDEX])
                best = max(set(upcs), key=upcs.count)
                best_number_sold = upcs.count(best)
                print best
                print best_number_sold
                
        def summary_by_range(self, list_of_dates):
                new_vinyl_gross = 0
                used_vinyl_gross = 0
                new_vinyl_net = 0
                used_vinyl_net = 0
                clothing_misc_gross = 0
                clothing_misc_net = 0
                other_misc_gross = 0
                other_misc_net = 0
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
	def summary_by_day(self, year, month, day):
		new_vinyl_gross = 0
		used_vinyl_gross = 0
		new_vinyl_net = 0
		used_vinyl_net = 0
		clothing_misc_gross = 0
		clothing_misc_net = 0
		other_misc_gross = 0
		other_misc_net = 0
		desired_date = datetime.date(int(year), int(month), int(day))
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_inventory ORDER BY date_sold ASC')):
			date_sold = (datetime.datetime.strptime(str(row[DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S")).date()
			if date_sold == desired_date:
				if row[NEW_USED_INDEX] == 'New':
					new_vinyl_gross += row[SOLD_FOR_INDEX]
					new_vinyl_net += (row[SOLD_FOR_INDEX] - row[PRICE_PAID_INDEX])
				else:
					used_vinyl_gross += row[SOLD_FOR_INDEX]
					used_vinyl_net += (row[SOLD_FOR_INDEX] - row[PRICE_PAID_INDEX])
		for ix, row in enumerate(self.db_cursor.execute('SELECT * FROM sold_misc_inventory ORDER BY date_sold ASC')):
			date_sold = (datetime.datetime.strptime(str(row[MISC_DATE_SOLD_INDEX]), "%Y-%m-%d %H:%M:%S")).date()
			if date_sold == desired_date:
				if row[MISC_TYPE_INDEX] == 'Clothing':
					clothing_misc_gross += row[MISC_SOLD_FOR_INDEX]
					clothing_misc_net += (row[MISC_SOLD_FOR_INDEX] - row[MISC_PRICE_PAID_INDEX])
				else:
					other_misc_gross += row[MISC_SOLD_FOR_INDEX]
					other_misc_net += (row[MISC_SOLD_FOR_INDEX] - row[MISC_PRICE_PAID_INDEX])
                stats_to_return = [new_vinyl_gross, used_vinyl_gross, new_vinyl_net, used_vinyl_net, clothing_misc_gross, clothing_misc_net, other_misc_gross, other_misc_net]
                
                                        
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
		print '\n'

                return stats_to_return


if __name__ == '__main__':
	util = Util(sys.argv[1])
	entered = ''
	while(entered != 'q' and entered != 'quit'):
		entered = raw_input('plaid-room-util > ')
		if entered == 'h' or entered == 'help':
			print '\nh(elp) - display this message'
			print 's(ummary) - display summary of past week'
			print 'd(ay) - display summary of single day'
                        print 'r(ange) - display summary stats for a range\n'
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
                        util.best_sellers()
                
                        
