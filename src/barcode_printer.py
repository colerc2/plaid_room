#!/usr/bin/python

from reportlab.graphics.barcode import code39, eanbc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
import locale
import subprocess

class BarcodePrinter():
    def __init__(self):
        self.file = '/Users/plaidroomrecords/Desktop/barcode_test.pdf'
        locale.setlocale( locale.LC_ALL, '')

    def print_barcode(self, code, artist, title, price):
        print price
        c = canvas.Canvas(self.file, pagesize=(62 * mm, 29 * mm))

        if code.isdigit():
            code = '%013d' % int(code)
            code = reportlab.graphics.barcode.createBarcodeDrawing('EAN13',value=code,barHeight=10*mm,width=60*mm)
        else:
            code = reportlab.graphics.barcode.createBarcodeDrawing('Code128',value=code,barHeight=8*mm,width=60*mm,humanReadable=True)
        
        code.drawOn(c,1*mm, 3*mm)
        c.setFont('Courier', 8)
        artist = artist[0:22]
        title = title[0:22]
        c.drawString(2*mm, 19*mm,artist)#19
        c.drawString(2*mm, 16*mm,title)#16
        c.setFont('Courier',16)
        c.drawString(40*mm, 16*mm, locale.currency(price))
        
        c.showPage()
        c.save()

        #make call to subprocess to talk to CUPS to print this shiz on the printer
        command = 'lp -d Brother_QL_700 -o media=Custom.62x25mm /Users/plaidroomrecords/Desktop/barcode_test.pdf'
        subprocess.call(command, shell=True)
        
        
if __name__ == '__main__':
    barcode_maker = BarcodePrinter()
    
