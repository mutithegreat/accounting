from PyQt5.QtWidgets import *
from cariListesiUi import Ui_Form
import sqlite3
from PyQt5.QtCore import pyqtSignal


class CariListesi(QWidget):
    data_updated = pyqtSignal()
    def __init__(self):
        super().__init__()
        self.cariListesi = Ui_Form()
        self.cariListesi.setupUi(self)
        self.cariListesi.pushButton.clicked.connect(self.firmaKaydet)
    
    def firmaKaydet(self):
        firmaAdi = self.cariListesi.lineEdit.text()
        firmaAdresi = self.cariListesi.textEdit.toPlainText()
        vergiDairesi = self.cariListesi.lineEdit_2.text()
        vergiNo = self.cariListesi.lineEdit_3.text()
        telefon = self.cariListesi.lineEdit_4.text()
        mail = self.cariListesi.lineEdit_5.text()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("Insert into cari_kart(cari , adres ,vergi_dairesi , vergi_no , telefon , mail_adresi) values(?,?,?,?,?,?)",(firmaAdi,firmaAdresi,vergiDairesi,vergiNo,telefon,mail))
        self.con.commit()
        self.con.close()
        self.cariListesi.lineEdit.clear()
        self.cariListesi.lineEdit_2.clear()
        self.cariListesi.lineEdit_3.clear()
        self.cariListesi.lineEdit_4.clear()
        self.cariListesi.lineEdit_5.clear()
        self.cariListesi.textEdit.clear()
        self.data_updated.emit()
        self.close()
        
        
        
        