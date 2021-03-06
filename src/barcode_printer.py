#!/usr/bin/python

from reportlab.graphics.barcode import code39, eanbc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
import locale
import subprocess
from config_stuff import *

class BarcodePrinter():
    def __init__(self):
        self.file = '/Users/plaidroomrecords/Desktop/barcode_test.pdf'
        locale.setlocale( locale.LC_ALL, '')

    
        
    def print_barcode(self, code, artist, title, price, genre, new_used):
        c = canvas.Canvas(self.file, pagesize=(62 * mm, 29 * mm))
        code_copy = code #this is terrible i hate myself
        
        if code.isdigit():
            code = '%013d' % int(code)
            code = reportlab.graphics.barcode.createBarcodeDrawing('EAN13',value=code,barHeight=8*mm,width=49*mm)
        else:
            code = reportlab.graphics.barcode.createBarcodeDrawing('Code128',value=code,barHeight=5*mm,width=49*mm,humanReadable=True)
        
        code.drawOn(c,12*mm, 3*mm)
        c.drawImage(BABY_LOGO_FILE_NAME, 2*mm,-24*mm,width=9*mm,preserveAspectRatio=True)
        #c.drawImage(BABY_LOGO_FILE_NAME, 1*mm,-14*mm,preserveAspectRatio=True)
        c.setFont('Courier', 8)
        artist = artist[0:22]
        title = title[0:22]
        c.drawString(2*mm, 19*mm,artist)#19
        c.drawString(2*mm, 16*mm,title)#16
        #if new_used == 'Used':
        filtered_genre = genre.replace("Folk, World, & Country", "FWC")
        c.drawString(2*mm, 13*mm,filtered_genre)#13
        c.setFont('Courier',16)
        if 'PRRGC' not in code_copy:
            if price > 99.99:
                c.drawString(37*mm, 17*mm, locale.currency(price))
            else:
                c.drawString(40*mm, 17*mm, locale.currency(price))
        c.showPage()
        c.save()

        #make call to subprocess to talk to CUPS to print this shiz on the printer
        command = 'lp -d Brother_QL_700 -o media=Custom.62x25mm /Users/plaidroomrecords/Desktop/barcode_test.pdf'
        subprocess.call(command, shell=True)
        
        
if __name__ == '__main__':
    barcode_maker = BarcodePrinter()
    
