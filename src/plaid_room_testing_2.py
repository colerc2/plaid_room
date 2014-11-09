# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/plaid_room.ui'
#
# Created: Sat Nov  8 05:01:22 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import os
import discogs_client
from discogs_interface import DiscogsClient
from more_info_dialog import Ui_more_info_dialog
from cash_dialog import Ui_CashDialog
import time
import datetime
import sqlite3
import re
import string
from threading import Thread


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
TRANSACTION_ID_INDEX = 24
NEW_ID_INDEX = 25

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

try:
    _fromUtf8 = QtCore.QString.fromUtf8
except AttributeError:
    def _fromUtf8(s):
        return s

try:
    _encoding = QtGui.QApplication.UnicodeUTF8
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig, _encoding)
except AttributeError:
    def _translate(context, text, disambig):
        return QtGui.QApplication.translate(context, text, disambig)

class Ui_Form(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        #self.thread().setPriority(QtCore.QThread.TimeCriticalPriority)
        self.thread().setPriority(QtCore.QThread.HighestPriority)

        #declare global stuff here?
        self.discogs = DiscogsClient()
        self.checkout_list = []
        self.search_list = []
        self.checkout_subtotal = 0
        self.checkout_discount = 0
        self.checkout_shipping = 0
        self.checkout_total = 0

        #DB stuff
        self.db = sqlite3.connect('inventory.db')
        self.db_cursor = self.db.cursor()
        #store previous set of results
        self.previous_results = None
        #create inventory table
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS inventory
        (upc text, artist text, title text, format text, price real, price_paid real, new_used text, distributor text, label text, genre text, year integer, date_added text, discogs_release_number integer, real_name text, profile text, variations text, aliases text, track_list text, notes text, id integer primary key autoincrement)
        """)
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS sold_inventory
        (upc text, artist text, title text, format text, price real, price_paid real, new_used text, distributor text, label text, genre text, year integer, date_added text, discogs_release_number integer, real_name text, profile text, variations text, aliases text, track_list text, notes text, inventory_id integer, sold_for real, percent_discount real, date_sold text, sold_notes text, transaction_id integer, id integer primary key autoincrement)
        """)
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS sold_transactions
        (number_of_items integer, date_sold text, subtotal real, discount_percent real, discounted_price real, tax real, shipping real, total real, cash_credit text, sold_ids text, id integer primary key autoincrement)
        """)

        
        self.num_attributes = 19
        self.combobox_cols = [6,7]
        
        self.setupUi(self)

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1920, 1018)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(1920, 1050))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.main_menu_tabs = QtGui.QTabWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.main_menu_tabs.sizePolicy().hasHeightForWidth())
        self.main_menu_tabs.setSizePolicy(sizePolicy)
        self.main_menu_tabs.setMinimumSize(QtCore.QSize(0, 0))
        self.main_menu_tabs.setMaximumSize(QtCore.QSize(1900, 1000))
        self.main_menu_tabs.setTabPosition(QtGui.QTabWidget.North)
        self.main_menu_tabs.setIconSize(QtCore.QSize(16, 16))
        self.main_menu_tabs.setObjectName(_fromUtf8("main_menu_tabs"))
        self.add_inventory_tab = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_inventory_tab.sizePolicy().hasHeightForWidth())
        self.add_inventory_tab.setSizePolicy(sizePolicy)
        self.add_inventory_tab.setObjectName(_fromUtf8("add_inventory_tab"))
        self.layoutWidget = QtGui.QWidget(self.add_inventory_tab)
        self.layoutWidget.setGeometry(QtCore.QRect(0, 0, 1876, 961))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout_3 = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout_3.setMargin(0)
        self.verticalLayout_3.setObjectName(_fromUtf8("verticalLayout_3"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.tab_one_search_item_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_search_item_lbl.setFont(font)
        self.tab_one_search_item_lbl.setScaledContents(False)
        self.tab_one_search_item_lbl.setObjectName(_fromUtf8("tab_one_search_item_lbl"))
        self.horizontalLayout_2.addWidget(self.tab_one_search_item_lbl)
        spacerItem = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem)
        self.add_item_vert_line = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line.setObjectName(_fromUtf8("add_item_vert_line"))
        self.horizontalLayout_2.addWidget(self.add_item_vert_line)
        spacerItem1 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem1)
        self.tab_one_vinyl_radio_button = QtGui.QRadioButton(self.layoutWidget)
        self.tab_one_vinyl_radio_button.setChecked(True)
        self.tab_one_vinyl_radio_button.setObjectName(_fromUtf8("tab_one_vinyl_radio_button"))
        self.horizontalLayout_2.addWidget(self.tab_one_vinyl_radio_button)
        self.tab_one_cd_radio_button = QtGui.QRadioButton(self.layoutWidget)
        self.tab_one_cd_radio_button.setObjectName(_fromUtf8("tab_one_cd_radio_button"))
        self.horizontalLayout_2.addWidget(self.tab_one_cd_radio_button)
        self.tab_one_any_radio_button = QtGui.QRadioButton(self.layoutWidget)
        self.tab_one_any_radio_button.setObjectName(_fromUtf8("tab_one_any_radio_button"))
        self.horizontalLayout_2.addWidget(self.tab_one_any_radio_button)
        spacerItem2 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem2)
        self.add_item_vert_line_27 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_27.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_27.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_27.setObjectName(_fromUtf8("add_item_vert_line_27"))
        self.horizontalLayout_2.addWidget(self.add_item_vert_line_27)
        spacerItem3 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem3)
        self.tab_one_search_upc_qline = QtGui.QLineEdit(self.layoutWidget)
        self.tab_one_search_upc_qline.setObjectName(_fromUtf8("tab_one_search_upc_qline"))
        self.horizontalLayout_2.addWidget(self.tab_one_search_upc_qline)
        self.tab_one_search_upc_button = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_search_upc_button.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_search_upc_button.setObjectName(_fromUtf8("tab_one_search_upc_button"))
        self.horizontalLayout_2.addWidget(self.tab_one_search_upc_button)
        spacerItem4 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem4)
        self.add_item_vert_line_2 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_2.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_2.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_2.setObjectName(_fromUtf8("add_item_vert_line_2"))
        self.horizontalLayout_2.addWidget(self.add_item_vert_line_2)
        spacerItem5 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem5)
        self.tab_one_search_artist_title_title_qline = QtGui.QLineEdit(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_search_artist_title_title_qline.sizePolicy().hasHeightForWidth())
        self.tab_one_search_artist_title_title_qline.setSizePolicy(sizePolicy)
        self.tab_one_search_artist_title_title_qline.setMinimumSize(QtCore.QSize(250, 0))
        self.tab_one_search_artist_title_title_qline.setText(_fromUtf8(""))
        self.tab_one_search_artist_title_title_qline.setObjectName(_fromUtf8("tab_one_search_artist_title_title_qline"))
        self.horizontalLayout_2.addWidget(self.tab_one_search_artist_title_title_qline)
        self.tab_one_search_artist_title_button = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_search_artist_title_button.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_search_artist_title_button.setObjectName(_fromUtf8("tab_one_search_artist_title_button"))
        self.horizontalLayout_2.addWidget(self.tab_one_search_artist_title_button)
        spacerItem6 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem6)
        self.add_item_vert_line_4 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_4.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_4.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_4.setObjectName(_fromUtf8("add_item_vert_line_4"))
        self.horizontalLayout_2.addWidget(self.add_item_vert_line_4)
        spacerItem7 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem7)
        self.tab_one_clear_all_button = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_clear_all_button.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_clear_all_button.setObjectName(_fromUtf8("tab_one_clear_all_button"))
        self.horizontalLayout_2.addWidget(self.tab_one_clear_all_button)
        spacerItem8 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_2.addItem(spacerItem8)
        self.verticalLayout_3.addLayout(self.horizontalLayout_2)
        self.tab_one_results_table = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_results_table.sizePolicy().hasHeightForWidth())
        self.tab_one_results_table.setSizePolicy(sizePolicy)
        self.tab_one_results_table.setMinimumSize(QtCore.QSize(1850, 380))
        self.tab_one_results_table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tab_one_results_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tab_one_results_table.setObjectName(_fromUtf8("tab_one_results_table"))
        self.tab_one_results_table.setColumnCount(13)
        self.tab_one_results_table.setRowCount(15)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table.setItem(0, 2, item)
        self.tab_one_results_table.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_one_results_table.horizontalHeader().setDefaultSectionSize(100)
        self.tab_one_results_table.horizontalHeader().setSortIndicatorShown(False)
        self.tab_one_results_table.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout_3.addWidget(self.tab_one_results_table)
        self.horizontalLayout_7 = QtGui.QHBoxLayout()
        self.horizontalLayout_7.setObjectName(_fromUtf8("horizontalLayout_7"))
        self.horizontalLayout_6 = QtGui.QHBoxLayout()
        self.horizontalLayout_6.setObjectName(_fromUtf8("horizontalLayout_6"))
        self.tab_one_add_item_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_add_item_lbl.setFont(font)
        self.tab_one_add_item_lbl.setScaledContents(False)
        self.tab_one_add_item_lbl.setObjectName(_fromUtf8("tab_one_add_item_lbl"))
        self.horizontalLayout_6.addWidget(self.tab_one_add_item_lbl)
        spacerItem9 = QtGui.QSpacerItem(70, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem9)
        self.add_item_vert_line_7 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_7.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_7.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_7.setObjectName(_fromUtf8("add_item_vert_line_7"))
        self.horizontalLayout_6.addWidget(self.add_item_vert_line_7)
        spacerItem10 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem10)
        self.tab_one_add_selected_to_inventory = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_add_selected_to_inventory.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_add_selected_to_inventory.setObjectName(_fromUtf8("tab_one_add_selected_to_inventory"))
        self.horizontalLayout_6.addWidget(self.tab_one_add_selected_to_inventory)
        self.tab_one_print_sticker_check_box = QtGui.QCheckBox(self.layoutWidget)
        self.tab_one_print_sticker_check_box.setChecked(True)
        self.tab_one_print_sticker_check_box.setObjectName(_fromUtf8("tab_one_print_sticker_check_box"))
        self.horizontalLayout_6.addWidget(self.tab_one_print_sticker_check_box)
        spacerItem11 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem11)
        self.add_item_vert_line_8 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_8.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_8.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_8.setObjectName(_fromUtf8("add_item_vert_line_8"))
        self.horizontalLayout_6.addWidget(self.add_item_vert_line_8)
        spacerItem12 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_6.addItem(spacerItem12)
        self.tab_one_generate_sku_button = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_generate_sku_button.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_generate_sku_button.setObjectName(_fromUtf8("tab_one_generate_sku_button"))
        self.horizontalLayout_6.addWidget(self.tab_one_generate_sku_button)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_6)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.add_item_vert_line_13 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_13.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_13.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_13.setObjectName(_fromUtf8("add_item_vert_line_13"))
        self.horizontalLayout_3.addWidget(self.add_item_vert_line_13)
        spacerItem13 = QtGui.QSpacerItem(413, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_3.addItem(spacerItem13)
        self.horizontalLayout_7.addLayout(self.horizontalLayout_3)
        self.verticalLayout_3.addLayout(self.horizontalLayout_7)
        self.line = QtGui.QFrame(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Helvetica"))
        font.setPointSize(24)
        font.setItalic(True)
        self.line.setFont(font)
        self.line.setFrameShadow(QtGui.QFrame.Plain)
        self.line.setLineWidth(3)
        self.line.setMidLineWidth(0)
        self.line.setFrameShape(QtGui.QFrame.HLine)
        self.line.setFrameShadow(QtGui.QFrame.Sunken)
        self.line.setObjectName(_fromUtf8("line"))
        self.verticalLayout_3.addWidget(self.line)
        self.horizontalLayout_15 = QtGui.QHBoxLayout()
        self.horizontalLayout_15.setObjectName(_fromUtf8("horizontalLayout_15"))
        self.verticalLayout = QtGui.QVBoxLayout()
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_8 = QtGui.QHBoxLayout()
        self.horizontalLayout_8.setSizeConstraint(QtGui.QLayout.SetDefaultConstraint)
        self.horizontalLayout_8.setObjectName(_fromUtf8("horizontalLayout_8"))
        self.tab_one_recent_additions_lbl = QtGui.QLabel(self.layoutWidget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_recent_additions_lbl.setFont(font)
        self.tab_one_recent_additions_lbl.setScaledContents(False)
        self.tab_one_recent_additions_lbl.setObjectName(_fromUtf8("tab_one_recent_additions_lbl"))
        self.horizontalLayout_8.addWidget(self.tab_one_recent_additions_lbl)
        spacerItem14 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem14)
        self.add_item_vert_line_9 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_9.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_9.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_9.setObjectName(_fromUtf8("add_item_vert_line_9"))
        self.horizontalLayout_8.addWidget(self.add_item_vert_line_9)
        spacerItem15 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem15)
        self.tab_one_remove_selected_item_from_inventory = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_remove_selected_item_from_inventory.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_remove_selected_item_from_inventory.setObjectName(_fromUtf8("tab_one_remove_selected_item_from_inventory"))
        self.horizontalLayout_8.addWidget(self.tab_one_remove_selected_item_from_inventory)
        spacerItem16 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem16)
        self.add_item_vert_line_14 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_14.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_14.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_14.setObjectName(_fromUtf8("add_item_vert_line_14"))
        self.horizontalLayout_8.addWidget(self.add_item_vert_line_14)
        spacerItem17 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem17)
        self.tab_one_edit_selected_item = QtGui.QPushButton(self.layoutWidget)
        self.tab_one_edit_selected_item.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_one_edit_selected_item.setObjectName(_fromUtf8("tab_one_edit_selected_item"))
        self.horizontalLayout_8.addWidget(self.tab_one_edit_selected_item)
        spacerItem18 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem18)
        self.add_item_vert_line_28 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_28.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_28.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_28.setObjectName(_fromUtf8("add_item_vert_line_28"))
        self.horizontalLayout_8.addWidget(self.add_item_vert_line_28)
        spacerItem19 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_8.addItem(spacerItem19)
        self.tab_one_num_inventory_label = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_num_inventory_label.sizePolicy().hasHeightForWidth())
        self.tab_one_num_inventory_label.setSizePolicy(sizePolicy)
        self.tab_one_num_inventory_label.setMinimumSize(QtCore.QSize(170, 0))
        self.tab_one_num_inventory_label.setObjectName(_fromUtf8("tab_one_num_inventory_label"))
        self.horizontalLayout_8.addWidget(self.tab_one_num_inventory_label)
        self.verticalLayout.addLayout(self.horizontalLayout_8)
        self.tab_one_recently_added_table = QtGui.QTableWidget(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_recently_added_table.sizePolicy().hasHeightForWidth())
        self.tab_one_recently_added_table.setSizePolicy(sizePolicy)
        self.tab_one_recently_added_table.setMinimumSize(QtCore.QSize(1300, 350))
        self.tab_one_recently_added_table.setAlternatingRowColors(False)
        self.tab_one_recently_added_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tab_one_recently_added_table.setObjectName(_fromUtf8("tab_one_recently_added_table"))
        self.tab_one_recently_added_table.setColumnCount(20)
        self.tab_one_recently_added_table.setRowCount(20)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setHorizontalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_recently_added_table.setItem(0, 0, item)
        self.verticalLayout.addWidget(self.tab_one_recently_added_table)
        self.horizontalLayout_15.addLayout(self.verticalLayout)
        self.verticalLayout_2 = QtGui.QVBoxLayout()
        self.verticalLayout_2.setObjectName(_fromUtf8("verticalLayout_2"))
        self.horizontalLayout_4 = QtGui.QHBoxLayout()
        self.horizontalLayout_4.setObjectName(_fromUtf8("horizontalLayout_4"))
        self.add_item_vert_line_12 = QtGui.QFrame(self.layoutWidget)
        self.add_item_vert_line_12.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_12.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_12.setObjectName(_fromUtf8("add_item_vert_line_12"))
        self.horizontalLayout_4.addWidget(self.add_item_vert_line_12)
        spacerItem20 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem20)
        self.tab_one_console_lbl = QtGui.QLabel(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_console_lbl.sizePolicy().hasHeightForWidth())
        self.tab_one_console_lbl.setSizePolicy(sizePolicy)
        self.tab_one_console_lbl.setMinimumSize(QtCore.QSize(100, 0))
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_console_lbl.setFont(font)
        self.tab_one_console_lbl.setScaledContents(False)
        self.tab_one_console_lbl.setAlignment(QtCore.Qt.AlignCenter)
        self.tab_one_console_lbl.setObjectName(_fromUtf8("tab_one_console_lbl"))
        self.horizontalLayout_4.addWidget(self.tab_one_console_lbl)
        spacerItem21 = QtGui.QSpacerItem(150, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_4.addItem(spacerItem21)
        self.verticalLayout_2.addLayout(self.horizontalLayout_4)
        self.tab_one_text_browser = QtGui.QTextBrowser(self.layoutWidget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_text_browser.sizePolicy().hasHeightForWidth())
        self.tab_one_text_browser.setSizePolicy(sizePolicy)
        self.tab_one_text_browser.setMinimumSize(QtCore.QSize(400, 0))
        self.tab_one_text_browser.setMaximumSize(QtCore.QSize(550, 16777215))
        self.tab_one_text_browser.setAutoFormatting(QtGui.QTextEdit.AutoNone)
        self.tab_one_text_browser.setOverwriteMode(False)
        self.tab_one_text_browser.setObjectName(_fromUtf8("tab_one_text_browser"))
        self.verticalLayout_2.addWidget(self.tab_one_text_browser)
        self.horizontalLayout_15.addLayout(self.verticalLayout_2)
        self.verticalLayout_3.addLayout(self.horizontalLayout_15)
        self.main_menu_tabs.addTab(self.add_inventory_tab, _fromUtf8(""))
        self.search_inventory_tab = QtGui.QWidget()
        self.search_inventory_tab.setObjectName(_fromUtf8("search_inventory_tab"))
        self.layoutWidget1 = QtGui.QWidget(self.search_inventory_tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 3, 1852, 947))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.verticalLayout_7 = QtGui.QVBoxLayout(self.layoutWidget1)
        self.verticalLayout_7.setMargin(0)
        self.verticalLayout_7.setObjectName(_fromUtf8("verticalLayout_7"))
        self.verticalLayout_4 = QtGui.QVBoxLayout()
        self.verticalLayout_4.setSpacing(5)
        self.verticalLayout_4.setObjectName(_fromUtf8("verticalLayout_4"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout()
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.tab_one_search_item_lbl_2 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_search_item_lbl_2.setFont(font)
        self.tab_one_search_item_lbl_2.setScaledContents(False)
        self.tab_one_search_item_lbl_2.setObjectName(_fromUtf8("tab_one_search_item_lbl_2"))
        self.horizontalLayout_5.addWidget(self.tab_one_search_item_lbl_2)
        spacerItem22 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem22)
        self.add_item_vert_line_3 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_3.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_3.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_3.setObjectName(_fromUtf8("add_item_vert_line_3"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_3)
        spacerItem23 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem23)
        self.tab_two_search_artist_title_qline = QtGui.QLineEdit(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_two_search_artist_title_qline.sizePolicy().hasHeightForWidth())
        self.tab_two_search_artist_title_qline.setSizePolicy(sizePolicy)
        self.tab_two_search_artist_title_qline.setMinimumSize(QtCore.QSize(250, 0))
        self.tab_two_search_artist_title_qline.setText(_fromUtf8(""))
        self.tab_two_search_artist_title_qline.setObjectName(_fromUtf8("tab_two_search_artist_title_qline"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_title_qline)
        self.tab_two_search_artist_title_button = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_search_artist_title_button.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_two_search_artist_title_button.setObjectName(_fromUtf8("tab_two_search_artist_title_button"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_title_button)
        spacerItem24 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem24)
        self.add_item_vert_line_6 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_6.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_6.setObjectName(_fromUtf8("add_item_vert_line_6"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_6)
        spacerItem25 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem25)
        self.tab_two_reset_button = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_reset_button.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_two_reset_button.setObjectName(_fromUtf8("tab_two_reset_button"))
        self.horizontalLayout_5.addWidget(self.tab_two_reset_button)
        spacerItem26 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem26)
        self.add_item_vert_line_16 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_16.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_16.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_16.setObjectName(_fromUtf8("add_item_vert_line_16"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_16)
        spacerItem27 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem27)
        self.tab_two_remove_selected_item_from_inventory = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_remove_selected_item_from_inventory.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_two_remove_selected_item_from_inventory.setObjectName(_fromUtf8("tab_two_remove_selected_item_from_inventory"))
        self.horizontalLayout_5.addWidget(self.tab_two_remove_selected_item_from_inventory)
        spacerItem28 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem28)
        self.add_item_vert_line_15 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_15.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_15.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_15.setObjectName(_fromUtf8("add_item_vert_line_15"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_15)
        spacerItem29 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem29)
        self.tab_two_edit_selected_item = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_edit_selected_item.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_two_edit_selected_item.setObjectName(_fromUtf8("tab_two_edit_selected_item"))
        self.horizontalLayout_5.addWidget(self.tab_two_edit_selected_item)
        spacerItem30 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem30)
        self.add_item_vert_line_31 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_31.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_31.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_31.setObjectName(_fromUtf8("add_item_vert_line_31"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_31)
        spacerItem31 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem31)
        self.tab_two_add_item_to_checkout = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_add_item_to_checkout.setMinimumSize(QtCore.QSize(0, 45))
        self.tab_two_add_item_to_checkout.setObjectName(_fromUtf8("tab_two_add_item_to_checkout"))
        self.horizontalLayout_5.addWidget(self.tab_two_add_item_to_checkout)
        spacerItem32 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem32)
        self.add_item_vert_line_29 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_29.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_29.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_29.setObjectName(_fromUtf8("add_item_vert_line_29"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_29)
        spacerItem33 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem33)
        self.tab_two_num_inventory_label = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_two_num_inventory_label.sizePolicy().hasHeightForWidth())
        self.tab_two_num_inventory_label.setSizePolicy(sizePolicy)
        self.tab_two_num_inventory_label.setMinimumSize(QtCore.QSize(170, 0))
        self.tab_two_num_inventory_label.setObjectName(_fromUtf8("tab_two_num_inventory_label"))
        self.horizontalLayout_5.addWidget(self.tab_two_num_inventory_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_5)
        self.horizontalLayout_9 = QtGui.QHBoxLayout()
        self.horizontalLayout_9.setSpacing(-1)
        self.horizontalLayout_9.setObjectName(_fromUtf8("horizontalLayout_9"))
        self.tab_one_search_item_lbl_3 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_search_item_lbl_3.setFont(font)
        self.tab_one_search_item_lbl_3.setScaledContents(False)
        self.tab_one_search_item_lbl_3.setObjectName(_fromUtf8("tab_one_search_item_lbl_3"))
        self.horizontalLayout_9.addWidget(self.tab_one_search_item_lbl_3)
        spacerItem34 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem34)
        self.add_item_vert_line_5 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_5.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_5.setObjectName(_fromUtf8("add_item_vert_line_5"))
        self.horizontalLayout_9.addWidget(self.add_item_vert_line_5)
        spacerItem35 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem35)
        self.filter_by_date_added_checkbox = QtGui.QCheckBox(self.layoutWidget1)
        self.filter_by_date_added_checkbox.setObjectName(_fromUtf8("filter_by_date_added_checkbox"))
        self.horizontalLayout_9.addWidget(self.filter_by_date_added_checkbox)
        spacerItem36 = QtGui.QSpacerItem(20, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem36)
        self.verticalLayout_6 = QtGui.QVBoxLayout()
        self.verticalLayout_6.setSpacing(0)
        self.verticalLayout_6.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_6.setObjectName(_fromUtf8("verticalLayout_6"))
        self.tab_two_date_start = QtGui.QDateEdit(self.layoutWidget1)
        self.tab_two_date_start.setCalendarPopup(True)
        self.tab_two_date_start.setObjectName(_fromUtf8("tab_two_date_start"))
        self.verticalLayout_6.addWidget(self.tab_two_date_start)
        self.label_4 = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_4.sizePolicy().hasHeightForWidth())
        self.label_4.setSizePolicy(sizePolicy)
        self.label_4.setMinimumSize(QtCore.QSize(0, 20))
        self.label_4.setAlignment(QtCore.Qt.AlignCenter)
        self.label_4.setObjectName(_fromUtf8("label_4"))
        self.verticalLayout_6.addWidget(self.label_4)
        self.horizontalLayout_9.addLayout(self.verticalLayout_6)
        self.verticalLayout_5 = QtGui.QVBoxLayout()
        self.verticalLayout_5.setSpacing(0)
        self.verticalLayout_5.setSizeConstraint(QtGui.QLayout.SetFixedSize)
        self.verticalLayout_5.setObjectName(_fromUtf8("verticalLayout_5"))
        self.tab_two_date_end = QtGui.QDateEdit(self.layoutWidget1)
        self.tab_two_date_end.setCalendarPopup(True)
        self.tab_two_date_end.setObjectName(_fromUtf8("tab_two_date_end"))
        self.verticalLayout_5.addWidget(self.tab_two_date_end)
        self.label_3 = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.label_3.sizePolicy().hasHeightForWidth())
        self.label_3.setSizePolicy(sizePolicy)
        self.label_3.setMinimumSize(QtCore.QSize(0, 20))
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName(_fromUtf8("label_3"))
        self.verticalLayout_5.addWidget(self.label_3)
        self.horizontalLayout_9.addLayout(self.verticalLayout_5)
        spacerItem37 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem37)
        self.add_item_vert_line_40 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_40.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_40.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_40.setObjectName(_fromUtf8("add_item_vert_line_40"))
        self.horizontalLayout_9.addWidget(self.add_item_vert_line_40)
        spacerItem38 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem38)
        self.label = QtGui.QLabel(self.layoutWidget1)
        self.label.setObjectName(_fromUtf8("label"))
        self.horizontalLayout_9.addWidget(self.label)
        self.tab_two_num_displayed_spin_box = QtGui.QSpinBox(self.layoutWidget1)
        self.tab_two_num_displayed_spin_box.setCorrectionMode(QtGui.QAbstractSpinBox.CorrectToNearestValue)
        self.tab_two_num_displayed_spin_box.setMinimum(10)
        self.tab_two_num_displayed_spin_box.setMaximum(99)
        self.tab_two_num_displayed_spin_box.setSingleStep(10)
        self.tab_two_num_displayed_spin_box.setProperty("value", 50)
        self.tab_two_num_displayed_spin_box.setObjectName(_fromUtf8("tab_two_num_displayed_spin_box"))
        self.horizontalLayout_9.addWidget(self.tab_two_num_displayed_spin_box)
        self.label_2 = QtGui.QLabel(self.layoutWidget1)
        self.label_2.setObjectName(_fromUtf8("label_2"))
        self.horizontalLayout_9.addWidget(self.label_2)
        spacerItem39 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem39)
        self.add_item_vert_line_41 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_41.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_41.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_41.setObjectName(_fromUtf8("add_item_vert_line_41"))
        self.horizontalLayout_9.addWidget(self.add_item_vert_line_41)
        spacerItem40 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_9.addItem(spacerItem40)
        self.tab_two_items_found_label = QtGui.QLabel(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_two_items_found_label.sizePolicy().hasHeightForWidth())
        self.tab_two_items_found_label.setSizePolicy(sizePolicy)
        self.tab_two_items_found_label.setMinimumSize(QtCore.QSize(170, 0))
        self.tab_two_items_found_label.setObjectName(_fromUtf8("tab_two_items_found_label"))
        self.horizontalLayout_9.addWidget(self.tab_two_items_found_label)
        self.verticalLayout_4.addLayout(self.horizontalLayout_9)
        self.verticalLayout_7.addLayout(self.verticalLayout_4)
        self.tab_two_results_table = QtGui.QTableWidget(self.layoutWidget1)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_two_results_table.sizePolicy().hasHeightForWidth())
        self.tab_two_results_table.setSizePolicy(sizePolicy)
        self.tab_two_results_table.setMinimumSize(QtCore.QSize(1850, 825))
        self.tab_two_results_table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tab_two_results_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tab_two_results_table.setObjectName(_fromUtf8("tab_two_results_table"))
        self.tab_two_results_table.setColumnCount(21)
        self.tab_two_results_table.setRowCount(97)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(21, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(22, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(23, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(24, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(25, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(26, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(27, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(28, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(29, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(30, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(31, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(32, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(33, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(34, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(35, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(36, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(37, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(38, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(39, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(40, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(41, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(42, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(43, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(44, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(45, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(46, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(47, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(48, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(49, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(50, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(51, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(52, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(53, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(54, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(55, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(56, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(57, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(58, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(59, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(60, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(61, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(62, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(63, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(64, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(65, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(66, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(67, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(68, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(69, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(70, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(71, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(72, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(73, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(74, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(75, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(76, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(77, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(78, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(79, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(80, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(81, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(82, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(83, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(84, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(85, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(86, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(87, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(88, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(89, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(90, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(91, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(92, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(93, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(94, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(95, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setVerticalHeaderItem(96, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setHorizontalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table.setItem(0, 3, item)
        self.tab_two_results_table.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_two_results_table.horizontalHeader().setDefaultSectionSize(100)
        self.tab_two_results_table.horizontalHeader().setSortIndicatorShown(False)
        self.tab_two_results_table.horizontalHeader().setStretchLastSection(True)
        self.verticalLayout_7.addWidget(self.tab_two_results_table)
        self.main_menu_tabs.addTab(self.search_inventory_tab, _fromUtf8(""))
        self.check_out_tab = QtGui.QWidget()
        self.check_out_tab.setObjectName(_fromUtf8("check_out_tab"))
        self.verticalLayout_9 = QtGui.QVBoxLayout(self.check_out_tab)
        self.verticalLayout_9.setObjectName(_fromUtf8("verticalLayout_9"))
        self.horizontalLayout_10 = QtGui.QHBoxLayout()
        self.horizontalLayout_10.setObjectName(_fromUtf8("horizontalLayout_10"))
        self.tab_one_search_item_lbl_4 = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_one_search_item_lbl_4.setFont(font)
        self.tab_one_search_item_lbl_4.setScaledContents(False)
        self.tab_one_search_item_lbl_4.setObjectName(_fromUtf8("tab_one_search_item_lbl_4"))
        self.horizontalLayout_10.addWidget(self.tab_one_search_item_lbl_4)
        spacerItem41 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem41)
        self.add_item_vert_line_10 = QtGui.QFrame(self.check_out_tab)
        self.add_item_vert_line_10.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_10.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_10.setObjectName(_fromUtf8("add_item_vert_line_10"))
        self.horizontalLayout_10.addWidget(self.add_item_vert_line_10)
        spacerItem42 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem42)
        self.tab_three_scan_barcode_qline = QtGui.QLineEdit(self.check_out_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_three_scan_barcode_qline.sizePolicy().hasHeightForWidth())
        self.tab_three_scan_barcode_qline.setSizePolicy(sizePolicy)
        self.tab_three_scan_barcode_qline.setMinimumSize(QtCore.QSize(250, 35))
        self.tab_three_scan_barcode_qline.setText(_fromUtf8(""))
        self.tab_three_scan_barcode_qline.setObjectName(_fromUtf8("tab_three_scan_barcode_qline"))
        self.horizontalLayout_10.addWidget(self.tab_three_scan_barcode_qline)
        spacerItem43 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem43)
        spacerItem44 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem44)
        self.tab_three_inventory_count_label = QtGui.QLabel(self.check_out_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_three_inventory_count_label.sizePolicy().hasHeightForWidth())
        self.tab_three_inventory_count_label.setSizePolicy(sizePolicy)
        self.tab_three_inventory_count_label.setMinimumSize(QtCore.QSize(170, 0))
        self.tab_three_inventory_count_label.setObjectName(_fromUtf8("tab_three_inventory_count_label"))
        self.horizontalLayout_10.addWidget(self.tab_three_inventory_count_label)
        self.tab_three_CREAM_button = QtGui.QPushButton(self.check_out_tab)
        self.tab_three_CREAM_button.setMinimumSize(QtCore.QSize(150, 50))
        self.tab_three_CREAM_button.setObjectName(_fromUtf8("tab_three_CREAM_button"))
        self.horizontalLayout_10.addWidget(self.tab_three_CREAM_button)
        spacerItem45 = QtGui.QSpacerItem(55, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_10.addItem(spacerItem45)
        self.tab_three_card_button = QtGui.QPushButton(self.check_out_tab)
        self.tab_three_card_button.setMinimumSize(QtCore.QSize(150, 50))
        self.tab_three_card_button.setObjectName(_fromUtf8("tab_three_card_button"))
        self.horizontalLayout_10.addWidget(self.tab_three_card_button)
        self.verticalLayout_9.addLayout(self.horizontalLayout_10)
        self.horizontalLayout_17 = QtGui.QHBoxLayout()
        self.horizontalLayout_17.setObjectName(_fromUtf8("horizontalLayout_17"))
        self.tab_three_checkout_table = QtGui.QTableWidget(self.check_out_tab)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Minimum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_three_checkout_table.sizePolicy().hasHeightForWidth())
        self.tab_three_checkout_table.setSizePolicy(sizePolicy)
        self.tab_three_checkout_table.setMinimumSize(QtCore.QSize(1450, 900))
        self.tab_three_checkout_table.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tab_three_checkout_table.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tab_three_checkout_table.setObjectName(_fromUtf8("tab_three_checkout_table"))
        self.tab_three_checkout_table.setColumnCount(12)
        self.tab_three_checkout_table.setRowCount(98)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(21, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(22, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(23, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(24, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(25, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(26, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(27, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(28, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(29, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(30, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(31, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(32, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(33, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(34, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(35, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(36, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(37, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(38, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(39, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(40, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(41, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(42, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(43, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(44, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(45, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(46, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(47, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(48, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(49, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(50, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(51, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(52, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(53, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(54, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(55, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(56, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(57, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(58, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(59, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(60, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(61, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(62, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(63, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(64, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(65, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(66, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(67, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(68, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(69, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(70, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(71, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(72, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(73, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(74, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(75, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(76, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(77, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(78, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(79, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(80, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(81, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(82, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(83, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(84, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(85, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(86, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(87, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(88, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(89, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(90, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(91, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(92, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(93, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(94, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(95, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(96, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setVerticalHeaderItem(97, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setItem(0, 2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_checkout_table.setItem(0, 3, item)
        self.tab_three_checkout_table.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_three_checkout_table.horizontalHeader().setDefaultSectionSize(100)
        self.tab_three_checkout_table.horizontalHeader().setSortIndicatorShown(False)
        self.tab_three_checkout_table.horizontalHeader().setStretchLastSection(False)
        self.horizontalLayout_17.addWidget(self.tab_three_checkout_table)
        spacerItem46 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_17.addItem(spacerItem46)
        self.verticalLayout_8 = QtGui.QVBoxLayout()
        self.verticalLayout_8.setObjectName(_fromUtf8("verticalLayout_8"))
        self.tab_three_final_checkout_table = QtGui.QTableWidget(self.check_out_tab)
        self.tab_three_final_checkout_table.setMinimumSize(QtCore.QSize(360, 700))
        self.tab_three_final_checkout_table.setMaximumSize(QtCore.QSize(360, 700))
        self.tab_three_final_checkout_table.setGridStyle(QtCore.Qt.SolidLine)
        self.tab_three_final_checkout_table.setObjectName(_fromUtf8("tab_three_final_checkout_table"))
        self.tab_three_final_checkout_table.setColumnCount(2)
        self.tab_three_final_checkout_table.setRowCount(50)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(21, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(22, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(23, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(24, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(25, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(26, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(27, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(28, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(29, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(30, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(31, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(32, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(33, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(34, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(35, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(36, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(37, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(38, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(39, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(40, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(41, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(42, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(43, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(44, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(45, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(46, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(47, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(48, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setVerticalHeaderItem(49, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_three_final_checkout_table.setHorizontalHeaderItem(1, item)
        self.tab_three_final_checkout_table.horizontalHeader().setVisible(False)
        self.tab_three_final_checkout_table.horizontalHeader().setStretchLastSection(True)
        self.tab_three_final_checkout_table.verticalHeader().setVisible(False)
        self.tab_three_final_checkout_table.verticalHeader().setStretchLastSection(False)
        self.verticalLayout_8.addWidget(self.tab_three_final_checkout_table)
        self.horizontalLayout_13 = QtGui.QHBoxLayout()
        self.horizontalLayout_13.setObjectName(_fromUtf8("horizontalLayout_13"))
        self.tab_three_subtotal_label = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_subtotal_label.setFont(font)
        self.tab_three_subtotal_label.setObjectName(_fromUtf8("tab_three_subtotal_label"))
        self.horizontalLayout_13.addWidget(self.tab_three_subtotal_label)
        spacerItem47 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_13.addItem(spacerItem47)
        self.tab_three_subtotal_qline = QtGui.QLineEdit(self.check_out_tab)
        self.tab_three_subtotal_qline.setMinimumSize(QtCore.QSize(100, 0))
        self.tab_three_subtotal_qline.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tab_three_subtotal_qline.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tab_three_subtotal_qline.setReadOnly(True)
        self.tab_three_subtotal_qline.setObjectName(_fromUtf8("tab_three_subtotal_qline"))
        self.horizontalLayout_13.addWidget(self.tab_three_subtotal_qline)
        self.verticalLayout_8.addLayout(self.horizontalLayout_13)
        self.horizontalLayout_12 = QtGui.QHBoxLayout()
        self.horizontalLayout_12.setObjectName(_fromUtf8("horizontalLayout_12"))
        self.tab_three_discount_label = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_discount_label.setFont(font)
        self.tab_three_discount_label.setObjectName(_fromUtf8("tab_three_discount_label"))
        self.horizontalLayout_12.addWidget(self.tab_three_discount_label)
        spacerItem48 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_12.addItem(spacerItem48)
        self.horizontalLayout_11 = QtGui.QHBoxLayout()
        self.horizontalLayout_11.setObjectName(_fromUtf8("horizontalLayout_11"))
        self.tab_three_percent_discount_qline = QtGui.QLineEdit(self.check_out_tab)
        self.tab_three_percent_discount_qline.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tab_three_percent_discount_qline.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tab_three_percent_discount_qline.setObjectName(_fromUtf8("tab_three_percent_discount_qline"))
        self.horizontalLayout_11.addWidget(self.tab_three_percent_discount_qline)
        self.tab_three_discount_qline = QtGui.QLineEdit(self.check_out_tab)
        self.tab_three_discount_qline.setMinimumSize(QtCore.QSize(100, 0))
        self.tab_three_discount_qline.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tab_three_discount_qline.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tab_three_discount_qline.setObjectName(_fromUtf8("tab_three_discount_qline"))
        self.horizontalLayout_11.addWidget(self.tab_three_discount_qline)
        self.horizontalLayout_12.addLayout(self.horizontalLayout_11)
        self.verticalLayout_8.addLayout(self.horizontalLayout_12)
        self.horizontalLayout_14 = QtGui.QHBoxLayout()
        self.horizontalLayout_14.setObjectName(_fromUtf8("horizontalLayout_14"))
        self.tab_three_tax_label = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_tax_label.setFont(font)
        self.tab_three_tax_label.setObjectName(_fromUtf8("tab_three_tax_label"))
        self.horizontalLayout_14.addWidget(self.tab_three_tax_label)
        spacerItem49 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_14.addItem(spacerItem49)
        self.tab_three_tax_amount_label = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_tax_amount_label.setFont(font)
        self.tab_three_tax_amount_label.setObjectName(_fromUtf8("tab_three_tax_amount_label"))
        self.horizontalLayout_14.addWidget(self.tab_three_tax_amount_label)
        self.verticalLayout_8.addLayout(self.horizontalLayout_14)
        self.horizontalLayout_19 = QtGui.QHBoxLayout()
        self.horizontalLayout_19.setObjectName(_fromUtf8("horizontalLayout_19"))
        self.tab_three_shipping_label = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_shipping_label.setFont(font)
        self.tab_three_shipping_label.setObjectName(_fromUtf8("tab_three_shipping_label"))
        self.horizontalLayout_19.addWidget(self.tab_three_shipping_label)
        spacerItem50 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_19.addItem(spacerItem50)
        self.tab_three_shipping_qline = QtGui.QLineEdit(self.check_out_tab)
        self.tab_three_shipping_qline.setMinimumSize(QtCore.QSize(100, 0))
        self.tab_three_shipping_qline.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tab_three_shipping_qline.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tab_three_shipping_qline.setObjectName(_fromUtf8("tab_three_shipping_qline"))
        self.horizontalLayout_19.addWidget(self.tab_three_shipping_qline)
        self.verticalLayout_8.addLayout(self.horizontalLayout_19)
        spacerItem51 = QtGui.QSpacerItem(20, 40, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem51)
        self.horizontalLayout_16 = QtGui.QHBoxLayout()
        self.horizontalLayout_16.setObjectName(_fromUtf8("horizontalLayout_16"))
        self.tab_three_total_label = QtGui.QLabel(self.check_out_tab)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_total_label.setFont(font)
        self.tab_three_total_label.setObjectName(_fromUtf8("tab_three_total_label"))
        self.horizontalLayout_16.addWidget(self.tab_three_total_label)
        spacerItem52 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_16.addItem(spacerItem52)
        self.tab_three_total_qline = QtGui.QLineEdit(self.check_out_tab)
        self.tab_three_total_qline.setMinimumSize(QtCore.QSize(100, 0))
        self.tab_three_total_qline.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tab_three_total_qline.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tab_three_total_qline.setObjectName(_fromUtf8("tab_three_total_qline"))
        self.horizontalLayout_16.addWidget(self.tab_three_total_qline)
        self.verticalLayout_8.addLayout(self.horizontalLayout_16)
        spacerItem53 = QtGui.QSpacerItem(10, 20, QtGui.QSizePolicy.Minimum, QtGui.QSizePolicy.Expanding)
        self.verticalLayout_8.addItem(spacerItem53)
        self.horizontalLayout_17.addLayout(self.verticalLayout_8)
        self.verticalLayout_9.addLayout(self.horizontalLayout_17)
        self.main_menu_tabs.addTab(self.check_out_tab, _fromUtf8(""))
        self.history_tab = QtGui.QWidget()
        self.history_tab.setObjectName(_fromUtf8("history_tab"))
        self.tab_one_results_table_4 = QtGui.QTableWidget(self.history_tab)
        self.tab_one_results_table_4.setGeometry(QtCore.QRect(30, 450, 1850, 380))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.MinimumExpanding)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_one_results_table_4.sizePolicy().hasHeightForWidth())
        self.tab_one_results_table_4.setSizePolicy(sizePolicy)
        self.tab_one_results_table_4.setMinimumSize(QtCore.QSize(1850, 380))
        self.tab_one_results_table_4.setSelectionMode(QtGui.QAbstractItemView.ExtendedSelection)
        self.tab_one_results_table_4.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.tab_one_results_table_4.setObjectName(_fromUtf8("tab_one_results_table_4"))
        self.tab_one_results_table_4.setColumnCount(21)
        self.tab_one_results_table_4.setRowCount(49)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(21, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(22, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(23, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(24, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(25, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(26, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(27, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(28, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(29, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(30, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(31, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(32, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(33, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(34, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(35, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(36, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(37, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(38, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(39, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(40, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(41, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(42, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(43, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(44, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(45, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(46, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(47, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setVerticalHeaderItem(48, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(19, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setHorizontalHeaderItem(20, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_one_results_table_4.setItem(0, 2, item)
        self.tab_one_results_table_4.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_one_results_table_4.horizontalHeader().setDefaultSectionSize(100)
        self.tab_one_results_table_4.horizontalHeader().setSortIndicatorShown(True)
        self.tab_one_results_table_4.horizontalHeader().setStretchLastSection(False)
        self.layoutWidget_2 = QtGui.QWidget(self.history_tab)
        self.layoutWidget_2.setGeometry(QtCore.QRect(1020, 90, 200, 23))
        self.layoutWidget_2.setObjectName(_fromUtf8("layoutWidget_2"))
        self.horizontalLayout_18 = QtGui.QHBoxLayout(self.layoutWidget_2)
        self.horizontalLayout_18.setMargin(0)
        self.horizontalLayout_18.setObjectName(_fromUtf8("horizontalLayout_18"))
        self.tab_three_total_label_2 = QtGui.QLabel(self.layoutWidget_2)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(16)
        self.tab_three_total_label_2.setFont(font)
        self.tab_three_total_label_2.setObjectName(_fromUtf8("tab_three_total_label_2"))
        self.horizontalLayout_18.addWidget(self.tab_three_total_label_2)
        spacerItem54 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_18.addItem(spacerItem54)
        self.tab_three_total_qline_2 = QtGui.QLineEdit(self.layoutWidget_2)
        self.tab_three_total_qline_2.setMinimumSize(QtCore.QSize(100, 0))
        self.tab_three_total_qline_2.setMaximumSize(QtCore.QSize(100, 16777215))
        self.tab_three_total_qline_2.setObjectName(_fromUtf8("tab_three_total_qline_2"))
        self.horizontalLayout_18.addWidget(self.tab_three_total_qline_2)
        self.main_menu_tabs.addTab(self.history_tab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.main_menu_tabs)

        self.retranslateUi(Form)
        self.main_menu_tabs.setCurrentIndex(2)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Plaid Room Records", None))
        self.tab_one_search_item_lbl.setText(_translate("Form", "Search Item", None))
        self.tab_one_vinyl_radio_button.setText(_translate("Form", "Vinyl", None))
        self.tab_one_cd_radio_button.setText(_translate("Form", "CD", None))
        self.tab_one_any_radio_button.setText(_translate("Form", "Any", None))
        self.tab_one_search_upc_button.setText(_translate("Form", "Search UPC/SKU/EAN", None))
        self.tab_one_search_artist_title_button.setText(_translate("Form", "Search Artist/Title", None))
        self.tab_one_clear_all_button.setText(_translate("Form", "Clear All", None))
        self.tab_one_results_table.setSortingEnabled(False)
        item = self.tab_one_results_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_one_results_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_one_results_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_one_results_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_one_results_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_one_results_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_one_results_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_one_results_table.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_one_results_table.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_one_results_table.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_one_results_table.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_one_results_table.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_one_results_table.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_one_results_table.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_one_results_table.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_one_results_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.tab_one_results_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Artist", None))
        item = self.tab_one_results_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Title", None))
        item = self.tab_one_results_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Format", None))
        item = self.tab_one_results_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.tab_one_results_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Price Paid", None))
        item = self.tab_one_results_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "New/Used", None))
        item = self.tab_one_results_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Distributor", None))
        item = self.tab_one_results_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Label", None))
        item = self.tab_one_results_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Genre", None))
        item = self.tab_one_results_table.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Year", None))
        item = self.tab_one_results_table.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Date Added", None))
        item = self.tab_one_results_table.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Discogs Release Number", None))
        __sortingEnabled = self.tab_one_results_table.isSortingEnabled()
        self.tab_one_results_table.setSortingEnabled(False)
        self.tab_one_results_table.setSortingEnabled(__sortingEnabled)
        self.tab_one_add_item_lbl.setText(_translate("Form", "Add Item", None))
        self.tab_one_add_selected_to_inventory.setText(_translate("Form", "Add Selected Item To Inventory", None))
        self.tab_one_print_sticker_check_box.setText(_translate("Form", "Print Sticker", None))
        self.tab_one_generate_sku_button.setText(_translate("Form", "Generate New SKU For Selected Item", None))
        self.tab_one_recent_additions_lbl.setText(_translate("Form", "Recent Additions", None))
        self.tab_one_remove_selected_item_from_inventory.setText(_translate("Form", "Remove Selected Item From Inventory", None))
        self.tab_one_edit_selected_item.setText(_translate("Form", "Save Changes To Selected Item", None))
        self.tab_one_num_inventory_label.setText(_translate("Form", "XXXX Items In Inventory", None))
        self.tab_one_recently_added_table.setSortingEnabled(False)
        item = self.tab_one_recently_added_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(15)
        item.setText(_translate("Form", "16", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(16)
        item.setText(_translate("Form", "17", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(17)
        item.setText(_translate("Form", "18", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(18)
        item.setText(_translate("Form", "19", None))
        item = self.tab_one_recently_added_table.verticalHeaderItem(19)
        item.setText(_translate("Form", "20", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Artist", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Title", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Format", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Price Paid", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "New/Used", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Distributor", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Label", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Genre", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Year", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Date Added", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Discogs Release Number", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(13)
        item.setText(_translate("Form", "Real Name", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(14)
        item.setText(_translate("Form", "Profile", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(15)
        item.setText(_translate("Form", "Variations", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(16)
        item.setText(_translate("Form", "Aliases", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(17)
        item.setText(_translate("Form", "Track List", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(18)
        item.setText(_translate("Form", "Notes", None))
        item = self.tab_one_recently_added_table.horizontalHeaderItem(19)
        item.setText(_translate("Form", "Primary Key", None))
        __sortingEnabled = self.tab_one_recently_added_table.isSortingEnabled()
        self.tab_one_recently_added_table.setSortingEnabled(False)
        self.tab_one_recently_added_table.setSortingEnabled(__sortingEnabled)
        self.tab_one_console_lbl.setText(_translate("Form", "Console", None))
        self.tab_one_text_browser.setHtml(_translate("Form", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'.Lucida Grande UI\'; font-size:13pt; font-weight:400; font-style:normal;\">\n"
"<p style=\"-qt-paragraph-type:empty; margin-top:12px; margin-bottom:12px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\"><br /></p></body></html>", None))
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.add_inventory_tab), _translate("Form", "Add Inventory", None))
        self.tab_one_search_item_lbl_2.setText(_translate("Form", "Search Item", None))
        self.tab_two_search_artist_title_button.setText(_translate("Form", "Search", None))
        self.tab_two_reset_button.setText(_translate("Form", "Reset", None))
        self.tab_two_remove_selected_item_from_inventory.setText(_translate("Form", "Remove Selected Item From Inventory", None))
        self.tab_two_edit_selected_item.setText(_translate("Form", "Save Changes To Selected Item", None))
        self.tab_two_add_item_to_checkout.setText(_translate("Form", "Add Item to Checkout", None))
        self.tab_two_num_inventory_label.setText(_translate("Form", "XXXX Items In Inventory", None))
        self.tab_one_search_item_lbl_3.setText(_translate("Form", "Filter", None))
        self.filter_by_date_added_checkbox.setText(_translate("Form", "Filter by Date Added", None))
        self.label_4.setText(_translate("Form", "Start Date", None))
        self.label_3.setText(_translate("Form", "End Date", None))
        self.label.setText(_translate("Form", "Show", None))
        self.label_2.setText(_translate("Form", "Items", None))
        self.tab_two_items_found_label.setText(_translate("Form", "XXXX Items Found For Search Terms", None))
        self.tab_two_results_table.setSortingEnabled(False)
        item = self.tab_two_results_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_two_results_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_two_results_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_two_results_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_two_results_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_two_results_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_two_results_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_two_results_table.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_two_results_table.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_two_results_table.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_two_results_table.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_two_results_table.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_two_results_table.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_two_results_table.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_two_results_table.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_two_results_table.verticalHeaderItem(15)
        item.setText(_translate("Form", "16", None))
        item = self.tab_two_results_table.verticalHeaderItem(16)
        item.setText(_translate("Form", "17", None))
        item = self.tab_two_results_table.verticalHeaderItem(17)
        item.setText(_translate("Form", "18", None))
        item = self.tab_two_results_table.verticalHeaderItem(18)
        item.setText(_translate("Form", "19", None))
        item = self.tab_two_results_table.verticalHeaderItem(19)
        item.setText(_translate("Form", "20", None))
        item = self.tab_two_results_table.verticalHeaderItem(20)
        item.setText(_translate("Form", "21", None))
        item = self.tab_two_results_table.verticalHeaderItem(21)
        item.setText(_translate("Form", "22", None))
        item = self.tab_two_results_table.verticalHeaderItem(22)
        item.setText(_translate("Form", "23", None))
        item = self.tab_two_results_table.verticalHeaderItem(23)
        item.setText(_translate("Form", "24", None))
        item = self.tab_two_results_table.verticalHeaderItem(24)
        item.setText(_translate("Form", "25", None))
        item = self.tab_two_results_table.verticalHeaderItem(25)
        item.setText(_translate("Form", "26", None))
        item = self.tab_two_results_table.verticalHeaderItem(26)
        item.setText(_translate("Form", "27", None))
        item = self.tab_two_results_table.verticalHeaderItem(27)
        item.setText(_translate("Form", "28", None))
        item = self.tab_two_results_table.verticalHeaderItem(28)
        item.setText(_translate("Form", "29", None))
        item = self.tab_two_results_table.verticalHeaderItem(29)
        item.setText(_translate("Form", "30", None))
        item = self.tab_two_results_table.verticalHeaderItem(30)
        item.setText(_translate("Form", "31", None))
        item = self.tab_two_results_table.verticalHeaderItem(31)
        item.setText(_translate("Form", "32", None))
        item = self.tab_two_results_table.verticalHeaderItem(32)
        item.setText(_translate("Form", "33", None))
        item = self.tab_two_results_table.verticalHeaderItem(33)
        item.setText(_translate("Form", "34", None))
        item = self.tab_two_results_table.verticalHeaderItem(34)
        item.setText(_translate("Form", "35", None))
        item = self.tab_two_results_table.verticalHeaderItem(35)
        item.setText(_translate("Form", "36", None))
        item = self.tab_two_results_table.verticalHeaderItem(36)
        item.setText(_translate("Form", "37", None))
        item = self.tab_two_results_table.verticalHeaderItem(37)
        item.setText(_translate("Form", "38", None))
        item = self.tab_two_results_table.verticalHeaderItem(38)
        item.setText(_translate("Form", "39", None))
        item = self.tab_two_results_table.verticalHeaderItem(39)
        item.setText(_translate("Form", "40", None))
        item = self.tab_two_results_table.verticalHeaderItem(40)
        item.setText(_translate("Form", "41", None))
        item = self.tab_two_results_table.verticalHeaderItem(41)
        item.setText(_translate("Form", "42", None))
        item = self.tab_two_results_table.verticalHeaderItem(42)
        item.setText(_translate("Form", "43", None))
        item = self.tab_two_results_table.verticalHeaderItem(43)
        item.setText(_translate("Form", "44", None))
        item = self.tab_two_results_table.verticalHeaderItem(44)
        item.setText(_translate("Form", "45", None))
        item = self.tab_two_results_table.verticalHeaderItem(45)
        item.setText(_translate("Form", "46", None))
        item = self.tab_two_results_table.verticalHeaderItem(46)
        item.setText(_translate("Form", "47", None))
        item = self.tab_two_results_table.verticalHeaderItem(47)
        item.setText(_translate("Form", "48", None))
        item = self.tab_two_results_table.verticalHeaderItem(48)
        item.setText(_translate("Form", "49", None))
        item = self.tab_two_results_table.verticalHeaderItem(49)
        item.setText(_translate("Form", "50", None))
        item = self.tab_two_results_table.verticalHeaderItem(50)
        item.setText(_translate("Form", "51", None))
        item = self.tab_two_results_table.verticalHeaderItem(51)
        item.setText(_translate("Form", "52", None))
        item = self.tab_two_results_table.verticalHeaderItem(52)
        item.setText(_translate("Form", "53", None))
        item = self.tab_two_results_table.verticalHeaderItem(53)
        item.setText(_translate("Form", "55", None))
        item = self.tab_two_results_table.verticalHeaderItem(54)
        item.setText(_translate("Form", "56", None))
        item = self.tab_two_results_table.verticalHeaderItem(55)
        item.setText(_translate("Form", "57", None))
        item = self.tab_two_results_table.verticalHeaderItem(56)
        item.setText(_translate("Form", "58", None))
        item = self.tab_two_results_table.verticalHeaderItem(57)
        item.setText(_translate("Form", "59", None))
        item = self.tab_two_results_table.verticalHeaderItem(58)
        item.setText(_translate("Form", "60", None))
        item = self.tab_two_results_table.verticalHeaderItem(59)
        item.setText(_translate("Form", "61", None))
        item = self.tab_two_results_table.verticalHeaderItem(60)
        item.setText(_translate("Form", "62", None))
        item = self.tab_two_results_table.verticalHeaderItem(61)
        item.setText(_translate("Form", "63", None))
        item = self.tab_two_results_table.verticalHeaderItem(62)
        item.setText(_translate("Form", "64", None))
        item = self.tab_two_results_table.verticalHeaderItem(63)
        item.setText(_translate("Form", "65", None))
        item = self.tab_two_results_table.verticalHeaderItem(64)
        item.setText(_translate("Form", "66", None))
        item = self.tab_two_results_table.verticalHeaderItem(65)
        item.setText(_translate("Form", "67", None))
        item = self.tab_two_results_table.verticalHeaderItem(66)
        item.setText(_translate("Form", "68", None))
        item = self.tab_two_results_table.verticalHeaderItem(67)
        item.setText(_translate("Form", "69", None))
        item = self.tab_two_results_table.verticalHeaderItem(68)
        item.setText(_translate("Form", "70", None))
        item = self.tab_two_results_table.verticalHeaderItem(69)
        item.setText(_translate("Form", "71", None))
        item = self.tab_two_results_table.verticalHeaderItem(70)
        item.setText(_translate("Form", "72", None))
        item = self.tab_two_results_table.verticalHeaderItem(71)
        item.setText(_translate("Form", "73", None))
        item = self.tab_two_results_table.verticalHeaderItem(72)
        item.setText(_translate("Form", "74", None))
        item = self.tab_two_results_table.verticalHeaderItem(73)
        item.setText(_translate("Form", "75", None))
        item = self.tab_two_results_table.verticalHeaderItem(74)
        item.setText(_translate("Form", "76", None))
        item = self.tab_two_results_table.verticalHeaderItem(75)
        item.setText(_translate("Form", "77", None))
        item = self.tab_two_results_table.verticalHeaderItem(76)
        item.setText(_translate("Form", "78", None))
        item = self.tab_two_results_table.verticalHeaderItem(77)
        item.setText(_translate("Form", "79", None))
        item = self.tab_two_results_table.verticalHeaderItem(78)
        item.setText(_translate("Form", "80", None))
        item = self.tab_two_results_table.verticalHeaderItem(79)
        item.setText(_translate("Form", "81", None))
        item = self.tab_two_results_table.verticalHeaderItem(80)
        item.setText(_translate("Form", "82", None))
        item = self.tab_two_results_table.verticalHeaderItem(81)
        item.setText(_translate("Form", "83", None))
        item = self.tab_two_results_table.verticalHeaderItem(82)
        item.setText(_translate("Form", "84", None))
        item = self.tab_two_results_table.verticalHeaderItem(83)
        item.setText(_translate("Form", "85", None))
        item = self.tab_two_results_table.verticalHeaderItem(84)
        item.setText(_translate("Form", "86", None))
        item = self.tab_two_results_table.verticalHeaderItem(85)
        item.setText(_translate("Form", "87", None))
        item = self.tab_two_results_table.verticalHeaderItem(86)
        item.setText(_translate("Form", "88", None))
        item = self.tab_two_results_table.verticalHeaderItem(87)
        item.setText(_translate("Form", "90", None))
        item = self.tab_two_results_table.verticalHeaderItem(88)
        item.setText(_translate("Form", "91", None))
        item = self.tab_two_results_table.verticalHeaderItem(89)
        item.setText(_translate("Form", "92", None))
        item = self.tab_two_results_table.verticalHeaderItem(90)
        item.setText(_translate("Form", "93", None))
        item = self.tab_two_results_table.verticalHeaderItem(91)
        item.setText(_translate("Form", "94", None))
        item = self.tab_two_results_table.verticalHeaderItem(92)
        item.setText(_translate("Form", "95", None))
        item = self.tab_two_results_table.verticalHeaderItem(93)
        item.setText(_translate("Form", "96", None))
        item = self.tab_two_results_table.verticalHeaderItem(94)
        item.setText(_translate("Form", "97", None))
        item = self.tab_two_results_table.verticalHeaderItem(95)
        item.setText(_translate("Form", "98", None))
        item = self.tab_two_results_table.verticalHeaderItem(96)
        item.setText(_translate("Form", "99", None))
        item = self.tab_two_results_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "More...", None))
        item = self.tab_two_results_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.tab_two_results_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Artist", None))
        item = self.tab_two_results_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Title", None))
        item = self.tab_two_results_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Format", None))
        item = self.tab_two_results_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.tab_two_results_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Price Paid", None))
        item = self.tab_two_results_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "New/Used", None))
        item = self.tab_two_results_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Distributor", None))
        item = self.tab_two_results_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Label", None))
        item = self.tab_two_results_table.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Genre", None))
        item = self.tab_two_results_table.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Year", None))
        item = self.tab_two_results_table.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Date Added", None))
        item = self.tab_two_results_table.horizontalHeaderItem(13)
        item.setText(_translate("Form", "Discogs Release Number", None))
        item = self.tab_two_results_table.horizontalHeaderItem(14)
        item.setText(_translate("Form", "Real Name", None))
        item = self.tab_two_results_table.horizontalHeaderItem(15)
        item.setText(_translate("Form", "Profile", None))
        item = self.tab_two_results_table.horizontalHeaderItem(16)
        item.setText(_translate("Form", "Variations", None))
        item = self.tab_two_results_table.horizontalHeaderItem(17)
        item.setText(_translate("Form", "Aliases", None))
        item = self.tab_two_results_table.horizontalHeaderItem(18)
        item.setText(_translate("Form", "Track List", None))
        item = self.tab_two_results_table.horizontalHeaderItem(19)
        item.setText(_translate("Form", "Notes", None))
        item = self.tab_two_results_table.horizontalHeaderItem(20)
        item.setText(_translate("Form", "Key", None))
        __sortingEnabled = self.tab_two_results_table.isSortingEnabled()
        self.tab_two_results_table.setSortingEnabled(False)
        self.tab_two_results_table.setSortingEnabled(__sortingEnabled)
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.search_inventory_tab), _translate("Form", "Search/Edit/Remove Inventory", None))
        self.tab_one_search_item_lbl_4.setText(_translate("Form", "Scan Barcode", None))
        self.tab_three_inventory_count_label.setText(_translate("Form", "XXXX Items In Inventory", None))
        self.tab_three_CREAM_button.setText(_translate("Form", "C.R.E.A.M.", None))
        self.tab_three_card_button.setText(_translate("Form", "Credit", None))
        self.tab_three_checkout_table.setSortingEnabled(False)
        item = self.tab_three_checkout_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(15)
        item.setText(_translate("Form", "16", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(16)
        item.setText(_translate("Form", "17", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(17)
        item.setText(_translate("Form", "18", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(18)
        item.setText(_translate("Form", "19", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(19)
        item.setText(_translate("Form", "20", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(20)
        item.setText(_translate("Form", "21", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(21)
        item.setText(_translate("Form", "22", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(22)
        item.setText(_translate("Form", "23", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(23)
        item.setText(_translate("Form", "24", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(24)
        item.setText(_translate("Form", "25", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(25)
        item.setText(_translate("Form", "26", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(26)
        item.setText(_translate("Form", "27", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(27)
        item.setText(_translate("Form", "28", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(28)
        item.setText(_translate("Form", "29", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(29)
        item.setText(_translate("Form", "30", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(30)
        item.setText(_translate("Form", "31", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(31)
        item.setText(_translate("Form", "32", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(32)
        item.setText(_translate("Form", "33", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(33)
        item.setText(_translate("Form", "34", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(34)
        item.setText(_translate("Form", "35", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(35)
        item.setText(_translate("Form", "36", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(36)
        item.setText(_translate("Form", "37", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(37)
        item.setText(_translate("Form", "38", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(38)
        item.setText(_translate("Form", "39", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(39)
        item.setText(_translate("Form", "40", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(40)
        item.setText(_translate("Form", "41", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(41)
        item.setText(_translate("Form", "42", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(42)
        item.setText(_translate("Form", "43", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(43)
        item.setText(_translate("Form", "44", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(44)
        item.setText(_translate("Form", "45", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(45)
        item.setText(_translate("Form", "46", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(46)
        item.setText(_translate("Form", "47", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(47)
        item.setText(_translate("Form", "48", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(48)
        item.setText(_translate("Form", "49", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(49)
        item.setText(_translate("Form", "50", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(50)
        item.setText(_translate("Form", "51", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(51)
        item.setText(_translate("Form", "52", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(52)
        item.setText(_translate("Form", "53", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(53)
        item.setText(_translate("Form", "55", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(54)
        item.setText(_translate("Form", "56", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(55)
        item.setText(_translate("Form", "57", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(56)
        item.setText(_translate("Form", "58", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(57)
        item.setText(_translate("Form", "59", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(58)
        item.setText(_translate("Form", "60", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(59)
        item.setText(_translate("Form", "61", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(60)
        item.setText(_translate("Form", "62", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(61)
        item.setText(_translate("Form", "63", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(62)
        item.setText(_translate("Form", "64", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(63)
        item.setText(_translate("Form", "65", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(64)
        item.setText(_translate("Form", "66", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(65)
        item.setText(_translate("Form", "67", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(66)
        item.setText(_translate("Form", "68", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(67)
        item.setText(_translate("Form", "69", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(68)
        item.setText(_translate("Form", "70", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(69)
        item.setText(_translate("Form", "71", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(70)
        item.setText(_translate("Form", "72", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(71)
        item.setText(_translate("Form", "73", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(72)
        item.setText(_translate("Form", "74", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(73)
        item.setText(_translate("Form", "75", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(74)
        item.setText(_translate("Form", "76", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(75)
        item.setText(_translate("Form", "77", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(76)
        item.setText(_translate("Form", "78", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(77)
        item.setText(_translate("Form", "79", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(78)
        item.setText(_translate("Form", "80", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(79)
        item.setText(_translate("Form", "81", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(80)
        item.setText(_translate("Form", "82", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(81)
        item.setText(_translate("Form", "83", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(82)
        item.setText(_translate("Form", "84", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(83)
        item.setText(_translate("Form", "85", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(84)
        item.setText(_translate("Form", "86", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(85)
        item.setText(_translate("Form", "87", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(86)
        item.setText(_translate("Form", "88", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(87)
        item.setText(_translate("Form", "89", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(88)
        item.setText(_translate("Form", "90", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(89)
        item.setText(_translate("Form", "91", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(90)
        item.setText(_translate("Form", "92", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(91)
        item.setText(_translate("Form", "93", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(92)
        item.setText(_translate("Form", "94", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(93)
        item.setText(_translate("Form", "95", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(94)
        item.setText(_translate("Form", "96", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(95)
        item.setText(_translate("Form", "97", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(96)
        item.setText(_translate("Form", "98", None))
        item = self.tab_three_checkout_table.verticalHeaderItem(97)
        item.setText(_translate("Form", "99", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Remove", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Artist", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Title", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Discount", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "+5%", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "New/Used", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Date Added", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Sold Notes", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Key", None))
        item = self.tab_three_checkout_table.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Price Paid", None))
        __sortingEnabled = self.tab_three_checkout_table.isSortingEnabled()
        self.tab_three_checkout_table.setSortingEnabled(False)
        self.tab_three_checkout_table.setSortingEnabled(__sortingEnabled)
        item = self.tab_three_final_checkout_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(15)
        item.setText(_translate("Form", "16", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(16)
        item.setText(_translate("Form", "17", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(17)
        item.setText(_translate("Form", "18", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(18)
        item.setText(_translate("Form", "19", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(19)
        item.setText(_translate("Form", "20", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(20)
        item.setText(_translate("Form", "21", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(21)
        item.setText(_translate("Form", "22", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(22)
        item.setText(_translate("Form", "23", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(23)
        item.setText(_translate("Form", "24", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(24)
        item.setText(_translate("Form", "25", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(25)
        item.setText(_translate("Form", "26", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(26)
        item.setText(_translate("Form", "27", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(27)
        item.setText(_translate("Form", "28", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(28)
        item.setText(_translate("Form", "29", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(29)
        item.setText(_translate("Form", "30", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(30)
        item.setText(_translate("Form", "31", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(31)
        item.setText(_translate("Form", "32", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(32)
        item.setText(_translate("Form", "33", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(33)
        item.setText(_translate("Form", "34", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(34)
        item.setText(_translate("Form", "35", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(35)
        item.setText(_translate("Form", "36", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(36)
        item.setText(_translate("Form", "37", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(37)
        item.setText(_translate("Form", "38", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(38)
        item.setText(_translate("Form", "39", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(39)
        item.setText(_translate("Form", "40", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(40)
        item.setText(_translate("Form", "41", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(41)
        item.setText(_translate("Form", "42", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(42)
        item.setText(_translate("Form", "43", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(43)
        item.setText(_translate("Form", "44", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(44)
        item.setText(_translate("Form", "45", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(45)
        item.setText(_translate("Form", "46", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(46)
        item.setText(_translate("Form", "47", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(47)
        item.setText(_translate("Form", "48", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(48)
        item.setText(_translate("Form", "49", None))
        item = self.tab_three_final_checkout_table.verticalHeaderItem(49)
        item.setText(_translate("Form", "50", None))
        item = self.tab_three_final_checkout_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "Item", None))
        item = self.tab_three_final_checkout_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Price", None))
        self.tab_three_subtotal_label.setText(_translate("Form", "Subtotal", None))
        self.tab_three_discount_label.setText(_translate("Form", "Discount", None))
        self.tab_three_tax_label.setText(_translate("Form", "Sales tax at 7%", None))
        self.tab_three_tax_amount_label.setText(_translate("Form", "$X.XX", None))
        self.tab_three_shipping_label.setText(_translate("Form", "Shipping", None))
        self.tab_three_total_label.setText(_translate("Form", "Total", None))
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.check_out_tab), _translate("Form", "Check Out", None))
        self.tab_one_results_table_4.setSortingEnabled(True)
        item = self.tab_one_results_table_4.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(15)
        item.setText(_translate("Form", "16", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(16)
        item.setText(_translate("Form", "17", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(17)
        item.setText(_translate("Form", "18", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(18)
        item.setText(_translate("Form", "19", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(19)
        item.setText(_translate("Form", "20", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(20)
        item.setText(_translate("Form", "21", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(21)
        item.setText(_translate("Form", "22", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(22)
        item.setText(_translate("Form", "23", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(23)
        item.setText(_translate("Form", "24", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(24)
        item.setText(_translate("Form", "25", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(25)
        item.setText(_translate("Form", "26", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(26)
        item.setText(_translate("Form", "27", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(27)
        item.setText(_translate("Form", "28", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(28)
        item.setText(_translate("Form", "29", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(29)
        item.setText(_translate("Form", "30", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(30)
        item.setText(_translate("Form", "31", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(31)
        item.setText(_translate("Form", "32", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(32)
        item.setText(_translate("Form", "33", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(33)
        item.setText(_translate("Form", "34", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(34)
        item.setText(_translate("Form", "35", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(35)
        item.setText(_translate("Form", "36", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(36)
        item.setText(_translate("Form", "37", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(37)
        item.setText(_translate("Form", "38", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(38)
        item.setText(_translate("Form", "39", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(39)
        item.setText(_translate("Form", "40", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(40)
        item.setText(_translate("Form", "41", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(41)
        item.setText(_translate("Form", "42", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(42)
        item.setText(_translate("Form", "43", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(43)
        item.setText(_translate("Form", "44", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(44)
        item.setText(_translate("Form", "45", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(45)
        item.setText(_translate("Form", "46", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(46)
        item.setText(_translate("Form", "47", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(47)
        item.setText(_translate("Form", "48", None))
        item = self.tab_one_results_table_4.verticalHeaderItem(48)
        item.setText(_translate("Form", "50", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(0)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Artist", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Title", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Format", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Price Paid", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Sold Price (w/ tax)", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(7)
        item.setText(_translate("Form", "Date Sold", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(8)
        item.setText(_translate("Form", "New/Used", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Distributor", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Label", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Genre", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Year", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(13)
        item.setText(_translate("Form", "Date Added", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(14)
        item.setText(_translate("Form", "Discogs Release Number", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(15)
        item.setText(_translate("Form", "Real Name", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(16)
        item.setText(_translate("Form", "Profile", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(17)
        item.setText(_translate("Form", "Variations", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(18)
        item.setText(_translate("Form", "Aliases", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(19)
        item.setText(_translate("Form", "Track List", None))
        item = self.tab_one_results_table_4.horizontalHeaderItem(20)
        item.setText(_translate("Form", "Key", None))
        __sortingEnabled = self.tab_one_results_table_4.isSortingEnabled()
        self.tab_one_results_table_4.setSortingEnabled(False)
        self.tab_one_results_table_4.setSortingEnabled(__sortingEnabled)
        self.tab_three_total_label_2.setText(_translate("Form", "Total", None))
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.history_tab), _translate("Form", "History/Generate Reports", None))

        #other stuff
        self.tab_one_text_browser.setPlainText('\n')
        self.tab_one_results_table.horizontalHeader().setStretchLastSection(True)

        #make shift,-> a shortcut for adding stuff from search to checkout
        self.add_to_checkout_shortcut = QtGui.QShortcut(self)
        self.add_to_checkout_shortcut.setKey(QtGui.QKeySequence.SelectNextChar)
        self.search_inventory_tab.connect(self.add_to_checkout_shortcut,QtCore.SIGNAL("activated()"),self.tab_two_ctrl_a_shortcut)
        

        #displays recently added items on start up
        self.tab_one_update_recently_added_table()
        self.tab_two_reset_results_table()
        
        #combo box stuff
        for ii in range(self.num_attributes):
            self.tab_one_results_table.setCellWidget(ii,6,self.generate_new_used_combobox())
            self.tab_one_results_table.setCellWidget(ii,7,self.generate_distributor_combobox())
            
        #buttons in tab three
        self.tab_three_refresh_checkout_table()
        self.tab_three_checkout_table.horizontalHeader().setStretchLastSection(True)
        self.tab_three_final_checkout_table.horizontalHeader().setVisible(True)
        
        
        #set dates to current time in date time edit boxes
        self.tab_two_date_start.setCalendarPopup(True)
        self.tab_two_date_start.setDateTime(datetime.datetime.today())
        self.tab_two_date_end.setCalendarPopup(True)
        self.tab_two_date_end.setDateTime(datetime.datetime.today())

        #connectors bro *****************

        #connect tab one stuff
        self.tab_one_search_upc_button.clicked.connect(self.tab_one_search_for_upc)
        self.tab_one_search_upc_qline.returnPressed.connect(self.tab_one_search_for_upc)
        self.tab_one_add_selected_to_inventory.clicked.connect(self.tab_one_add_to_inventory)
        self.tab_one_search_artist_title_button.clicked.connect(self.tab_one_search_for_artist_title)
        self.tab_one_search_artist_title_title_qline.returnPressed.connect(self.tab_one_search_for_artist_title)
        self.tab_one_remove_selected_item_from_inventory.clicked.connect(self.tab_one_remove_from_inventory)
        self.tab_one_edit_selected_item.clicked.connect(self.tab_one_edit_inventory)
        self.tab_one_clear_all_button.clicked.connect(self.clear_tab_one_search_table)

        #connect tab two stuff
        self.tab_two_search_artist_title_qline.returnPressed.connect(self.search_inventory)
        self.tab_two_search_artist_title_button.clicked.connect(self.search_inventory)
        self.tab_two_reset_button.clicked.connect(self.tab_two_reset_results_table)
        self.tab_two_remove_selected_item_from_inventory.clicked.connect(self.tab_two_remove_from_inventory)
        self.tab_two_edit_selected_item.clicked.connect(self.tab_two_edit_inventory)
        self.tab_two_add_item_to_checkout.clicked.connect(self.add_inventory_to_checkout)
        
        #connect tab three stuff
        self.tab_three_scan_barcode_qline.returnPressed.connect(self.search_inventory_checkout)
        self.connect(self.tab_three_checkout_table,QtCore.SIGNAL("cellChanged(int, int)"),self.tab_three_percent_changed)
        self.connect(self.tab_three_discount_qline,QtCore.SIGNAL("returnPressed()"),self.tab_three_discount_qline_edited)
        self.connect(self.tab_three_percent_discount_qline,QtCore.SIGNAL("returnPressed()"),self.tab_three_percent_discount_qline_edited)
        self.tab_three_CREAM_button.clicked.connect(self.tab_three_make_a_cash_dialog)

    def tab_three_make_a_cash_dialog(self):
        if self.checkout_list:
            #wu-tang ain't nothin' to fuck with
            cream = Ui_CashDialog(self.checkout_total)
            paid_or_naaa = cream.exec_()
            if paid_or_naaa == QtGui.QDialog.Accepted:
                curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                sold_inventory_new_ids = []
                for row in self.checkout_list:
                    percent_discount = row[20]
                    sold_for = round(((100-percent_discount)*.01)*row[PRICE_INDEX],2)
                    #first add to sold_inventory DB
                    db_item = (self.xstr(row[UPC_INDEX]),
                               self.xstr(row[ARTIST_INDEX]),
                               self.xstr(row[TITLE_INDEX]),
                               self.xstr(row[FORMAT_INDEX]),
                               self.xfloat(row[PRICE_INDEX]),
                               self.xfloat(row[PRICE_PAID_INDEX]),
                               self.xstr(row[NEW_USED_INDEX]),
                               self.xstr(row[DISTRIBUTOR_INDEX]),
                               self.xstr(row[LABEL_INDEX]),
                               self.xstr(row[GENRE_INDEX]),
                               self.xint(row[YEAR_INDEX]),
                               self.xstr(row[DATE_ADDED_INDEX]),
                               self.xint(row[DISCOGS_RELEASE_NUMBER_INDEX]),
                               self.xstr(row[REAL_NAME_INDEX]),
                               self.xstr(row[PROFILE_INDEX]),
                               self.xstr(row[VARIATIONS_INDEX]),
                               self.xstr(row[ALIASES_INDEX]),
                               self.xstr(row[TRACK_LIST_INDEX]),
                               self.xstr(row[NOTES_INDEX]),
                               self.xstr(row[ID_INDEX]),
                               self.xfloat(sold_for),
                               self.xint(percent_discount),
                               curr_time,
                               self.xstr(row[21]),
                               0)
                    self.db_cursor.execute('INSERT INTO sold_inventory (upc, artist, title, format, price, price_paid, new_used, distributor, label, genre, year, date_added, discogs_release_number, real_name, profile, variations, aliases, track_list, notes, inventory_id, sold_for, percent_discount, date_sold, sold_notes, transaction_id) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', db_item)
                    self.db.commit()
                    sold_inventory_new_ids.append(str(self.db_cursor.lastrowid))
                #add to transactions DB
                final_checkout_percent_of_price = ((100-self.checkout_discount)*.01)
                discounted_price = round(final_checkout_percent_of_price*self.checkout_subtotal,2)
                tax_amount = round(discounted_price * 0.07,2)
                trans_item = (self.xint(len(self.checkout_list)),
                              curr_time,
                              self.xfloat(self.checkout_subtotal),
                              self.xfloat(self.checkout_discount),
                              self.xfloat(discounted_price),
                              self.xfloat(tax_amount),
                              self.xfloat(self.checkout_shipping),
                              self.xfloat(self.checkout_total),
                              self.xstr("Cash"),
                              self.xstr(",".join(sold_inventory_new_ids)))
                self.db_cursor.execute('INSERT INTO sold_transactions (number_of_items, date_sold, subtotal, discount_percent, discounted_price, tax, shipping, total, cash_credit, sold_ids) VALUES (?,?,?,?,?,?,?,?,?,?)', trans_item)
                self.db.commit()
                trans_id = self.db_cursor.lastrowid
                for item in sold_inventory_new_ids:
                    query = (trans_id, item)
                    self.db_cursor.execute('UPDATE sold_inventory SET transaction_id = ? WHERE id = ?', query)
                    self.db.commit()
                #delete from inventory DB
                for row in self.checkout_list:
                    date = row[DATE_ADDED_INDEX]
                    key = row[ID_INDEX]
                    self.db_cursor.execute('DELETE FROM inventory WHERE id = ? and date_added = ?', (key,date))
                    self.db.commit()

                self.checkout_list = []
                self.tab_three_refresh_checkout_table()

    def tab_three_percent_discount_qline_edited(self):
        text = self.tab_three_percent_discount_qline.text()
        to_number = self.string_with_percent_sign_to_int(text)
        if to_number >= 0 and to_number <= 100:
            self.checkout_discount = to_number
        self.tab_three_refresh_checkout_table()

    def tab_three_discount_qline_edited(self):
        text = self.tab_three_discount_qline.text()
        new_price = float(text)
        if new_price >= 0 and self.checkout_subtotal != 0:
            self.checkout_discount = (self.checkout_subtotal-new_price)/self.checkout_subtotal
        self.tab_three_refresh_checkout_table()

    def tab_three_percent_changed(self, row, col):
        if col == 5:
            text = self.tab_three_checkout_table.item(row, col).text()
            to_number = self.string_with_percent_sign_to_int(text)
            if to_number != int(self.checkout_list[row][20]) and to_number != -1 and to_number <= 100 and to_number >= 0:
                self.checkout_list[row][20] = to_number
            self.tab_three_refresh_checkout_table()
        elif col == 4:
            new_price = float(self.tab_three_checkout_table.item(row, col).text())
            if new_price >= 0:
                new_percent = new_price / self.checkout_list[row][PRICE_INDEX]
                new_percent = (1-new_percent)*100
                self.checkout_list[row][20] = new_percent
            self.tab_three_refresh_checkout_table()
        elif col == 9:
            self.checkout_list[row][21] = str(self.get_tab_three_checkout_table_text(row,col))
            self.tab_three_refresh_checkout_table()
            
                

    def string_with_percent_sign_to_int(self, string):
        string = string.replace('%','')
        try:
            return int(string)
        except Exception as e:
            print 'something happened when casting'
            return -1

    def tab_two_ctrl_a_shortcut(self):
        if self.main_menu_tabs.currentIndex() == 1:
            self.add_inventory_to_checkout()
        elif self.main_menu_tabs.currentIndex() == 0:
            self.tab_one_add_to_inventory()

    def tab_three_remove_row(self, value):
        del self.checkout_list[value]
        self.tab_three_refresh_checkout_table()
        print 'Row clicked: %d' % value
    
    def subtract_5_percent_from_item(self, value):
        self.checkout_list[value][20] = self.checkout_list[value][20] + 5
        self.tab_three_refresh_checkout_table()

    def add_inventory_to_checkout(self):
        row = self.tab_two_results_table.currentRow()
        key = int(self.get_tab_two_results_table_text(row,20))
        
        for row in self.db_cursor.execute('SELECT * FROM inventory WHERE id = ?', (key,)):
            row_list = list(row)
            row_list.append(0)
            row_list.append('')
            if not self.tab_three_is_duplicate_item(row[PRIMARY_KEY_INDEX]):
                self.checkout_list.append(row_list)
        self.tab_three_refresh_checkout_table()
        self.main_menu_tabs.setCurrentIndex(2)
        self.tab_three_scan_barcode_qline.clear()
        self.tab_three_scan_barcode_qline.setFocus()
            

    def search_inventory_checkout(self):
        barcode_query = str(self.tab_three_scan_barcode_qline.text())
        count = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc = ?', (barcode_query,)):
            count = count + 1

        if count == 1:
            #self.tab_three_checkout_table.setRowCount((len(self.checkout_list)+1))
            #add item to checkout
            for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc = ?', (barcode_query,)):
                row_list = list(row)
                row_list.append(0.0)
                row_list.append('')
                if not self.tab_three_is_duplicate_item(row[ID_INDEX]):
                    self.checkout_list.append(row_list)
            self.tab_three_refresh_checkout_table()
            self.tab_three_scan_barcode_qline.clear()
            self.tab_three_scan_barcode_qline.setFocus()
        else:
            self.search_list = []
            for row in self.db_cursor.execute('SELECT * FROM inventory WHERE upc = ? ORDER BY date_added ASC', (barcode_query,)):
               self.search_list.append(list(row))
            self.main_menu_tabs.setCurrentIndex(1)
            self.tab_two_results_table.selectRow(0)
            self.tab_two_results_table.scrollToTop()
            self.tab_two_results_table.setFocus()
            self.tab_two_refresh()
            
    def tab_three_is_duplicate_item(self, primary_key):
        for row in self.checkout_list:
            if row[ID_INDEX] == primary_key:
                return True
        return False


    def tab_three_refresh_checkout_table(self):
        self.clear_tab_three_final_checkout_table()
        self.tab_three_checkout_table.setRowCount(len(self.checkout_list))
        #loop through and populate table (both tables, this method should have been plural)
        checkout_table_index = 0
        self.checkout_subtotal = 0.0
        for row in self.checkout_list:
            percent_of_price = ((100-row[20])*.01)
            self.change_tab_three_checkout_table_text(checkout_table_index, 1, str(row[UPC_INDEX]))
            self.change_tab_three_checkout_table_text(checkout_table_index, 2, str(row[ARTIST_INDEX]))
            self.change_tab_three_checkout_table_text(checkout_table_index, 3, str(row[TITLE_INDEX]))
            #since i can only tell when a cell is changed, and not when return is pressed in a cell, there's no
            # way to tell if the cell is being changed by code or by the user. these next two lines trigger a sort
            #of infinite loop unless the cellChanged() signal is blocked on the table temporarily. there might
            #be a more elegant way to do this, but i can't figure it out
            self.tab_three_checkout_table.blockSignals(True)
            self.change_tab_three_checkout_table_text(checkout_table_index, 4, str(round(percent_of_price*row[PRICE_INDEX],2)))
            self.change_tab_three_checkout_table_text(checkout_table_index, 5, str('%d%%' % int(row[20])))
            self.change_tab_three_checkout_table_text(checkout_table_index, 7, str(row[NEW_USED_INDEX]))
            self.change_tab_three_checkout_table_text(checkout_table_index, 8, str(row[DATE_ADDED_INDEX]))
            self.change_tab_three_checkout_table_text(checkout_table_index, 9, str(row[21]))
            self.tab_three_checkout_table.blockSignals(False)#danger lies here
            self.change_tab_three_checkout_table_text(checkout_table_index, 10, str(row[ID_INDEX]))
            self.change_tab_three_checkout_table_text(checkout_table_index, 11, str(row[PRICE_PAID_INDEX]))
            self.change_tab_three_final_checkout_table_text(checkout_table_index, 0, str(row[ARTIST_INDEX] + ' - ' + row[TITLE_INDEX]))
            self.change_tab_three_final_checkout_table_text(checkout_table_index, 1, str(round(percent_of_price*row[PRICE_INDEX],2)))
            self.checkout_subtotal = self.checkout_subtotal + round((percent_of_price*row[PRICE_INDEX]),2)
            checkout_table_index = checkout_table_index + 1
        #fill in totals and stuff
        final_checkout_percent_of_price = ((100-self.checkout_discount)*.01)
        discounted_price = round(final_checkout_percent_of_price*self.checkout_subtotal,2)
        tax_amount = round(discounted_price * 0.07,2)
        self.tab_three_subtotal_qline.setText(str(self.checkout_subtotal))
        self.tab_three_percent_discount_qline.setText(str('%d%%' % int(self.checkout_discount)))
        self.tab_three_discount_qline.setText(str(discounted_price))
        self.tab_three_tax_amount_label.setText('$'+str(tax_amount))
        self.tab_three_shipping_qline.setText(str(round(self.checkout_shipping,2)))
        self.checkout_total = round(discounted_price+tax_amount,2)
        self.tab_three_total_qline.setText(str(self.checkout_total))
        self.tab_three_set_checkout_table_widths()
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        self.tab_three_inventory_count_label.setText('%s Items In Inventory' % str(how_many))

        


    def tab_two_reset_results_table(self):
        self.clear_tab_two_results_table()
        index = 0
        self.tab_two_num_displayed_spin_box.setValue(50)
        self.tab_two_date_start.setDateTime(datetime.datetime.today())
        self.tab_two_date_end.setDateTime(datetime.datetime.today())
        self.filter_by_date_added_checkbox.setCheckState(False)
        
        self.tab_two_results_table.setRowCount(self.tab_two_num_displayed_spin_box.value())
        self.search_list = []
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY date_added DESC'):
            self.search_list.append(row)
            #make sure we don't exceed the limits of the qtablewidget
            #if index > (self.tab_two_results_table.rowCount()-1):
            #    break
            #display stuff
            #for col in range(len(row)):
            #    self.change_tab_two_results_table_text(index, (col+1), str(row[col]))
            #index = index + 1
        self.tab_two_refresh()
        #make pretty
        #self.tab_two_results_table.resizeColumnsToContents()
        #update inventory count
        #how_many = 0
        #for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
        #    how_many = how_many + 1
        #self.tab_two_num_inventory_label.setText('%s Items In Inventory' % str(how_many))
        #self.tab_two_items_found_label.setText('%s Items Found For Search Terms' % str(how_many))


    def tab_two_remove_from_inventory(self):
        row = self.tab_two_results_table.currentRow()
        date = str(self.get_tab_two_results_table_text(row,12))
        key = int(self.get_tab_two_results_table_text(row,20))

        #remove her
        self.db_cursor.execute('DELETE FROM inventory WHERE id = ? and date_added = ?', (key, date))
        
        #commit
        self.db.commit()
        
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        self.tab_two_num_inventory_label.setText('%s Items In Inventory' % str(how_many))
        self.tab_two_items_found_label.setText('%s Items Found For Search Terms' % str(how_many))

        #research for current query so the table resets itself with chosen item removed
        self.search_inventory()
        
        
        
    def tab_one_remove_from_inventory(self):
        row = self.tab_one_recently_added_table.currentRow()
        #TODO: might want to replace this shiz with primary key stuff later
        #upc = str(self.get_tab_one_recently_added_table_text(row, 0))
        date = str(self.get_tab_one_recently_added_table_text(row, 11))
        key = int(self.get_tab_one_recently_added_table_text(row,19))
        #print key

        #remove her
        self.db_cursor.execute('DELETE FROM inventory WHERE id = ? and date_added = ?', (key, date))

        #commit
        self.db.commit()
        
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        #print '%s items in database' % str(how_many)
            

        #update the shiz
        self.tab_one_update_recently_added_table()

    def search_inventory(self):
        query = self.tab_two_search_artist_title_qline.text()
        if query == '':
            self.tab_two_reset_results_table()
            return
        
        #TODO: deleting this and recreating this every time is fucking idiotic, but #yolo for now since DB is small
        self.db_cursor.execute('DROP table IF EXISTS virt_inventory')
        self.db_cursor.execute('CREATE VIRTUAL TABLE IF NOT EXISTS virt_inventory USING fts4(key INT, content)')
        self.db.commit()
        self.db_cursor.execute("""INSERT INTO virt_inventory (key, content) SELECT id, upc || ' ' || artist || ' ' || title || ' ' || format || ' ' || label || ' ' || real_name || ' ' || profile || ' ' || variations || ' ' || aliases || ' ' || track_list || ' ' || notes || ' ' || date_added FROM inventory""")
        self.db.commit()
        #get search term
        SEARCH_FTS = """SELECT * FROM inventory WHERE id IN (SELECT key FROM virt_inventory WHERE content MATCH ?) ORDER BY date_added DESC"""
        self.db_cursor.execute(SEARCH_FTS, (str(query),))
        self.search_list = []
        for row in self.db_cursor.fetchall():
            #check date ranges if specified
            if self.filter_by_date_added_checkbox.isChecked():
                compare = (datetime.datetime.strptime(str(row[11]),"%Y-%m-%d %H:%M:%S")).date()
                start = self.tab_two_date_start.date().toPyDate()
                end = self.tab_two_date_end.date().toPyDate()
                range_delta = end - start
                compare_delta = end - compare
                zero_days = start - start
                if (compare_delta < zero_days) or (compare_delta > range_delta):
                    #current row is out of range
                    continue
            self.search_list.append(list(row))

        #update UI
        self.tab_two_refresh()

        #update inventory count
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        self.tab_two_num_inventory_label.setText('%s Items In Inventory' % str(how_many))
        #update number of results
        self.tab_two_items_found_label.setText('%s Items Found For Search Terms' % str(len(self.search_list)))

    #the redirection of stderr/stdout doesn't seem to work, still throws some weird error to console
    def tab_two_more_info_requested(self, row):
        actual_stdout = sys.stdout
        actual_stderr = sys.stderr
        if row <= len(self.search_list):
            try:
                sys.stdout = open(os.devnull, 'w')#sending to the black hole
                sys.stderr = open(os.devnull, 'w')#more victims of the black hole
                more_info = Ui_more_info_dialog()
                more_info.add_text(self.search_list[row])
                more_info.exec_()
            except Exception as e:
                this_is_a_placeholder = 0
        sys.stdout.flush()
        sys.stderr.flush()
        sys.stdout = actual_stdout
        sys.stderr = actual_stderr


    def tab_two_refresh(self):
        self.clear_tab_two_results_table()
        self.generate_more_info_buttons()
        index = 0
        for row in self.search_list:
            #don't exceed table length
            if index > (self.tab_two_results_table.rowCount()-1):
                index += 1
                continue
            
            #fill in table
            for col in range(len(row)):
                self.change_tab_two_results_table_text(index, (col+1), str(row[col]))
            
            index += 1
        self.tab_two_results_table.resizeColumnsToContents()
        self.tab_two_results_table.setColumnWidth(0,50)
        self.tab_two_results_table.setColumnWidth(4,200)
        #update inventory count
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        self.tab_two_num_inventory_label.setText('%s Items In Inventory' % str(how_many))
        self.tab_two_items_found_label.setText('%s Items Found For Search Terms' % str(how_many))

            

    def tab_two_edit_inventory(self):
        row = self.tab_two_results_table.currentRow()
        date = str(self.get_tab_two_results_table_text(row,12))
        key = int(self.get_tab_two_results_table_text(row,20))
        
        db_query = (str(self.get_tab_two_results_table_text(row, 1)),
                    str(self.get_tab_two_results_table_text(row,2)),
                    str(self.get_tab_two_results_table_text(row,3)),
                    str(self.get_tab_two_results_table_text(row,4)),
                    float(self.get_tab_two_results_table_text(row,5)),
                    float(self.get_tab_two_results_table_text(row,6)),
                    str(self.get_tab_two_results_table_text(row,7)),
                    str(self.get_tab_two_results_table_text(row,8)),
                    str(self.get_tab_two_results_table_text(row,9)),
                    str(self.get_tab_two_results_table_text(row,10)),
                    int(self.get_tab_two_results_table_text(row,11)),
                    int(self.get_tab_two_results_table_text(row,13)),
                    str(self.get_tab_two_results_table_text(row,14)),
                    str(self.get_tab_two_results_table_text(row,15)),
                    str(self.get_tab_two_results_table_text(row,16)),
                    str(self.get_tab_two_results_table_text(row,17)),
                    str(self.get_tab_two_results_table_text(row,18)),
                    str(self.get_tab_two_results_table_text(row,19)), key, date)
        
        #edit her
        self.db_cursor.execute('UPDATE inventory SET upc = ?, artist = ?, title = ?, format = ?, price = ?, price_paid = ?, new_used = ?, distributor = ?, label = ?, genre = ?, year = ?, discogs_release_number = ?, real_name = ?, profile = ?, variations = ?, aliases = ?, track_list = ?, notes = ? WHERE id = ? and date_added = ?', db_query)
        
        #commit
        self.db.commit()

        #redo search so that the table updates
        self.search_inventory()

    def tab_one_edit_inventory(self):
        row = self.tab_one_recently_added_table.currentRow()
        date = str(self.get_tab_one_recently_added_table_text(row, 11))
        key = int(self.get_tab_one_recently_added_table_text(row,19))

        db_query = (str(self.get_tab_one_recently_added_table_text(row, 0)),
                    str(self.get_tab_one_recently_added_table_text(row,1)),
                    str(self.get_tab_one_recently_added_table_text(row,2)),
                    str(self.get_tab_one_recently_added_table_text(row,3)),
                    float(self.get_tab_one_recently_added_table_text(row,4)),
                    float(self.get_tab_one_recently_added_table_text(row,5)),
                    str(self.get_tab_one_recently_added_table_text(row,6)),
                    str(self.get_tab_one_recently_added_table_text(row,7)),
                    str(self.get_tab_one_recently_added_table_text(row,8)),
                    str(self.get_tab_one_recently_added_table_text(row,9)),
                    int(self.get_tab_one_recently_added_table_text(row,10)),
                    int(self.get_tab_one_recently_added_table_text(row,12)),
                    str(self.get_tab_one_recently_added_table_text(row,13)),
                    str(self.get_tab_one_recently_added_table_text(row,14)),
                    str(self.get_tab_one_recently_added_table_text(row,15)),
                    str(self.get_tab_one_recently_added_table_text(row,16)),
                    str(self.get_tab_one_recently_added_table_text(row,17)),
                    str(self.get_tab_one_recently_added_table_text(row,18)), key, date)

        
        #edit her
        self.db_cursor.execute('UPDATE inventory SET upc = ?, artist = ?, title = ?, format = ?, price = ?, price_paid = ?, new_used = ?, distributor = ?, label = ?, genre = ?, year = ?, discogs_release_number = ?, real_name = ?, profile = ?, variations = ?, aliases = ?, track_list = ?, notes = ? WHERE id = ? and date_added = ?', db_query)
        
        #commit
        self.db.commit()

        #udate the gui
        self.tab_one_update_recently_added_table()
        
        
    def tab_one_add_to_inventory(self):
        row = self.tab_one_results_table.currentRow()
        #this guy is special, we want a different time for each addition to the DB
        curr_time = datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S")
        #now find stuff out about this release that we didn't do when the search results were displayed
        discogs_release_number = self.get_tab_one_results_table_text(row,12)
        errors = []
        real_name_db = ''
        profile_db = ''
        variations_db = ''
        aliases_db = ''
        tracks_db = ''
        notes_db = ''
        try:
            if discogs_release_number is not None: #did we find this on discogs or enter manually?
                discogs_release_number = str(discogs_release_number)
                #loop through previous results until we find the matching entry
                for result in self.previous_results:
                    if str(result.id) != discogs_release_number:
                        continue
                    #else, it's time to grab more info
                    #13 - real name ------------------------------
                    real_names = []
                    try:
                        for jj in range(len(result.artists)):
                            if result.artists[jj].real_name is not None:
                                real_names.append(result.artists[jj].real_name)
                        real_name_db = filter(lambda x: x in string.printable,", ".join(real_names))
                        #self.change_tab_one_results_table_text(ii,12,", ".join(real_names))
                    except Exception as e:
                    #    worked[12] = False
                        errors.append('Error on 12: %s\n' % e)
                    #14 - profile --------------------------------
                    profiles = []
                    try:
                        for jj in range(len(result.artists)):
                            if result.artists[jj].profile is not None:
                                profile = result.artists[jj].name
                                profile = profile + ' - ' + result.artists[jj].profile
                                profiles.append(profile)
                        profile_db = filter(lambda x: x in string.printable,"\n\n".join(profiles))
                    #    self.change_tab_one_results_table_text(ii,13,filter(lambda x: x in string.printable,"\n\n".join(profiles)))
                    except Exception as e:
                        #            worked[13] = False
                        errors.append('Error on 13: %s\n' % e)
                    #15 variations --------------------------------
                    variations = []
                    try:
                        for jj in range(len(result.artists)):
                            if result.artists[jj].name_variations is not None:
                                variation = ", ".join(result.artists[jj].name_variations)
                                variations.append(variation)
                        if variations:#this returns true if not empty
                            variations_db = filter(lambda x: x in string.printable,",".join(variations))
                            #self.change_tab_one_results_table_text(ii,14,filter(lambda x: x in string.printable,",".join(variations)))
                    except Exception as e:
                    #    worked[14] = False
                        errors.append('Error on 14: %s\n' % e)
                    #16 aliases -----------------------------------
                    aliases = []
                    try:
                        for jj in range(len(result.artists)):
                            temp = []
                            for artist in result.artists[jj].aliases:
                                temp.append(artist.name)
                            alias = ", ".join(temp)
                        aliases.append(alias)
                        aliases_db = filter(lambda x: x in string.printable,",".join(aliases))
                        #self.change_tab_one_results_table_text(ii,15,filter(lambda x: x in string.printable,",".join(aliases)))
                    except Exception as e:
                    #    worked[15] = False
                        errors.append('Error on 15: %s\n' % e)
                    #18 - Track List -------------------------------
                    tracks = []
                    try:
                        if result.tracklist is not None:
                            for t in result.tracklist:
                                tracks.append(('%s - %s - %s' % (t.position, t.duration, t.title)))
                            tracks_db = filter(lambda x: x in string.printable,"\n".join(tracks))
                            #self.change_tab_one_results_table_text(ii,17,"\n".join(tracks))
                    except Exception as e:
                    #    worked[17] = False
                        errors.append('Error on 17: %s\n' % e)
                    #19 - Notes -----------------------------------
                    try:
                        if result.notes is not None:
                            notes_db = filter(lambda x: x in string.printable,result.notes)
                            #self.change_tab_one_results_table_text(ii,18,filter(lambda x: x in string.printable,result.notes))
                    except Exception as e:
                    #    worked[18] = False
                        errors.append('Error on 18: %s\n' % e)
            if errors:
                self.print_to_console('There were a few issues adding the release, double check to make sure everything is OK:\n')
                self.print_to_console("\t".join(errors))
        except Exception as e:
            self.print_to_console('There was some error adding release, most likely an issue with discogs time limit, wait a second and then try again.')
            return
            
        try:
            
            #first add it to the database
            db_item = (self.xstr(self.get_tab_one_results_table_text(row, 0)),
                       self.xstr(self.get_tab_one_results_table_text(row,1)),
                       self.xstr(self.get_tab_one_results_table_text(row,2)),
                       self.xstr(self.get_tab_one_results_table_text(row,3)),
                       self.xfloat(self.get_tab_one_results_table_text(row,4)),
                       self.xfloat(self.get_tab_one_results_table_text(row,5)),
                       self.xstr(self.get_tab_one_results_table_text(row,6)),
                       self.xstr(self.get_tab_one_results_table_text(row,7)),
                       self.xstr(self.get_tab_one_results_table_text(row,8)),
                       self.xstr(self.get_tab_one_results_table_text(row,9)),
                       self.xint(self.get_tab_one_results_table_text(row,10)),
                       curr_time,
                       self.xint(self.get_tab_one_results_table_text(row,12)),
                       self.xstr(real_name_db),
                       self.xstr(profile_db),
                       self.xstr(variations_db),
                       self.xstr(aliases_db),
                       self.xstr(tracks_db),
                       self.xstr(notes_db))
            
            self.db_cursor.execute('INSERT INTO inventory (upc, artist, title, format, price, price_paid, new_used, distributor, label, genre, year, date_added, discogs_release_number, real_name, profile, variations, aliases, track_list, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', db_item)
            self.db.commit()
            #print self.db_cursor.lastrowid
            self.print_to_console('%s item added to database.\n' % str(self.get_tab_one_results_table_text(row,1))) 
        except Exception as e:
            self.print_to_console('Problem adding item to DB: %s' % e)

        #display in that young box as recently added
        self.tab_one_update_recently_added_table()

        #clear upc and artist/title search terms and give focus back to upc search box
        self.tab_one_search_upc_qline.setText('')
        self.tab_one_search_artist_title_title_qline.setText('')
        self.tab_one_search_upc_qline.setFocus()
 
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        #print '%s items in database' % str(how_many)

    def xstr(self,s):
        if s is None:
            return ''
        return str(s)
    
    def xint(self, i):
        if i is None:
            return -1
        return int(i)

    def xfloat(self, f):
        if f is None:
            return -1
        return float(f)

    def tab_one_update_recently_added_table(self):
        self.clear_tab_one_recently_added_table()
        index = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY date_added DESC'):
            #make sure we don't exceed the limits of the qtablewidget
            if index > (self.tab_one_recently_added_table.rowCount()-1):
                break
            #display stuff
            for col in range(len(row)):
                self.change_tab_one_recently_added_table_text(index, col, str(row[col]))
            index = index + 1
        #make pretty
        self.tab_one_recently_added_table.resizeColumnsToContents()
        #update inventory count
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        self.tab_one_num_inventory_label.setText('%s Items In Inventory' % str(how_many))


    def tab_one_search_for_upc(self):
        #get entered text and do sanity checks
        upc = str(self.tab_one_search_upc_qline.text())
        upc = self.discogs.clean_up_upc(upc)
        if(not self.discogs.does_this_even_make_sense(upc)):
            self.print_to_console(('This upc (%s) doesn\'t even make sense.\n' % upc))
            #self.tab_one_results_table.setRowCount(1)
            return
        else:
            self.tab_one_search_for_release(upc, False)

    def tab_one_search_for_artist_title(self):
        artist_title = str(self.tab_one_search_artist_title_title_qline.text())
        self.tab_one_search_for_release(artist_title, True)

    def tab_one_search_for_release(self, search_query, upc_needed):
        #clear table
        self.clear_tab_one_search_table()

        #add "cd", "vinyl", or "" to search term
        search_query_with_radio_button = search_query + self.get_tab_one_radio_button_input()
        worked = [True]*19

        #search
        self.print_to_console('Searching discogs...')
        try:
            results = self.discogs.search_for_release(search_query_with_radio_button)
            
            #save globally for use later
            self.previous_results = results
            #check sanity of response
            if results is None or len(results) == 0:
                self.print_to_console('\tNo match found on discogs for term: %s.\n' % search_query)
                self.tab_one_results_table.setRowCount(20)
                return
            self.print_to_console('\t%s results found on discogs for term: %s.\n' % (len(results), search_query))
            self.tab_one_results_table.setRowCount(20)
            ii = 0
            
            #loop through results and display
            for result in results:
                #udate the GUI
                QtGui.QApplication.processEvents()
                
                if ii == 20:
                    break
                worked = [True]*19
                errors = []
                #0 - upc -------------------------------------
                try:
                    if(upc_needed):
                        self.change_tab_one_results_table_text(ii,0,'BLANK')
                    else:
                        self.change_tab_one_results_table_text(ii,0,search_query)
                except Exception as e:
                    worked[0] = False
                    errors.append('Error on 0: %s\n' % e)
                #1 - artist --------------------------------
                #artists_ = []
                #try:
                #    for artist in result.artists:
                #        artists_.append(artist.name)
                #    self.change_tab_one_results_table_text(ii,1,", ".join(artists_))
                #except Exception as e:
                #    worked[1] = False
                #    errors.append('Error on 1: %s\n' % e)
                try:
                    artists_, title_ = result.title.rsplit('-',1)
                    self.change_tab_one_results_table_text(ii,1,artists_)
                except Exception as e:
                    worked[1] = False
                    errors.append('Error on 1: %s\n' % e)
                #TODO: this needs to be more "elegant"
                if 'Various' in artists_:
                    #TODO: clear row
                    self.change_tab_one_results_table_text(ii,0,'')
                    self.change_tab_one_results_table_text(ii,1,'')
                    continue
                #2 - title ---------------------------------
                try:
                    self.change_tab_one_results_table_text(ii,2,title_)
                except Exception as e:
                    worked[2] = False
                    errors.append('Error on 2: %s\n' % e)
                #3 - format---------------------------------
                format_ = ''
                try:
                    for jj in range(len(result.formats)):
                        if 'qty' in (result.formats[jj]):
                            format_ = format_ + (result.formats[jj])['qty'] + 'x'
                        if 'name' in (result.formats[jj]):
                            format_ = format_ + (result.formats[jj])['name'] + ', '
                        if 'descriptions' in (result.formats[jj]):
                            format_ = format_ + ", ".join((result.formats[jj])['descriptions'])
                        if jj != (len(result.formats)-1):
                            format_ = format_ + ' + '
                    self.change_tab_one_results_table_text(ii,3,str(filter(lambda x: x in string.printable,format_)))
                except Exception as e:
                    worked[3] = False
                    errors.append('Error on 3: %s\n' % e)
                #4 - price -----------------------------------
                #TODO: maybe do in parallel so it doesn't suck
                #prices = [None] * 3
                #self.discogs.scrape_price(result.id, prices)
                #if prices[0] != None:
                # self.change_tab_one_results_table_text(ii,4,prices[1])
                try:
                    self.change_tab_one_results_table_text(ii,4,'14.99')
                except Exception as e:
                    worked[4] = False
                    errors.append('Error on 4: %s\n' % e)
                #5 - price paid ------------------------------
                #print '\t8 - %s' % datetime.datetime.now()
                try:
                    self.change_tab_one_results_table_text(ii,5,str(9+ii))
                except Exception as e:
                    worked[7] = False
                    errors.append('Error on 7: %s\n' % e)
                #6 - new/used --------------------------------
                #TODO: select new or used based on something, i dunno yet
                #print '\t6 - %s' % datetime.datetime.now()
                try:
                    self.tab_one_results_table.setCellWidget(ii,6,self.generate_new_used_combobox())
                except Exception as e:
                        worked[5] = False
                        errors.append('Error on 5: %s\n' % e)
                #7 - distributor -----------------------------
                #TODO: select distributor based on most recent DB item
                #print '\t7 - %s' % datetime.datetime.now()
                try:
                    self.tab_one_results_table.setCellWidget(ii,7,self.generate_distributor_combobox())
                except Exception as e:
                    worked[6] = False
                    errors.append('Error on 6: %s\n' % e)
                    #self.change_tab_one_results_table_text(ii,6,'Fat Beats')
                #8 - label -----------------------------------
                try:
                    self.change_tab_one_results_table_text(ii,8,result.labels[0].name)
                except Exception as e:
                    worked[8] = False
                    errors.append('Error on 8: %s\n' % e)
                #9 - genre ----------------------------------
                try:
                    self.change_tab_one_results_table_text(ii,9,(", ".join(result.genres)))
                except Exception as e:
                    worked[9] = False
                    errors.append('Error on 9: %s\n' % e)
                #10 - year ----------------------------------
                try:
                    self.change_tab_one_results_table_text(ii,10,str(result.year))
                except Exception as e:
                    worked[10] = False
                    errors.append('Error on 10: %s\n' % e)
                #11 - date ----------------------------------
                try:
                    self.change_tab_one_results_table_text(ii,11,datetime.datetime.now().strftime("%Y-%m-%d %H:%M:%S"))
                except Exception as e:
                    worked[11] = False
                    errors.append('Error on 11: %s\n' % e)
                #12 - discogs release number -------------------
                try:
                    self.change_tab_one_results_table_text(ii,12,str(result.id))
                except Exception as e:
                    worked[16] = False
                    errors.append('Error on 12: %s\n' % e)

                ii = ii + 1
                if False in worked:
                    print "Errors adding title:"
                    print "\t%s" % ("\t".join(errors))

        except Exception as e:
            self.print_to_console('Something bad happened while searching for release: %s\n' % e)
            self.tab_one_results_table.setRowCount(20)
            self.clear_tab_one_search_table()
        
        #select first row
        self.tab_one_results_table.selectRow(0)
        self.tab_one_results_table.scrollToTop()
        self.tab_one_results_table.setFocus()
        self.tab_one_results_table.resizeColumnsToContents()
    


    def tab_three_set_checkout_table_widths(self):
        self.generate_remove_buttons()
        self.generate_5_perc_buttons()
        self.tab_three_checkout_table.resizeColumnsToContents()
        self.tab_three_checkout_table.setColumnWidth(0,50)
        self.tab_three_checkout_table.setColumnWidth(2,200)
        self.tab_three_checkout_table.setColumnWidth(3,200)
        self.tab_three_checkout_table.setColumnWidth(5,100)
        self.tab_three_checkout_table.setColumnWidth(6,50)
        self.tab_three_checkout_table.setColumnWidth(9,250)
        self.tab_three_final_checkout_table.setColumnWidth(0,200)

    def print_to_console(self, text):
        current_text = str(self.tab_one_text_browser.toPlainText())
        self.tab_one_text_browser.setPlainText(current_text + text)
        self.tab_one_text_browser.moveCursor(QtGui.QTextCursor.End)
    
    def get_tab_one_recently_added_table_text(self, row, col):
        item = self.tab_one_recently_added_table.item(row, col)
        if(item is not None):
            return item.text()
        else:
            return None

    def get_tab_two_results_table_text(self, row, col):
        item = self.tab_two_results_table.item(row, col)
        if item is not None:
            return item.text()
        else:
            return None

    def get_tab_one_results_table_text(self, row, col):
        if col in self.combobox_cols:
            widget = self.tab_one_results_table.cellWidget(row, col)
            #print widget.currentText()
            return widget.currentText()

        item = self.tab_one_results_table.item(row, col)
        if(item is not None):
            return item.text()
        else:
            return None

    def get_tab_three_checkout_table_text(self, row, col):
        item = self.tab_three_checkout_table.item(row, col)
        if item is not None:
            return item.text()
        else:
            return None

    def change_tab_one_results_table_text(self, row, col, text):
        text = str(filter(lambda x: x in string.printable,text))
        if col in self.combobox_cols:
            return
        item = self.tab_one_results_table.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.tab_one_results_table.setItem(row, col, item)

    def clear_tab_one_search_table(self):
        for ii in range(self.tab_one_results_table.rowCount()):
            for jj in range(self.tab_one_results_table.columnCount()):
                self.change_tab_one_results_table_text(ii,jj,"")

    def clear_tab_one_recently_added_table(self):
        for ii in range(self.tab_one_recently_added_table.rowCount()):
            for jj in range(self.tab_one_recently_added_table.columnCount()):
                self.change_tab_one_recently_added_table_text(ii,jj,"")

    def change_tab_one_recently_added_table_text(self, row, col, text):
        item = self.tab_one_recently_added_table.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.tab_one_recently_added_table.setItem(row, col, item)

    def clear_tab_two_results_table(self):
        for ii in range(self.tab_two_results_table.rowCount()):
            for jj in range(self.tab_two_results_table.columnCount()):
                self.change_tab_two_results_table_text(ii,jj,"")
        self.tab_two_results_table.setRowCount(self.tab_two_num_displayed_spin_box.value())
    
    def change_tab_two_results_table_text(self, row, col, text):
        text = str(filter(lambda x: x in string.printable, text))
        item = self.tab_two_results_table.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.tab_two_results_table.setItem(row, col, item)

    def clear_tab_three_checkout_(self):
        for ii in range(self.tab_three_checkout_table.rowCount()):
            for jj in range(self.tab_three_checkout_table.columnCount()):
                self.change_tab_three_checkout_table_text(ii,jj,"")
                
    def clear_tab_three_final_checkout_table(self):
        for ii in range(self.tab_three_final_checkout_table.rowCount()):
            for jj in range(self.tab_three_final_checkout_table.columnCount()):
                self.change_tab_three_final_checkout_table_text(ii,jj,"")

    def change_tab_three_checkout_table_text(self, row, col, text):
        text = str(filter(lambda x: x in string.printable, text))
        item = self.tab_three_checkout_table.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.tab_three_checkout_table.setItem(row, col, item)

    def change_tab_three_final_checkout_table_text(self, row, col, text):
        text = str(filter(lambda x: x in string.printable, text))
        item = self.tab_three_final_checkout_table.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.tab_three_final_checkout_table.setItem(row, col, item)

    def generate_new_used_combobox(self):
        combobox = QtGui.QComboBox()
        combobox.addItem("New")
        combobox.addItem("Used")
        return combobox
        
    def generate_distributor_combobox(self):
        combobox = QtGui.QComboBox()
        combobox.addItem("Fat Beats")
        combobox.addItem("Secretly Canadian")
        combobox.addItem("Other Distributor 2")
        combobox.addItem("Other Distributor 3")
        return combobox

    def generate_remove_buttons(self):
        #mapper stuff
        self.remove_mapper = QtCore.QSignalMapper(self)
        for ii in range(self.tab_three_checkout_table.rowCount()):
            button = QtGui.QPushButton('X')
            self.connect(button, QtCore.SIGNAL("clicked()"), self.remove_mapper, QtCore.SLOT("map()"))
            self.remove_mapper.setMapping(button, ii)            
            self.tab_three_checkout_table.setCellWidget(ii,0,button)
        self.connect(self.remove_mapper, QtCore.SIGNAL("mapped(int)"), self.tab_three_remove_row)


    def generate_5_perc_buttons(self):
        #more mapper stuff
        self.percent_mapper = QtCore.QSignalMapper(self)
        for ii in range(self.tab_three_checkout_table.rowCount()):
            button = QtGui.QPushButton('+5%')
            self.connect(button, QtCore.SIGNAL("clicked()"), self.percent_mapper, QtCore.SLOT("map()"))
            self.percent_mapper.setMapping(button,ii)
            self.tab_three_checkout_table.setCellWidget(ii,6,button)
        self.connect(self.percent_mapper, QtCore.SIGNAL("mapped(int)"), self.subtract_5_percent_from_item)

    def generate_more_info_buttons(self):
        self.more_info_mapper = QtCore.QSignalMapper(self)
        for ii in range(self.tab_two_results_table.rowCount()):
            button = QtGui.QPushButton('...')
            self.connect(button, QtCore.SIGNAL("clicked()"), self.more_info_mapper, QtCore.SLOT("map()"))
            self.more_info_mapper.setMapping(button, ii)
            self.tab_two_results_table.setCellWidget(ii,0,button)
        self.connect(self.more_info_mapper, QtCore.SIGNAL("mapped(int)"), self.tab_two_more_info_requested)

    def get_tab_one_radio_button_input(self):
        if self.tab_one_vinyl_radio_button.isChecked():
            return ' vinyl'
        if self.tab_one_cd_radio_button.isChecked():
            return ' cd'
        if self.tab_one_any_radio_button.isChecked():
            return ''


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.thread().setPriority(QtCore.QThread.TimeCriticalPriority)
    app.thread().setPriority(QtCore.QThread.HighestPriority)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())
