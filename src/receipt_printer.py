#!/usr/bin/python

from reportlab.graphics.barcode import code39, eanbc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
import locale
import subprocess
import datetime

UPC_INDEX = 0
ARTIST_INDEX = 1
TITLE_INDEX = 2
FORMAT_INDEX = 3
PRICE_INDEX = 4
PRICE_PAID_INDEX = 5
NEW_USED_INDEX = 6
DISTRIBUTOR_INDEX = 7
LABEL_INDEX = 8
GENRE_INDEX = 9
YEAR_INDEX = 10
DATE_ADDED_INDEX = 11
DISCOGS_RELEASE_NUMBER_INDEX = 12
REAL_NAME_INDEX = 13
PROFILE_INDEX = 14
VARIATIONS_INDEX = 15
ALIASES_INDEX = 16
TRACK_LIST_INDEX = 17
NOTES_INDEX = 18
ID_INDEX = 19
SOLD_FOR_INDEX = 20
PERCENT_DISCOUNT_INDEX = 21
DATE_SOLD_INDEX = 22
SOLD_NOTES_INDEX = 23
REORDER_STATE = 24
TRANSACTION_ID_INDEX = 25
NEW_ID_INDEX = 26

TRANS_NUM_ITEMS_INDEX = 0
TRANS_DATE_SOLD_INDEX = 1
TRANS_SUBTOTAL_INDEX = 2
TRANS_DISCOUNT_INDEX = 3
TRANS_DISCOUNTED_PRICE_INDEX = 4
TRANS_TAX_INDEX = 5
TRANS_SHIPPING_INDEX = 6
TRANS_TOTAL_INDEX = 7
TRANS_CASH_CREDIT_INDEX = 8
TRANS_SOLD_IDS_INDEX = 9
TRANS_ID_INDEX = 10


class ReceiptPrinter():
    def __init__(self):
        self.file = '/Users/plaidroomrecords/Desktop/receipt_test.pdf'
        locale.setlocale( locale.LC_ALL, '')
        
    def print_receipt(self, items, transaction):
        footer = 30
        lines = []
        #first loop through and find out how many lines we'll need, this will determine the size of the canvas
        lines.append(['-----------------------------------',True])
        lines.append(['Transaction #%06d' % transaction[TRANS_ID_INDEX],True])
        date_sold = (datetime.datetime.strptime(str(transaction[TRANS_DATE_SOLD_INDEX]),"%Y-%m-%d %H:%M:%S"))
        lines.append(['%s' % date_sold.strftime("%A %b %d, %Y %I:%M %p"),True])
        lines.append(['-----------------------------------',True])
        #36
        CHARS_IN_A_LINE = 36
        for item in items:
            temp = '%s - %s' % (item[ARTIST_INDEX], item[TITLE_INDEX])
            if len(temp) < 25: #fill in the price at the end of the line
                price = locale.currency(item[PRICE_INDEX])
                spaces_to_add = CHARS_IN_A_LINE - len(price) - len(temp)
                temp += (' '*spaces_to_add) + price
                lines.append([temp, False])
            else:
                #start grabbing words off of the end until it's less than 25
                split_temp = temp.split(' ')
                first_line = ''
                second_line = '    '
                for word in split_temp:
                    if (len(first_line)+len(word)+1) < 25:
                        first_line  = first_line + word + ' '
                    else:
                        second_line = second_line + word + ' '
                second_line = second_line[0:25]
                price = locale.currency(item[PRICE_INDEX])
                spaces_to_add = CHARS_IN_A_LINE - len(price) - len(second_line)
                second_line += (' '*spaces_to_add) + price
                lines.append([first_line,False])
                lines.append([second_line,False])
            #if there was a discount, add this to receipt
            if item[PERCENT_DISCOUNT_INDEX] != 0:
                temp = ('    - %d%%' % int(item[PERCENT_DISCOUNT_INDEX]))
                price = locale.currency(item[PRICE_INDEX] - item[SOLD_FOR_INDEX])
                price = '-' + price
                spaces_to_add = CHARS_IN_A_LINE - len(temp) - len(price)
                temp += (' '*spaces_to_add) + price
                lines.append([temp, False])

        break_between_items_and_total = ' '*28 + '-'*8
        lines.append([break_between_items_and_total,False])
        #subtotal
        total = (' '*13) + 'Subtotal'
        price = locale.currency(transaction[TRANS_SUBTOTAL_INDEX])
        spaces_to_add = CHARS_IN_A_LINE - len(total) - len(price)
        total = total + (' '*spaces_to_add) + price
        lines.append([total,False])
        #discount (if necessary)
        if(transaction[TRANS_DISCOUNT_INDEX] != 0):
            discount = (' '*13) + ('-%d%%' % transaction[TRANS_DISCOUNT_INDEX])
            price = '-' + locale.currency(transaction[TRANS_SUBTOTAL_INDEX]-transaction[TRANS_DISCOUNTED_PRICE_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(discount) - len(price)
            discount += (' '*spaces_to_add) + price
            lines.append([discount,False])
            #after discount
            total = (' '*13) + 'New Subtotal'
            price = locale.currency(transaction[TRANS_DISCOUNTED_PRICE_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(total) - len(price)
            total = total + (' '*spaces_to_add) + price
            lines.append([total,False])
        #tax
        tax = (' '*13) + 'Tax @ 7%'
        price = locale.currency(transaction[TRANS_TAX_INDEX])
        spaces_to_add = CHARS_IN_A_LINE - len(tax) - len(price)
        tax = tax + (' '*spaces_to_add) + price
        lines.append([tax,False])
        #total
        total = (' '*13) + 'Total'
        price = locale.currency(transaction[TRANS_TOTAL_INDEX])
        spaces_to_add = CHARS_IN_A_LINE - len(total) - len(price)
        total = total + (' '*spaces_to_add) + price
        lines.append([total,False])        
        #split between totals and transaction
        lines.append(['-----------------------------------',True])
        if transaction[TRANS_CASH_CREDIT_INDEX] == 'Cash':
            todo = 0
        elif transaction[TRANS_CASH_CREDIT_INDEX] == 'Credit':
            todo = 0
        else:
            print 'something went wrong'
        
        canvas_size = 40 + 4*len(lines) + footer
            

        
        c = canvas.Canvas(self.file,pagesize=(80 * mm, canvas_size * mm))

        c.setFont('Courier', 9)
        c.drawImage('/Users/plaidroomrecords/Desktop/plaid_room.jpg',2*mm,(canvas_size-110)*mm,width=70*mm,preserveAspectRatio=True)
        y_pos = canvas_size - 55
        for line in lines:
            if line[1]:
                c.drawCentredString(37*mm, y_pos*mm, line[0])
            else:
                c.drawString(2*mm, y_pos*mm, line[0])
            y_pos -= 4

        #trick printer into going down on me
        y_pos -= 10
        c.drawString(79*mm, y_pos*mm, '.')

        #save
        c.showPage()
        c.save()

        #make call to subprocess to talk to CUPS to print her
        command = 'lp -d EPSON_TM_T20 -o media=Custom.80x%dmm /Users/plaidroomrecords/Desktop/receipt_test.pdf' % canvas_size
        subprocess.call(command, shell=True)

        
    if __name__ == '__main__':
        receipt_maker = ReceiptPrinter()
