# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'cekGirisUi.ui'
#
# Created by: PyQt5 UI code generator 5.15.7
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_widget(object):
    def setupUi(self, widget):
        widget.setObjectName("widget")
        widget.resize(700, 250)
        self.deCekTarihi = QtWidgets.QDateEdit(widget)
        self.deCekTarihi.setGeometry(QtCore.QRect(10, 60, 120, 30))
        self.deCekTarihi.setObjectName("deCekTarihi")
        self.cbFirmaAdi = QtWidgets.QComboBox(widget)
        self.cbFirmaAdi.setGeometry(QtCore.QRect(150, 60, 231, 30))
        self.cbFirmaAdi.setObjectName("cbFirmaAdi")
        self.label = QtWidgets.QLabel(widget)
        self.label.setGeometry(QtCore.QRect(10, 20, 120, 30))
        self.label.setObjectName("label")
        self.label_2 = QtWidgets.QLabel(widget)
        self.label_2.setGeometry(QtCore.QRect(160, 20, 120, 30))
        self.label_2.setObjectName("label_2")
        self.deCekVadesi = QtWidgets.QDateEdit(widget)
        self.deCekVadesi.setGeometry(QtCore.QRect(10, 170, 120, 30))
        self.deCekVadesi.setObjectName("deCekVadesi")
        self.label_3 = QtWidgets.QLabel(widget)
        self.label_3.setGeometry(QtCore.QRect(10, 130, 120, 30))
        self.label_3.setObjectName("label_3")
        self.label_4 = QtWidgets.QLabel(widget)
        self.label_4.setGeometry(QtCore.QRect(560, 20, 120, 30))
        self.label_4.setObjectName("label_4")
        self.lineEdit = QtWidgets.QLineEdit(widget)
        self.lineEdit.setGeometry(QtCore.QRect(560, 60, 120, 30))
        self.lineEdit.setObjectName("lineEdit")
        self.pushButton = QtWidgets.QPushButton(widget)
        self.pushButton.setGeometry(QtCore.QRect(560, 140, 120, 30))
        self.pushButton.setObjectName("pushButton")
        self.textEdit = QtWidgets.QTextEdit(widget)
        self.textEdit.setGeometry(QtCore.QRect(150, 140, 231, 60))
        self.textEdit.setObjectName("textEdit")
        self.label_5 = QtWidgets.QLabel(widget)
        self.label_5.setGeometry(QtCore.QRect(160, 100, 120, 30))
        self.label_5.setObjectName("label_5")
        self.label_6 = QtWidgets.QLabel(widget)
        self.label_6.setGeometry(QtCore.QRect(410, 20, 120, 30))
        self.label_6.setObjectName("label_6")
        self.lineEdit_2 = QtWidgets.QLineEdit(widget)
        self.lineEdit_2.setGeometry(QtCore.QRect(410, 60, 120, 30))
        self.lineEdit_2.setObjectName("lineEdit_2")

        self.retranslateUi(widget)
        QtCore.QMetaObject.connectSlotsByName(widget)

    def retranslateUi(self, widget):
        _translate = QtCore.QCoreApplication.translate
        widget.setWindowTitle(_translate("widget", "Çek Girişi"))
        self.label.setText(_translate("widget", "Çek Tarihi"))
        self.label_2.setText(_translate("widget", "Firma İsmi"))
        self.label_3.setText(_translate("widget", "Çek Vadesi"))
        self.label_4.setText(_translate("widget", "Tutar"))
        self.pushButton.setText(_translate("widget", "Kaydet"))
        self.label_5.setText(_translate("widget", "Açıklama"))
        self.label_6.setText(_translate("widget", "Çek Numarası"))


if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)
    widget = QtWidgets.QWidget()
    ui = Ui_widget()
    ui.setupUi(widget)
    widget.show()
    sys.exit(app.exec_())
