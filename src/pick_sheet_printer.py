#!/usr/bin/python

from reportlab.graphics.barcode import code39, eanbc
from reportlab.lib.pagesizes import A4
from reportlab.lib.units import mm
from reportlab.pdfgen import canvas
import reportlab
import locale
import subprocess
from config_stuff import *

class PickSheetPrinter():
    def __init__(self):
        self.file = PICK_SHEET_FILE_NAME
        locale.setlocale( locale.LC_ALL, '')

    def print_pick_sheet(self, code, name, shopify_id, total_items, details, order_no):
        c = canvas.Canvas(self.file, pagesize=(62 * mm, 90 * mm))

        code_picture = reportlab.graphics.barcode.createBarcodeDrawing('Code128', value=code, barHeight=6*mm,width=42*mm,humanReadable=True)

        c.saveState()
        c.rotate(-90)
        c.setFont('Courier', 16)
        c.drawString(-88*mm,11*mm,name)
        c.drawString(-88*mm,2*mm,order_no)
        c.restoreState()

        code_picture.drawOn(c, 20*mm, 2*mm)
        c.showPage()
        c.save()
        
