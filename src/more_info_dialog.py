# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/more_info_dialog.ui'
#
# Created: Sat Nov  8 02:53:05 2014
#      by: PyQt4 UI code generator 4.11.2
#
# WARNING! All changes made in this file will be lost!

from PyQt4 import QtCore, QtGui

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

