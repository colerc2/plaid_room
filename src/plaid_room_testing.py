# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'print_fucker.ui'
#
# Created: Tue Oct 14 18:52:25 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import sys
import discogs_client
from discogs_interface import DiscogsClient
import time

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
        self.setupUi(self)

        #not sure if this is where this shit should go
        self.discogs = DiscogsClient()

    def setupUi(self, Form):
        Form.setObjectName(_fromUtf8("Form"))
        Form.resize(1400, 800)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(Form.sizePolicy().hasHeightForWidth())
        Form.setSizePolicy(sizePolicy)
        Form.setMaximumSize(QtCore.QSize(1400, 800))
        self.horizontalLayout = QtGui.QHBoxLayout(Form)
        self.horizontalLayout.setObjectName(_fromUtf8("horizontalLayout"))
        self.tabWidget = QtGui.QTabWidget(Form)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Preferred, QtGui.QSizePolicy.Preferred)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tabWidget.sizePolicy().hasHeightForWidth())
        self.tabWidget.setSizePolicy(sizePolicy)
        self.tabWidget.setObjectName(_fromUtf8("tabWidget"))
        self.tab_3 = QtGui.QWidget()
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.tab_3.sizePolicy().hasHeightForWidth())
        self.tab_3.setSizePolicy(sizePolicy)
        self.tab_3.setObjectName(_fromUtf8("tab_3"))
        self.widget = QtGui.QWidget(self.tab_3)
        self.widget.setGeometry(QtCore.QRect(11, 11, 1302, 488))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.widget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.horizontalLayout_2 = QtGui.QHBoxLayout()
        self.horizontalLayout_2.setObjectName(_fromUtf8("horizontalLayout_2"))
        self.add_item_lbl = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.add_item_lbl.setFont(font)
        self.add_item_lbl.setScaledContents(False)
        self.add_item_lbl.setObjectName(_fromUtf8("add_item_lbl"))
        self.horizontalLayout_2.addWidget(self.add_item_lbl)
        self.add_item_vert_line = QtGui.QFrame(self.widget)
        self.add_item_vert_line.setFrameShape(QtGui.QFrame.VLine)
        self.add_item_vert_line.setFrameShadow(QtGui.QFrame.Sunken)
        self.add_item_vert_line.setObjectName(_fromUtf8("add_item_vert_line"))
        self.horizontalLayout_2.addWidget(self.add_item_vert_line)
        self.search_upc_box = QtGui.QLineEdit(self.widget)
        self.search_upc_box.setObjectName(_fromUtf8("search_upc_box"))
        self.horizontalLayout_2.addWidget(self.search_upc_box)
        self.search_upc_button = QtGui.QPushButton(self.widget)
        self.search_upc_button.setObjectName(_fromUtf8("search_upc_button"))
        self.horizontalLayout_2.addWidget(self.search_upc_button)
        self.search_artist_box = QtGui.QLineEdit(self.widget)
        self.search_artist_box.setObjectName(_fromUtf8("search_artist_box"))
        self.horizontalLayout_2.addWidget(self.search_artist_box)
        self.search_artist_button = QtGui.QPushButton(self.widget)
        self.search_artist_button.setObjectName(_fromUtf8("search_artist_button"))
        self.horizontalLayout_2.addWidget(self.search_artist_button)
        self.verticalLayout.addLayout(self.horizontalLayout_2)
        self.results_table = QtGui.QTableWidget(self.widget)
        sizePolicy = QtGui.QSizePolicy(QtGui.QSizePolicy.Maximum, QtGui.QSizePolicy.Maximum)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.results_table.sizePolicy().hasHeightForWidth())
        self.results_table.setSizePolicy(sizePolicy)
        self.results_table.setMinimumSize(QtCore.QSize(1300, 400))
        self.results_table.setObjectName(_fromUtf8("results_table"))
        self.results_table.setColumnCount(19)
        self.results_table.setRowCount(15)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setVerticalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(5, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(6, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(7, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(8, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(9, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(10, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(11, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(12, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(13, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(14, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(15, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(16, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(17, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setHorizontalHeaderItem(18, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setItem(0, 0, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setItem(0, 1, item)
        item = QtGui.QTableWidgetItem()
        self.results_table.setItem(0, 2, item)
        self.results_table.horizontalHeader().setCascadingSectionResizes(False)
        self.results_table.horizontalHeader().setDefaultSectionSize(100)
        self.results_table.horizontalHeader().setSortIndicatorShown(False)
        self.results_table.horizontalHeader().setStretchLastSection(False)
        self.verticalLayout.addWidget(self.results_table)
        self.horizontalLayout_3 = QtGui.QHBoxLayout()
        self.horizontalLayout_3.setObjectName(_fromUtf8("horizontalLayout_3"))
        self.add_to_inventory_button = QtGui.QPushButton(self.widget)
        self.add_to_inventory_button.setObjectName(_fromUtf8("add_to_inventory_button"))
        self.horizontalLayout_3.addWidget(self.add_to_inventory_button)
        self.inventory_count_lbl = QtGui.QLabel(self.widget)
        self.inventory_count_lbl.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.inventory_count_lbl.setObjectName(_fromUtf8("inventory_count_lbl"))
        self.horizontalLayout_3.addWidget(self.inventory_count_lbl)
        self.verticalLayout.addLayout(self.horizontalLayout_3)
        self.tabWidget.addTab(self.tab_3, _fromUtf8(""))
        self.tab_5 = QtGui.QWidget()
        self.tab_5.setObjectName(_fromUtf8("tab_5"))
        self.tabWidget.addTab(self.tab_5, _fromUtf8(""))
        self.tab_4 = QtGui.QWidget()
        self.tab_4.setObjectName(_fromUtf8("tab_4"))
        self.tabWidget.addTab(self.tab_4, _fromUtf8(""))
        self.horizontalLayout.addWidget(self.tabWidget)

        self.retranslateUi(Form)
        self.tabWidget.setCurrentIndex(0)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        Form.setWindowTitle(_translate("Form", "Plaid Room Records", None))
        self.add_item_lbl.setText(_translate("Form", "Add Item", None))
        self.search_upc_button.setText(_translate("Form", "Search UPC/SKU/EAN", None))
        self.search_artist_button.setText(_translate("Form", "Search Artist", None))
        item = self.results_table.verticalHeaderItem(0)
        item.setText(_translate("Form", "1", None))
        item = self.results_table.verticalHeaderItem(1)
        item.setText(_translate("Form", "2", None))
        item = self.results_table.verticalHeaderItem(2)
        item.setText(_translate("Form", "3", None))
        item = self.results_table.verticalHeaderItem(3)
        item.setText(_translate("Form", "4", None))
        item = self.results_table.verticalHeaderItem(4)
        item.setText(_translate("Form", "5", None))
        item = self.results_table.verticalHeaderItem(5)
        item.setText(_translate("Form", "6", None))
        item = self.results_table.verticalHeaderItem(6)
        item.setText(_translate("Form", "7", None))
        item = self.results_table.verticalHeaderItem(7)
        item.setText(_translate("Form", "8", None))
        item = self.results_table.verticalHeaderItem(8)
        item.setText(_translate("Form", "9", None))
        item = self.results_table.verticalHeaderItem(9)
        item.setText(_translate("Form", "10", None))
        item = self.results_table.verticalHeaderItem(10)
        item.setText(_translate("Form", "11", None))
        item = self.results_table.verticalHeaderItem(11)
        item.setText(_translate("Form", "12", None))
        item = self.results_table.verticalHeaderItem(12)
        item.setText(_translate("Form", "13", None))
        item = self.results_table.verticalHeaderItem(13)
        item.setText(_translate("Form", "14", None))
        item = self.results_table.verticalHeaderItem(14)
        item.setText(_translate("Form", "15", None))
        item = self.results_table.horizontalHeaderItem(0)
        item.setText(_translate("Form", "UPC/SKU/EAN", None))
        item = self.results_table.horizontalHeaderItem(1)
        item.setText(_translate("Form", "Artist", None))
        item = self.results_table.horizontalHeaderItem(2)
        item.setText(_translate("Form", "Title", None))
        item = self.results_table.horizontalHeaderItem(3)
        item.setText(_translate("Form", "Sale Price", None))
        item = self.results_table.horizontalHeaderItem(4)
        item.setText(_translate("Form", "Format", None))
        item = self.results_table.horizontalHeaderItem(5)
        item.setText(_translate("Form", "Label", None))
        item = self.results_table.horizontalHeaderItem(6)
        item.setText(_translate("Form", "Genre", None))
        item = self.results_table.horizontalHeaderItem(7)
        item.setText(_translate("Form", "New/Used", None))
        item = self.results_table.horizontalHeaderItem(8)
        item.setText(_translate("Form", "Year", None))
        item = self.results_table.horizontalHeaderItem(9)
        item.setText(_translate("Form", "Distributor", None))
        item = self.results_table.horizontalHeaderItem(10)
        item.setText(_translate("Form", "Date Added", None))
        item = self.results_table.horizontalHeaderItem(11)
        item.setText(_translate("Form", "Price Paid", None))
        item = self.results_table.horizontalHeaderItem(12)
        item.setText(_translate("Form", "Real Name", None))
        item = self.results_table.horizontalHeaderItem(13)
        item.setText(_translate("Form", "Profile", None))
        item = self.results_table.horizontalHeaderItem(14)
        item.setText(_translate("Form", "Variations", None))
        item = self.results_table.horizontalHeaderItem(15)
        item.setText(_translate("Form", "Aliases", None))
        item = self.results_table.horizontalHeaderItem(16)
        item.setText(_translate("Form", "Discogs Release Number", None))
        item = self.results_table.horizontalHeaderItem(17)
        item.setText(_translate("Form", "Track List", None))
        item = self.results_table.horizontalHeaderItem(18)
        item.setText(_translate("Form", "Notes", None))
        __sortingEnabled = self.results_table.isSortingEnabled()
        self.results_table.setSortingEnabled(False)
        self.results_table.setSortingEnabled(__sortingEnabled)
        self.add_to_inventory_button.setText(_translate("Form", "Add Selected Item To Inventory", None))
        self.inventory_count_lbl.setText(_translate("Form", "XXX items in inventory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_3), _translate("Form", "Add/Remove Inventory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_5), _translate("Form", "Search Inventory", None))
        self.tabWidget.setTabText(self.tabWidget.indexOf(self.tab_4), _translate("Form", "Check Out", None))
        
        self.search_upc_button.clicked.connect(self.search_for_upc)
        self.search_upc_box.returnPressed.connect(self.search_for_upc)

    def search_for_upc(self):
        self.clear_whole_table()
        upc_entered = str(self.search_upc_box.text())
        upc = self.discogs.clean_up_upc(upc_entered)
        if(not self.discogs.does_this_even_make_sense(upc)):
            print 'This upc (%s) doesn\'t even make sense.' % upc
        try:
            results = self.discogs.search_for_release(upc)
            
            #check validity of response
            if results is None or len(results) == 0:
                print 'No match found on discogs for upc %s.' % upc

            self.results_table.setRowCount(len(results))    
            #need to use a dict here to speed things up maybe
            for ii in range(len(results)):
                result = results[ii]
                self.change_table_text(ii,0,upc)
                self.change_table_text(ii,1,result.artists[0].name)
                self.change_table_text(ii,2,result.title)
                self.change_table_text(ii,3,'$9.99')
                self.change_table_text(ii,4,'N/A')
                self.change_table_text(ii,5,result.labels[0].name)
                self.change_table_text(ii,6,(", ".join(result.genres)))
                self.change_table_text(ii,7,'New')
                self.change_table_text(ii,8,str(result.year))
                

        except Exception as e:
            print 'Something bad happened while searching for release: %s' % e

    def change_table_text(self, row, col, text):
        item = self.results_table.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.results_table.setItem(row,col,item)

    def clear_tab_one_search_table(self):
        for ii in range(self.results_table.rowCount()):
            for jj in range(self.results_table.columnCount()):
                self.change_table_text(ii,jj,"")
                        

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    ex = Ui_Form()
    ex.show()
    sys.exit(app.exec_())