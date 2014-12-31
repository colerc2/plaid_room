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
        self.locale.setlocale( locale.LC_ALL, '')

    def print_barcode(self, code, artist, title, price):
        c = canvas.Canvas('/Users/plaidroomrecords/Desktop/barcode_test.pdf', pagesize=(62 * mm, 29 * mm))

        #upca sucks so i convert to ean13
        code = '0' + code
        code = reportlab.graphics.barcode.createBarcodeDrawing('EAN13',value=code,barHeight=10*mm,width=60*mm)
        
        code.drawOn(c,1*mm, 3*mm)
        c.setFont('Helvetica', 8)
        artist = artist[0:25]
        title = title[0:25]
        c.drawString(2*mm, 19*mm,artist)
        c.drawString(2*mm, 16*mm,title)
        c.setFont('Helvetica',18)
        c.drawString(40*mm, 16*mm, locale.currency(price))
        
        c.showPage()
        c.save()

        #make call to subprocess to talk to CUPS to print this shiz on the printer
        command = 'lp -d Brother_QL_700 -o media=Custom.62x25mm /Users/plaidroomrecords/Desktop/barcode_test.pdf'
        subprocess.call(command, shell=True)
        
        
if __name__ == '__main__':
    barcode_maker = BarcodePrinter()
    
