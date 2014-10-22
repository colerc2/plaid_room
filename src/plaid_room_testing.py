# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file '../learning_pyqt/second_test/print_fucker.ui'
#
# Created: Wed Oct 22 19:04:19 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import discogs_client
from discogs_interface import DiscogsClient
import time
import datetime
import sqlite3
import re
import string
from threading import Thread

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
        #DB stuff
        self.db = sqlite3.connect('inventory.db')
        self.db_cursor = self.db.cursor()
        #store previous set of results
        self.previous_results = None
        #create table
        self.db_cursor.execute("""CREATE TABLE IF NOT EXISTS inventory
        (upc text, artist text, title text, format text, price real, price_paid real, new_used text, distributor text, label text, genre text, year integer, date_added text, discogs_release_number integer, real_name text, profile text, variations text, aliases text, track_list text, notes text, id integer primary key autoincrement)
        """)
        self.num_attributes = 19
        self.combobox_cols = [6,7]
        
        self.setupUi(self)


    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1920, 1036)
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
        self.tab_one_results_table.horizontalHeader().setSortIndicatorShown(True)
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
        self.tab_two_results_table_2 = QtGui.QTableWidget(self.search_inventory_tab)
        self.tab_two_results_table_2.setGeometry(QtCore.QRect(10, 64, 1850, 400))
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_two_results_table_2.sizePolicy().hasHeightForWidth())
        self.tab_two_results_table_2.setSizePolicy(sizePolicy)
        self.tab_two_results_table_2.setMinimumSize(QtCore.QSize(1850, 400))
        self.tab_two_results_table_2.setObjectName(_fromUtf8("tab_two_results_table_2"))
        self.tab_two_results_table_2.setColumnCount(19)
        self.tab_two_results_table_2.setRowCount(15)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setHorizontalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.tab_two_results_table_2.setItem(0, 2, item)
        self.tab_two_results_table_2.horizontalHeader().setCascadingSectionResizes(False)
        self.tab_two_results_table_2.horizontalHeader().setDefaultSectionSize(100)
        self.tab_two_results_table_2.horizontalHeader().setSortIndicatorShown(False)
        self.tab_two_results_table_2.horizontalHeader().setStretchLastSection(False)
        self.layoutWidget1 = QtGui.QWidget(self.search_inventory_tab)
        self.layoutWidget1.setGeometry(QtCore.QRect(10, 20, 1850, 34))
        self.layoutWidget1.setObjectName(_fromUtf8("layoutWidget1"))
        self.horizontalLayout_5 = QtGui.QHBoxLayout(self.layoutWidget1)
        self.horizontalLayout_5.setMargin(0)
        self.horizontalLayout_5.setObjectName(_fromUtf8("horizontalLayout_5"))
        self.tab_two_search_item_lbl_2 = QtGui.QLabel(self.layoutWidget1)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tab_two_search_item_lbl_2.setFont(font)
        self.tab_two_search_item_lbl_2.setScaledContents(False)
        self.tab_two_search_item_lbl_2.setObjectName(_fromUtf8("tab_two_search_item_lbl_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_item_lbl_2)
        spacerItem22 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem22)
        self.add_item_vert_line_5 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_5.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_5.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_5.setObjectName(_fromUtf8("add_item_vert_line_5"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_5)
        spacerItem23 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem23)
        self.tab_two_search_upc_qline_2 = QtGui.QLineEdit(self.layoutWidget1)
        self.tab_two_search_upc_qline_2.setObjectName(_fromUtf8("tab_two_search_upc_qline_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_upc_qline_2)
        self.tab_two_search_upc_button_2 = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_search_upc_button_2.setObjectName(_fromUtf8("tab_two_search_upc_button_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_upc_button_2)
        spacerItem24 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem24)
        self.add_item_vert_line_6 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_6.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_6.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_6.setObjectName(_fromUtf8("add_item_vert_line_6"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_6)
        spacerItem25 = QtGui.QSpacerItem(28, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem25)
        self.tab_two_search_artist_qline_2 = QtGui.QLineEdit(self.layoutWidget1)
        self.tab_two_search_artist_qline_2.setText(_fromUtf8(""))
        self.tab_two_search_artist_qline_2.setObjectName(_fromUtf8("tab_two_search_artist_qline_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_qline_2)
        self.tab_two_search_artist_button_2 = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_search_artist_button_2.setObjectName(_fromUtf8("tab_two_search_artist_button_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_button_2)
        spacerItem26 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem26)
        self.add_item_vert_line_10 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_10.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_10.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_10.setObjectName(_fromUtf8("add_item_vert_line_10"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_10)
        spacerItem27 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem27)
        self.tab_two_search_artist_title_artist_qline_2 = QtGui.QLineEdit(self.layoutWidget1)
        self.tab_two_search_artist_title_artist_qline_2.setText(_fromUtf8(""))
        self.tab_two_search_artist_title_artist_qline_2.setObjectName(_fromUtf8("tab_two_search_artist_title_artist_qline_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_title_artist_qline_2)
        self.tab_two_search_artist_title_title_qline_2 = QtGui.QLineEdit(self.layoutWidget1)
        self.tab_two_search_artist_title_title_qline_2.setText(_fromUtf8(""))
        self.tab_two_search_artist_title_title_qline_2.setObjectName(_fromUtf8("tab_two_search_artist_title_title_qline_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_title_title_qline_2)
        self.tab_two_search_artist_title_button_2 = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_search_artist_title_button_2.setObjectName(_fromUtf8("tab_two_search_artist_title_button_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_search_artist_title_button_2)
        spacerItem28 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem28)
        self.add_item_vert_line_11 = QtGui.QFrame(self.layoutWidget1)
        self.add_item_vert_line_11.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line_11.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line_11.setObjectName(_fromUtf8("add_item_vert_line_11"))
        self.horizontalLayout_5.addWidget(self.add_item_vert_line_11)
        spacerItem29 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem29)
        self.tab_two_clear_all_button_2 = QtGui.QPushButton(self.layoutWidget1)
        self.tab_two_clear_all_button_2.setObjectName(_fromUtf8("tab_two_clear_all_button_2"))
        self.horizontalLayout_5.addWidget(self.tab_two_clear_all_button_2)
        spacerItem30 = QtGui.QSpacerItem(40, 20, QtGui.QSizePolicy.Expanding, QtGui.QSizePolicy.Minimum)
        self.horizontalLayout_5.addItem(spacerItem30)
        self.main_menu_tabs.addTab(self.search_inventory_tab, _fromUtf8(""))
        self.check_out_tab = QtGui.QWidget()
        self.check_out_tab.setObjectName(_fromUtf8("check_out_tab"))
        self.main_menu_tabs.addTab(self.check_out_tab, _fromUtf8(""))
        self.history_tab = QtGui.QWidget()
        self.history_tab.setObjectName(_fromUtf8("history_tab"))
        self.main_menu_tabs.addTab(self.history_tab, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.main_menu_tabs)

        self.retranslateUi(Form)
        self.main_menu_tabs.setCurrentIndex(0)
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
        self.tab_one_results_table.setSortingEnabled(True)
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
        item = self.tab_two_results_table_2.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.tab_two_results_table_2.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(0)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Artist", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Title", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Format", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Label", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Genre", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(7)
        item.setText(_translate("Form", "New/Used", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Year", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Distributor", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Date Added", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Price Paid", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Real Name", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(13)
        item.setText(_translate("Form", "Profile", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(14)
        item.setText(_translate("Form", "Variations", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(15)
        item.setText(_translate("Form", "Aliases", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(16)
        item.setText(_translate("Form", "Discogs Release Number", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(17)
        item.setText(_translate("Form", "Track List", None))
        item = self.tab_two_results_table_2.horizontalHeaderItem(18)
        item.setText(_translate("Form", "Notes", None))
        __sortingEnabled = self.tab_two_results_table_2.isSortingEnabled()
        self.tab_two_results_table_2.setSortingEnabled(False)
        self.tab_two_results_table_2.setSortingEnabled(__sortingEnabled)
        self.tab_two_search_item_lbl_2.setText(_translate("Form", "Search Item", None))
        self.tab_two_search_upc_button_2.setText(_translate("Form", "Search UPC/SKU/EAN", None))
        self.tab_two_search_artist_button_2.setText(_translate("Form", "Search Artist", None))
        self.tab_two_search_artist_title_button_2.setText(_translate("Form", "Search Artist/Title", None))
        self.tab_two_clear_all_button_2.setText(_translate("Form", "Clear All", None))
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.search_inventory_tab), _translate("Form", "Search/Edit/Remove Inventory", None))
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.check_out_tab), _translate("Form", "Check Out", None))
        self.main_menu_tabs.setTabText(self.main_menu_tabs.indexOf(self.history_tab), _translate("Form", "History/Generate Reports", None))


        #other stuff
        self.tab_one_text_browser.setPlainText('Let\'s sell some shit today nigga.\n')
        
        #displays recently added items on start up
        self.tab_one_update_recently_added_table()
        
        #combo box stuff
        for ii in range(self.num_attributes):
            self.tab_one_results_table.setCellWidget(ii,6,self.generate_new_used_combobox())
            self.tab_one_results_table.setCellWidget(ii,7,self.generate_distributor_combobox())

        #connectors bro *****************

        #connect tab one search upc button
        self.tab_one_search_upc_button.clicked.connect(self.tab_one_search_for_upc)
        self.tab_one_search_upc_qline.returnPressed.connect(self.tab_one_search_for_upc)
        self.tab_one_add_selected_to_inventory.clicked.connect(self.tab_one_add_to_inventory)
        self.tab_one_search_artist_title_button.clicked.connect(self.tab_one_search_for_artist_title)
        self.tab_one_search_artist_title_title_qline.returnPressed.connect(self.tab_one_search_for_artist_title)
        self.tab_one_remove_selected_item_from_inventory.clicked.connect(self.tab_one_remove_from_inventory)
        self.tab_one_edit_selected_item.clicked.connect(self.tab_one_edit_inventory)
        self.tab_one_clear_all_button.clicked.connect(self.clear_tab_one_search_table)
        

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
        discogs_release_number = str(self.get_tab_one_results_table_text(row,12))
        errors = []
        real_name_db = ''
        profile_db = ''
        variations_db = ''
        aliases_db = ''
        tracks_db = ''
        notes_db = ''
        if discogs_release_number is not None: #did we find this on discogs or enter manually?
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

                                    
        
        try:
            #first add it to the database
            db_item = (str(self.get_tab_one_results_table_text(row, 0)),
                       str(self.get_tab_one_results_table_text(row,1)),
                       str(self.get_tab_one_results_table_text(row,2)),
                       str(self.get_tab_one_results_table_text(row,3)),
                       float(self.get_tab_one_results_table_text(row,4)),
                       float(self.get_tab_one_results_table_text(row,5)),
                       str(self.get_tab_one_results_table_text(row,6)),
                       str(self.get_tab_one_results_table_text(row,7)),
                       str(self.get_tab_one_results_table_text(row,8)),
                       str(self.get_tab_one_results_table_text(row,9)),
                       int(self.get_tab_one_results_table_text(row,10)),
                       curr_time,
                       int(self.get_tab_one_results_table_text(row,12)),
                       str(real_name_db),
                       str(profile_db),
                       str(variations_db),
                       str(aliases_db),
                       str(tracks_db),
                       str(notes_db))
            
            self.db_cursor.execute('INSERT INTO inventory (upc, artist, title, format, price, price_paid, new_used, distributor, label, genre, year, date_added, discogs_release_number, real_name, profile, variations, aliases, track_list, notes) VALUES (?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?,?)', db_item)
            self.db.commit()
            #print self.db_cursor.lastrowid
            self.print_to_console('%s item added to database.\n' % str(self.get_tab_one_results_table_text(row,1))) 
        except Exception as e:
            self.print_to_console('Problem adding item to DB: %s' % e)

        #display in that young box as recently added
        self.tab_one_update_recently_added_table()
 
        how_many = 0
        for row in self.db_cursor.execute('SELECT * FROM inventory ORDER BY upc DESC'):
            how_many = how_many + 1
        #print '%s items in database' % str(how_many)

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
        #curr_thread.setPriority(QtCore.QThread.TimeCriticalPriority)
        #curr_thread.setPriority(QtCore.QThread.HighestPriority)

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
        #resize columns
        self.tab_one_results_table.resizeColumnsToContents()
                                                                                                                                                                                



        
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

    def generate_new_used_combobox(self):
        combobox = QtGui.QComboBox()
        combobox.addItem("New")
        combobox.addItem("Used")
        return combobox
        
    def generate_distributor_combobox(self):
        combobox = QtGui.QComboBox()
        combobox.addItem("Fat Beats")
        combobox.addItem("Other Distributor 1")
        combobox.addItem("Other Distributor 2")
        combobox.addItem("Other Distributor 3")
        return combobox

    def get_tab_one_radio_button_input(self):
        if self.tab_one_vinyl_radio_button.isChecked():
            return ' vinyl'
        if self.tab_one_cd_radio_button.isChecked():
            return ' cd'
        if self.tab_one_any_radio_button.isChecked():
            return ''


if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    print 'shit %s' % app.thread().priority()
    #app.thread().setPriority(QtCore.QThread.TimeCriticalPriority)
    app.thread().setPriority(QtCore.QThread.HighestPriority)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())
