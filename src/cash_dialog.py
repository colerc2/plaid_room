# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'src/cash_dialog.ui'
#
# Created: Sat Nov  8 04:58:49 2014
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

class Ui_CashDialog(QtGui.QDialog):
    def __init__(self, total_):
        QtGui.QDialog.__init__(self)
        self.total = total_
        self.setupUi(self)

    def setupUi(self, CashDialog):
        CashDialog.setObjectName(_fromUtf8("CashDialog"))
        CashDialog.resize(400, 300)
        self.cash_dialog_button_box = QtGui.QDialogButtonBox(CashDialog)
        self.cash_dialog_button_box.setGeometry(QtCore.QRect(30, 240, 341, 32))
        self.cash_dialog_button_box.setOrientation(QtCore.Qt.Horizontal)
        self.cash_dialog_button_box.setStandardButtons(QtGui.QDialogButtonBox.Cancel|QtGui.QDialogButtonBox.Ok)
        self.cash_dialog_button_box.setObjectName(_fromUtf8("cash_dialog_button_box"))
        self.widget = QtGui.QWidget(CashDialog)
        self.widget.setGeometry(QtCore.QRect(60, 40, 301, 191))
        self.widget.setObjectName(_fromUtf8("widget"))
        self.gridLayout = QtGui.QGridLayout(self.widget)
        self.gridLayout.setMargin(0)
        self.gridLayout.setObjectName(_fromUtf8("gridLayout"))
        self.total_label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.total_label.setFont(font)
        self.total_label.setObjectName(_fromUtf8("total_label"))
        self.gridLayout.addWidget(self.total_label, 0, 0, 1, 1)
        self.tendered_label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.tendered_label.setFont(font)
        self.tendered_label.setObjectName(_fromUtf8("tendered_label"))
        self.gridLayout.addWidget(self.tendered_label, 1, 0, 1, 1)
        self.tendered_qline = QtGui.QLineEdit(self.widget)
        self.tendered_qline.setAlignment(QtCore.Qt.AlignRight|QtCore.Qt.AlignTrailing|QtCore.Qt.AlignVCenter)
        self.tendered_qline.setObjectName(_fromUtf8("tendered_qline"))
        self.gridLayout.addWidget(self.tendered_qline, 1, 1, 1, 1)
        self.change_due_label = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.change_due_label.setFont(font)
        self.change_due_label.setObjectName(_fromUtf8("change_due_label"))
        self.gridLayout.addWidget(self.change_due_label, 2, 0, 1, 1)
        self.change_due_label_cash = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.change_due_label_cash.setFont(font)
        self.change_due_label_cash.setObjectName(_fromUtf8("change_due_label_cash"))
        self.gridLayout.addWidget(self.change_due_label_cash, 2, 1, 1, 1)
        self.total_label_cash = QtGui.QLabel(self.widget)
        font = QtGui.QFont()
        font.setFamily(_fromUtf8("Lucida Grande"))
        font.setPointSize(18)
        self.total_label_cash.setFont(font)
        self.total_label_cash.setObjectName(_fromUtf8("total_label_cash"))
        self.gridLayout.addWidget(self.total_label_cash, 0, 1, 1, 1)

        self.retranslateUi(CashDialog)
        QtCore.QObject.connect(self.cash_dialog_button_box, QtCore.SIGNAL(_fromUtf8("accepted()")), self.filter_return_pressed)
        QtCore.QObject.connect(self.cash_dialog_button_box, QtCore.SIGNAL(_fromUtf8("rejected()")), CashDialog.reject)
        QtCore.QMetaObject.connectSlotsByName(CashDialog)

    def retranslateUi(self, CashDialog):
        CashDialog.setWindowTitle(_translate("CashDialog", "Dialog", None))
        self.total_label.setText(_translate("CashDialog", "Total", None))
        self.tendered_label.setText(_translate("CashDialog", "Tendered", None))
        self.change_due_label.setText(_translate("CashDialog", "Change Due", None))
        self.change_due_label_cash.setText(_translate("CashDialog", "$X.XX", None))
        self.total_label_cash.setText(_translate("CashDialog", "$X.XX", None))

        #initialize stuff
        #self.cash_dialog_button_box.setDefault(False)
        #self.cash_dialog_button_box.setAutoDefault(False)
        self.total_label_cash.setText(str('$'+str(self.total)))
        
        #connect stuff
        self.connect(self.tendered_qline,QtCore.SIGNAL("editingFinished()"), self.display_change)
        
    def filter_return_pressed(self):
        if not self.tendered_qline.hasFocus():
            self.accept()
        else:
            self.cash_dialog_button_box.button(QtGui.QDialogButtonBox.Ok).setFocus()

    def display_change(self):
        try:
            tendered = float(self.tendered_qline.text())
            change_due = tendered - self.total
            self.change_due_label_cash.setText(str('$'+str(change_due)))
            #self.cash_dialog_button_box.setFocus()
        except Exception as e:
            placeholder = 'bad coding'
        
