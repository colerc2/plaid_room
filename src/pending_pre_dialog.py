# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/pending_pre_dialog.ui'
#
# Created: Tue Nov 22 00:37:25 2016
#      by: PyQt4 UI code generator 4.11.3
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
import locale
import string
import re


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

class Ui_Pending_Dialog(QtGui.QDialog):
    def __init__(self, pre_order_list_):
        QtGui.QDialog.__init__(self)
        locale.setlocale(locale.LC_ALL, '')
        self.pre_order_list = pre_order_list_
        self.id_to_attach_to = -1
        self.setupUi(self)
    
    def setupUi(self, Dialog):
        Dialog.setObjectName(_fromUtf8("Dialog"))
        Dialog.resize(1339, 627)
        self.buttonBox = QtGui.QDialogButtonBox(Dialog)
        self.buttonBox.setGeometry(QtCore.QRect(960, 570, 341, 32))
        self.buttonBox.setOrientation(QtCore.Qt.Horizontal)
        self.buttonBox.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.buttonBox.setObjectName(_fromUtf8("buttonBox"))
        self.pending_table_widget = QtGui.QTableWidget(Dialog)
        self.pending_table_widget.setGeometry(QtCore.QRect(20, 20, 1291, 531))
        self.pending_table_widget.setSelectionBehavior(QtGui.QAbstractItemView.SelectRows)
        self.pending_table_widget.setObjectName(_fromUtf8("pending_table_widget"))
        self.pending_table_widget.setColumnCount(6)
        self.pending_table_widget.setRowCount(0)
        item = QtGui.QTableWidgetItem()
        self.pending_table_widget.setHorizontalHeaderItem(0, item)
        item = QtGui.QTableWidgetItem()
        self.pending_table_widget.setHorizontalHeaderItem(1, item)
        item = QtGui.QTableWidgetItem()
        self.pending_table_widget.setHorizontalHeaderItem(2, item)
        item = QtGui.QTableWidgetItem()
        self.pending_table_widget.setHorizontalHeaderItem(3, item)
        item = QtGui.QTableWidgetItem()
        self.pending_table_widget.setHorizontalHeaderItem(4, item)
        item = QtGui.QTableWidgetItem()
        self.pending_table_widget.setHorizontalHeaderItem(5, item)

        self.retranslateUi(Dialog)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("accepted()")), self.ok_pressed)
        QtCore.QObject.connect(self.buttonBox, QtCore.SIGNAL(_fromUtf8("rejected()")), Dialog.reject)
        QtCore.QMetaObject.connectSlotsByName(Dialog)

    def retranslateUi(self, Dialog):
        Dialog.setWindowTitle(_translate("Dialog", "Pending Pre-Orders", None))
        item = self.pending_table_widget.horizontalHeaderItem(0)
        item.setText(_translate("Dialog", "UPC", None))
        item = self.pending_table_widget.horizontalHeaderItem(1)
        item.setText(_translate("Dialog", "Name", None))
        item = self.pending_table_widget.horizontalHeaderItem(2)
        item.setText(_translate("Dialog", "Artist", None))
        item = self.pending_table_widget.horizontalHeaderItem(3)
        item.setText(_translate("Dialog", "Title", None))
        item = self.pending_table_widget.horizontalHeaderItem(4)
        item.setText(_translate("Dialog", "Date", None))
        item = self.pending_table_widget.horizontalHeaderItem(5)
        item.setText(_translate("Dialog", "id", None))

        #initialize stuff
        self.fill_in_table()
        #connect stuff

    def fill_in_table(self):
        self.pending_table_widget.setRowCount(len(self.pre_order_list))
        for ix, row in enumerate(self.pre_order_list):
            self.change_text(ix, 0, str(row[0]))
            self.change_text(ix, 1, str(row[1]))
            self.change_text(ix, 2, str(row[2]))
            self.change_text(ix, 3, str(row[3]))
            self.change_text(ix, 4, str(row[4]))
            self.change_text(ix, 5, str(row[5]))
        self.pending_table_widget.resizeColumnsToContents()

    def change_text(self, row, col, text):
        self.filter_unprintable(text)
        item = self.pending_table_widget.item(row, col)
        if item is not None:
            item.setText(text)
        else:
            item = QtGui.QTableWidgetItem()
            item.setText(text)
            self.pending_table_widget.setItem(row, col, item)
        
    def ok_pressed(self):
        row = self.pending_table_widget.currentRow()
        self.id_to_attach_to = self.pre_order_list[row][5]
        print 'id to attach to %s' % self.id_to_attach_to
        print self.pre_order_list
        self.accept()

    def get_id(self):
        return self.id_to_attach_to


    def filter_unprintable(self, str_):
        return filter(lambda x: x in string.printable, str_)

