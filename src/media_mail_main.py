from PyQt4 import QtCore, QtGui
import sys
import os
from shipping_tester import MediaMail
import shopify

COLEMINE = 0
PLAID_ROOM = 1

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

class Ui_ShipPaypal(QtGui.QWidget):
    def __init__(self):
        QtGui.QWidget.__init__(self)
        self.shipping = MediaMail()
        
        self.setupUi(self)
    
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

        self.colemine_radio.toggle()

        self.go_button.clicked.connect(self.go_clicked)
        self.order_input.returnPressed.connect(self.go_clicked)
        self.reset_button.clicked.connect(self.reset_clicked)

    def go_clicked(self):
        print self.order_input.text()
        order_number = self.order_input.text()
        shopify_order = self.shipping.get_shopify_order(order_number)
        if shopify_order is not None:
            print 'order found'
        print shopify_order.attributes
        full_address = self.shipping.send_to_paypal(shopify_order)
        self.address_text_box.setText(full_address)

    def reset_clicked(self):
        if self.colemine_radio.isChecked():
            self.shipping.reset_shopify_connection(COLEMINE)
            print 'clmn is checked'
        elif self.plaid_room_radio.isChecked():
            self.shipping.reset_shopify_connection(PLAID_ROOM)
            print 'prr is checked'
        self.shipping.reset_paypal_browser()
        
if __name__ == '__main__':
    app = QtGui.QApplication(sys.argv)
    #app.thread().setPriority(QtCore.QThread.HighestPriority)
    ex = Ui_ShipPaypal()
    ex.show()

    sys.exit(app.exec_())
