# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/shopify_to_media_mail_integration.ui'
#
# Created: Sat Sep 17 07:52:19 2016
#      by: PyQt4 UI code generator 4.11.1
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

class Ui_ShipPaypal(object):
    def setupUi(self, ShipPaypal):
        ShipPaypal.setObjectName(_fromUtf8("ShipPaypal"))
        ShipPaypal.resize(523, 394)
        self.go_button = QtGui.QPushButton(ShipPaypal)
        self.go_button.setGeometry(QtCore.QRect(49, 110, 211, 71))
        self.go_button.setObjectName(_fromUtf8("go_button"))
        self.order_input = QtGui.QLineEdit(ShipPaypal)
        self.order_input.setGeometry(QtCore.QRect(60, 50, 191, 31))
        self.order_input.setObjectName(_fromUtf8("order_input"))
        self.reset_button = QtGui.QPushButton(ShipPaypal)
        self.reset_button.setGeometry(QtCore.QRect(300, 110, 191, 71))
        self.reset_button.setObjectName(_fromUtf8("reset_button"))
        self.address_text_box = QtGui.QTextBrowser(ShipPaypal)
        self.address_text_box.setGeometry(QtCore.QRect(60, 190, 431, 141))
        self.address_text_box.setObjectName(_fromUtf8("address_text_box"))
        self.layoutWidget = QtGui.QWidget(ShipPaypal)
        self.layoutWidget.setGeometry(QtCore.QRect(310, 30, 171, 71))
        self.layoutWidget.setObjectName(_fromUtf8("layoutWidget"))
        self.verticalLayout = QtGui.QVBoxLayout(self.layoutWidget)
        self.verticalLayout.setMargin(0)
        self.verticalLayout.setObjectName(_fromUtf8("verticalLayout"))
        self.colemine_radio = QtGui.QRadioButton(self.layoutWidget)
        self.colemine_radio.setObjectName(_fromUtf8("colemine_radio"))
        self.verticalLayout.addWidget(self.colemine_radio)
        self.plaid_room_radio = QtGui.QRadioButton(self.layoutWidget)
        self.plaid_room_radio.setObjectName(_fromUtf8("plaid_room_radio"))
        self.verticalLayout.addWidget(self.plaid_room_radio)

        self.retranslateUi(ShipPaypal)
        QtCore.QMetaObject.connectSlotsByName(ShipPaypal)

    def retranslateUi(self, ShipPaypal):
        ShipPaypal.setWindowTitle(_translate("ShipPaypal", "Ship Paypal", None))
        self.go_button.setText(_translate("ShipPaypal", "Go!", None))
        self.reset_button.setText(_translate("ShipPaypal", "Reset", None))
        self.colemine_radio.setText(_translate("ShipPaypal", "Colemine Shopify", None))
        self.plaid_room_radio.setText(_translate("ShipPaypal", "Plaid Room Shopify", None))

if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.thread().setPriority(QtCore.QThread.HighestPriority)
    ex = Ui_Form()
    ex.show()

    sys.exit(app.exec_())
