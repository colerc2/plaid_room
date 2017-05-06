#!/usr/bin/python

from reportlab.graphics.barcode import code39, eanbc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
import locale
import subprocess
import datetime
from config_stuff import *
import math

CHARS_IN_A_LINE = 36

class ReceiptPrinter():
    def __init__(self, temp_receipt_file):
        self.file = temp_receipt_file
        locale.setlocale( locale.LC_ALL, '')
        
    def print_receipt(self, items, misc_items, transaction):
        footer = 30
        lines = []
        #sub-header
        lines.append(['-----------------------------------',True])
        lines.append(['Transaction #%06d' % transaction[TRANS_ID_INDEX],True])
        date_sold = (datetime.datetime.strptime(str(transaction[TRANS_DATE_SOLD_INDEX]),"%Y-%m-%d %H:%M:%S"))
        lines.append(['%s' % date_sold.strftime("%A %b %d, %Y %I:%M %p"),True])
        lines.append(['-----------------------------------',True])
        #items
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
            #if this item is tax exempt, make a note of this on receipt
            if item[TAXABLE_INDEX] == 0:
                temp = '    (Tax-exempt)'
                lines.append([temp,False])
        #misc items
        for item in misc_items:
            if 'PRRGC' in item[MISC_UPC_INDEX]:#gift cards exception, man these are annoying
                temp  = 'Gift Card - %s' % item[MISC_UPC_INDEX]
                price = locale.currency(item[MISC_SOLD_FOR_INDEX])
                spaces_to_add = CHARS_IN_A_LINE - len(price) - len(temp)
                temp += (' '*spaces_to_add) + price
                lines.append([temp, False])
            else:
                temp = '%s - %s' % (item[MISC_ITEM_INDEX], item[MISC_DESCRIPTION_INDEX])
                if len(temp) < 25: #fill in the price at the end of the line
                    price = locale.currency(item[MISC_PRICE_INDEX])
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
                    price = locale.currency(item[MISC_PRICE_INDEX])
                    spaces_to_add = CHARS_IN_A_LINE - len(price) - len(second_line)
                    second_line += (' '*spaces_to_add) + price
                    lines.append([first_line,False])
                    lines.append([second_line,False])
                #if there was a discount, add this to receipt
                if item[MISC_PERCENT_DISCOUNT_INDEX] != 0:
                    temp = ('    - %d%%' % int(item[MISC_PERCENT_DISCOUNT_INDEX]))
                    price = locale.currency(item[MISC_PRICE_INDEX] - item[MISC_SOLD_FOR_INDEX])
                    price = '-' + price
                    spaces_to_add = CHARS_IN_A_LINE - len(temp) - len(price)
                    temp += (' '*spaces_to_add) + price
                    lines.append([temp, False])
            #if this item is tax exempt, make a note of this on receipt
            if item[MISC_TAXABLE_INDEX] == 0:
                temp = '    (Tax-exempt)'
                lines.append([temp,False])
                
        break_between_items_and_total = ' '*28 + '-'*8
        lines.append([break_between_items_and_total,False])
        #subtotal
        total = (' '*13) + 'Subtotal'
        price = locale.currency(transaction[TRANS_SUBTOTAL_INDEX])
        spaces_to_add = CHARS_IN_A_LINE - len(total) - len(price)
        total = total + (' '*spaces_to_add) + price
        lines.append([total,False])
        #discount (if necessary)
        if(transaction[TRANS_DISCOUNT_PERCENT_INDEX] != 0):
            discount = (' '*13) + ('-%d%%' % transaction[TRANS_DISCOUNT_PERCENT_INDEX])
            price = '-' + locale.currency(transaction[TRANS_SUBTOTAL_INDEX]-transaction[TRANS_DISCOUNTED_PRICE_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(discount) - len(price)
            discount += (' '*spaces_to_add) + price
            lines.append([discount,False])
            #after discount
            total = (' '*13) + 'After Discount'
            price = locale.currency(transaction[TRANS_DISCOUNTED_PRICE_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(total) - len(price)
            total = total + (' '*spaces_to_add) + price
            lines.append([total,False])
        #tax
        tax = (' '*13) + 'Tax @ 6.75%'
        price = locale.currency(transaction[TRANS_TAX_INDEX])
        spaces_to_add = CHARS_IN_A_LINE - len(tax) - len(price)
        tax = tax + (' '*spaces_to_add) + price
        lines.append([tax,False])
        #shipping
        if(transaction[TRANS_SHIPPING_INDEX] != 0):
            shipping = (' '*13) + 'Shipping'
            price = locale.currency(transaction[TRANS_SHIPPING_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(shipping) - len(price)
            shipping = shipping + (' '*spaces_to_add) + price
            lines.append([shipping,False])
        #total
        total = (' '*13) + 'Total'
        price = locale.currency(transaction[TRANS_TOTAL_INDEX])
        spaces_to_add = CHARS_IN_A_LINE - len(total) - len(price)
        total = total + (' '*spaces_to_add) + price
        lines.append([total,False])        
        #split between totals and transaction
        lines.append(['-----------------------------------',True])
        #cash or credit
        if transaction[TRANS_CASH_CREDIT_INDEX] == 'Cash':
            tendered = (' '*13) + 'Cash Tendered'
            price = locale.currency(transaction[TRANS_TENDERED_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(tendered) - len(price)
            tendered = tendered + (' '*spaces_to_add) + price
            lines.append([tendered,False])
            change = (' '*13) + 'Change Due'
            price = locale.currency(transaction[TRANS_CHANGE_INDEX])
            spaces_to_add = CHARS_IN_A_LINE - len(change) - len(price)
            change = change + (' '*spaces_to_add) + price
            lines.append([change,False])
        elif transaction[TRANS_CASH_CREDIT_INDEX] == 'Credit':
            todo = 0
        else:
            print 'something went wrong'
        lines.append(['-----------------------------------',True])
        lines.append(['Have a great day!',True])
        #lines.append(['HAPPY RECORD STORE DAY!', True])
        #lines.append(['<3 <3 <3 <3 <3 <3 <3 <3 ', True])
        #lines.append(['Thanks for stopping in', True])
        #lines.append(['on record store day!! Be', True])
        #lines.append(['sure to visit Cappy\'s', True])
        #lines.append(['to try our collaboration beers', True])
        #lines.append(['with Madtree! Also, show this', True])
        #lines.append(['receipt at Paxton\'s for $1', True])
        #lines.append(['off pints of Great Lakes', True])
        #lines.append(['Turntable Pils! Cheers!!!', True])
        #lines.append(['', True])
        #lines.append(['', True])
        #lines.append(['Thanks for stopping in', True])
        #lines.append(['on record store day!! Show', True])
        #lines.append(['this receipt at Cappy\'s for', True])
        #lines.append(['$2 off Dogfish Head Growler fills', True])
        #lines.append(['and a chance to win an exclusive', True])
        #lines.append(['Dogfish Head turntable!', True])
        #lines.append(['Hope to see you again soon!',True])
        
            
        canvas_size = 40 + 4*len(lines) + footer
            

        
        c = canvas.Canvas(self.file,pagesize=(80 * mm, canvas_size * mm))

        c.setFont('Courier', 9)
        c.drawImage(RECEIPT_HEADER_FILE_NAME,2*mm,(canvas_size-110)*mm,width=70*mm,preserveAspectRatio=True)
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
        command = 'lp -d EPSON_TM_T20 -o media=Custom.80x%dmm %s' % (canvas_size, TEMP_RECEIPT_FILE_NAME)
        subprocess.call(command, shell=True)

        
    if __name__ == '__main__':
        receipt_maker = ReceiptPrinter()
