# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/more_info_dialog.ui'
#
# Created: Sat Nov  8 02:53:05 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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
        all_the_stuff.append('Artist:\t%s' % row[ARTIST_INDEX])
        all_the_stuff.append('Title:\t%s' % row[TITLE_INDEX])
        all_the_stuff.append('UPC:\t%s' % row[UPC_INDEX])
        all_the_stuff.append('Format:\t%s' % row[FORMAT_INDEX])
        all_the_stuff.append('Price:\t%s' % row[PRICE_INDEX])
        all_the_stuff.append('Price paid:\t%s' % row[PRICE_PAID_INDEX])
        all_the_stuff.append('New/Used:\t%s' % row[NEW_USED_INDEX])
        all_the_stuff.append('Distributor:\t%s' % row[DISTRIBUTOR_INDEX])
        all_the_stuff.append('Label:\t%s' % row[LABEL_INDEX])
        all_the_stuff.append('Genre:\t%s' % row[GENRE_INDEX])
        all_the_stuff.append('Year:\t%s' % row[YEAR_INDEX])
        all_the_stuff.append('Date Added:\t%s' % row[DATE_ADDED_INDEX])
        all_the_stuff.append('Discogs Release Number:\t%s' % row[DISCOGS_RELEASE_NUMBER_INDEX])
        all_the_stuff.append('Real Name:\t%s' % row[REAL_NAME_INDEX])
        all_the_stuff.append('Profile:\t%s' % row[PROFILE_INDEX])
        all_the_stuff.append('Variations:\t%s' % row[VARIATIONS_INDEX])
        all_the_stuff.append('Aliases:\t%s' % row[ALIASES_INDEX])
        track_list = row[TRACK_LIST_INDEX]
        track_list = track_list.replace('\n','\n\t')
        all_the_stuff.append('Track List:\n\t%s' % track_list)
        all_the_stuff.append('Notes:\t%s' % row[NOTES_INDEX])
        all_the_stuff.append('Primary Key:\t%s' % row[ID_INDEX])
        self.more_info_text_browser.setPlainText('\n'.join(all_the_stuff))
