# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/more_info_dialog.ui'
#
# Created: Sat Nov  8 02:53:05 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui
from config_stuff import *

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

class Ui_more_info_dialog(QtGui.QDialog):
    def __init__(self):
        QtGui.QDialog.__init__(self)
        self.setupUi(self)

    def setupUi(self, more_info_dialog):
        more_info_dialog.setObjectName(_fromUtf8("more_info_dialog"))
        more_info_dialog.resize(1000, 1000)
        more_info_dialog.setMinimumSize(QtCore.QSize(1000, 1000))
        self.ok_button = QtGui.QPushButton(more_info_dialog)
        self.ok_button.setGeometry(QtCore.QRect(870, 950, 114, 32))
        self.ok_button.setObjectName(_fromUtf8("ok_button"))
        self.more_info_text_browser = QtGui.QTextBrowser(more_info_dialog)
        self.more_info_text_browser.setGeometry(QtCore.QRect(0, 0, 1001, 941))
        self.more_info_text_browser.setObjectName(_fromUtf8("more_info_text_browser"))
        self.retranslateUi(more_info_dialog)
        QtCore.QMetaObject.connectSlotsByName(more_info_dialog)

    def retranslateUi(self, more_info_dialog):
        more_info_dialog.setWindowTitle(_translate("more_info_dialog", "Dialog", None))
        self.ok_button.setText(_translate("more_info_dialog", "Cool", None))
        
        #connectors
        self.ok_button.clicked.connect(self.close)
        
    def add_text(self, row):
        all_the_stuff = []
        all_the_stuff.append('Artist                \t:\t%s' % row[ARTIST_INDEX])
        all_the_stuff.append('Title                 \t:\t%s' % row[TITLE_INDEX])
        all_the_stuff.append('UPC                   \t:\t%s' % row[UPC_INDEX])
        all_the_stuff.append('Format                \t:\t%s' % row[FORMAT_INDEX])
        all_the_stuff.append('Price                 \t:\t%s' % row[PRICE_INDEX])
        all_the_stuff.append('Price paid            \t:\t%s' % row[PRICE_PAID_INDEX])
        all_the_stuff.append('New/Used              \t:\t%s' % row[NEW_USED_INDEX])
        all_the_stuff.append('Distributor           \t:\t%s' % row[DISTRIBUTOR_INDEX])
        all_the_stuff.append('Label                 \t:\t%s' % row[LABEL_INDEX])
        all_the_stuff.append('Genre                 \t:\t%s' % row[GENRE_INDEX])
        all_the_stuff.append('Year                  \t:\t%s' % row[YEAR_INDEX])
        all_the_stuff.append('Date Added            \t:\t%s' % row[DATE_ADDED_INDEX])
        all_the_stuff.append('Discogs Release Number\t:\t%s' % row[DISCOGS_RELEASE_NUMBER_INDEX])
        all_the_stuff.append('Real Name             \t:\t%s' % row[REAL_NAME_INDEX])
        all_the_stuff.append('Profile               \t:\t%s' % row[PROFILE_INDEX])
        all_the_stuff.append('Variations            \t:\t%s' % row[VARIATIONS_INDEX])
        all_the_stuff.append('Aliases               \t:\t%s' % row[ALIASES_INDEX])
        track_list = row[TRACK_LIST_INDEX]
        track_list = track_list.replace('\n','\n\t')
        all_the_stuff.append('Track List            :\n\t%s' % track_list)
        all_the_stuff.append('Notes                 \t:\t%s' % row[NOTES_INDEX])
        all_the_stuff.append('Taxable               \t:\t%s' % str(row[TAXABLE_INDEX]))
        all_the_stuff.append('Primary Key           \t:\t%s' % row[ID_INDEX])
        if len(row) > 23:
            all_the_stuff.append('Sold For                \t:\t%s' % row[SOLD_FOR_INDEX])
            all_the_stuff.append('Percent Discount        \t:\t%s' % row[PERCENT_DISCOUNT_INDEX])
            all_the_stuff.append('Date Sold               \t:\t%s' % row[DATE_SOLD_INDEX])
            all_the_stuff.append('Sold Notes              \t:\t%s' % row[SOLD_NOTES_INDEX])
            all_the_stuff.append('Reorder State           \t:\t%s' % row[REORDER_STATE_INDEX])
            all_the_stuff.append('Transaction ID          \t:\t%s' % row[TRANSACTION_ID_INDEX])
            all_the_stuff.append('New Primary Key         \t:\t%s' % row[NEW_ID_INDEX])
        self.more_info_text_browser.setPlainText('\n'.join(all_the_stuff))

    def add_misc_text(self, row):
        all_the_stuff = []
        all_the_stuff.append('UPC            \t:\t%s' % row[MISC_UPC_INDEX])
        all_the_stuff.append('Type           \t:\t%s' % row[MISC_TYPE_INDEX])
        all_the_stuff.append('Item           \t:\t%s' % row[MISC_ITEM_INDEX])
        all_the_stuff.append('Description    \t:\t%s' % row[MISC_DESCRIPTION_INDEX])
        all_the_stuff.append('Size           \t:\t%s' % row[MISC_SIZE_INDEX])
        all_the_stuff.append('Price          \t:\t%s' % row[MISC_PRICE_INDEX])
        all_the_stuff.append('Price Paid     \t:\t%s' % row[MISC_PRICE_PAID_INDEX])
        all_the_stuff.append('Date Added     \t:\t%s' % row[MISC_DATE_ADDED_INDEX])
        all_the_stuff.append('New/Used       \t:\t%s' % row[MISC_NEW_USED_INDEX])
        all_the_stuff.append('Code           \t:\t%s' % row[MISC_CODE_INDEX])
        all_the_stuff.append('Distributor    \t:\t%s' % row[MISC_DISTRIBUTOR_INDEX])
        all_the_stuff.append('Taxable        \t:\t%s' % row[MISC_TAXABLE_INDEX])
        all_the_stuff.append('Reserved One   \t:\t%s' % row[MISC_RESERVED_ONE_INDEX])
        all_the_stuff.append('Reserved Two   \t:\t%s' % row[MISC_RESERVED_TWO_INDEX])
        all_the_stuff.append('Reserved Three \t:\t%s' % row[MISC_RESERVED_THREE_INDEX])
        all_the_stuff.append('Reserved Four  \t:\t%s' % row[MISC_RESERVED_FOUR_INDEX])
        all_the_stuff.append('Primary Key    \t:\t%s' % row[MISC_ID_INDEX])
        if len(row) > 17:
            all_the_stuff.append('Sold For         \t:\t%s' % row[MISC_SOLD_FOR_INDEX])
            all_the_stuff.append('Percent Discount \t:\t%s' % row[MISC_PERCENT_DISCOUNT_INDEX])
            all_the_stuff.append('Date Sold        \t:\t%s' % row[MISC_DATE_SOLD_INDEX])
            all_the_stuff.append('Sold Notes       \t:\t%s' % row[MISC_SOLD_NOTES_INDEX])
            all_the_stuff.append('Reorder State    \t:\t%s' % row[MISC_REORDER_STATE_INDEX])
            all_the_stuff.append('Transaction ID   \t:\t%s' % row[MISC_TRANSACTION_ID_INDEX])
            all_the_stuff.append('Reserved Five    \t:\t%s' % row[MISC_RESERVED_FIVE_INDEX])
            all_the_stuff.append('Reserved Six     \t:\t%s' % row[MISC_RESERVED_SIX_INDEX])
            all_the_stuff.append('New Primary Key  \t:\t%s' % row[MISC_NEW_ID_INDEX])
            
