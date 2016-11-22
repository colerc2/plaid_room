#!/usr/bin/python

from reportlab.graphics.barcode import code39, eanbc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
import locale
import subprocess
from config_stuff import *
import datetime

class PickSheetPrinter():
    def __init__(self):
        self.file = PICK_SHEET_FILE_NAME
        locale.setlocale( locale.LC_ALL, '')

    def print_pick_sheet(self, code, name, shopify_id, total_items, order_no, upc, artist, title, date_sold, shipping_method, total_price, item_price, pre_order, pre_order_date):
        c = canvas.Canvas(self.file, pagesize=(62 * mm, 90 * mm))

        code_picture = reportlab.graphics.barcode.createBarcodeDrawing('Code128', value=code, barHeight=6*mm,width=42*mm,humanReadable=True)
        upc_picture = ''
        if upc.isdigit():
            upc = '%013d' % int(upc)
            upc_picture = reportlab.graphics.barcode.createBarcodeDrawing('EAN13',value=upc,barHeight=6*mm,width=42*mm)
        else:
            upc_picture = reportlab.graphics.barcode.createBarcodeDrawing('Code128',value=upc,barHeight=6*mm,width=42*mm,humanReadable=True)

        c.saveState()
        c.rotate(-90)
        c.setFont('Courier', 20)
        c.drawString(-88*mm,10*mm,name)
        c.drawString(-88*mm,2*mm,order_no)
        c.restoreState()
        c.setFont('Courier', 9)
        lines_to_print = []
        lines_to_print.append('Artist: %s' % artist)
        lines_to_print.append('Title: %s' % title)
        lines_to_print.append('Price: %s' % locale.currency(item_price))
        lines_to_print.append('Total Items: %s' % int(total_items))
        lines_to_print.append('Total Price: %s' % locale.currency(total_price))
        lines_to_print.append('Date: %s' % str((datetime.datetime.strptime(str(date_sold), "%Y-%m-%d %H:%M:%S")).date()))
        lines_to_print.append('Ship: %s' % shipping_method)
        if pre_order == 1:
            lines_to_print.append('PRE-ORDER')
            lines_to_print.append('STREET DATE')
            lines_to_print.append('%s' % pre_order_date)

        y_pos = 76
        for line in lines_to_print:
            c.drawString(20*mm, y_pos*mm, line)
            y_pos -= 4
        
            
        code_picture.drawOn(c, 20*mm, 2*mm)
        upc_picture.drawOn(c, 20*mm, 80*mm)
        c.showPage()
        c.save()
        
        #make call to subprocess to talk to CUPS to print this shiz on the printer
        command = 'lp -d Brother_QL_700 -o media=Custom.62x90mm %s' % PICK_SHEET_FILE_NAME
        subprocess.call(command, shell=True)
