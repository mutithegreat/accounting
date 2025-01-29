from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from alisFaturaUi import Ui_Form
import sqlite3

class AlisFaturasi(QWidget):
    def __init__(self):
        super().__init__()
        self.alisFatura = Ui_Form()
        self.alisFatura.setupUi(self)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT firma_adi FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.con.close()
        self.alisFatura.comboBox.addItems(sorted(firma_listesi))
        self.alisFatura.pushButton_2.clicked.connect(self.hesapla)
        self.alisFatura.pushButton.clicked.connect(self.kaydet)
        self.alisFatura.dateEdit.setCalendarPopup(True)
        self.alisFatura.dateEdit.setWrapping(True)
        self.alisFatura.dateEdit.setDate(QDate.currentDate())
        
    def hesapla(self):
        tutar = float(self.alisFatura.lineEditFaturaNo_2.text().replace(",","."))
        kdvOrani = int(self.alisFatura.comboBox_2.currentText())
        kdv = (kdvOrani * tutar) / 100
        self.alisFatura.lineEditFaturaNo_2.setText(str(tutar))
        self.alisFatura.lineEditFaturaNo_3.setText(str(kdv))
        toplamTutar = tutar + kdv
        self.alisFatura.lineEditFaturaNo_4.setText(str(toplamTutar))

        
    def kaydet(self):
        faturaTip = "af"
        day = str(self.alisFatura.dateEdit.date().day())
        month = str(self.alisFatura.dateEdit.date().month())
        year = str(self.alisFatura.dateEdit.date().year())
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month 
        ft = (year,month,day)
        faturaTarihi = "-".join(ft)
        faturaNumarasi = self.alisFatura.lineEditFaturaNo.text()
        cariAdi = self.alisFatura.comboBox.currentText()
        aciklama = self.alisFatura.textEdit.toPlainText()
        tutar = float(self.alisFatura.lineEditFaturaNo_2.text().replace(",","."))
        kdvOrani = int(self.alisFatura.comboBox_2.currentText())
        kdv = (kdvOrani * tutar) / 100
        self.alisFatura.lineEditFaturaNo_3.setText(str(kdv))
        toplamTutar = tutar + kdv
        self.alisFatura.lineEditFaturaNo_4.setText(str(toplamTutar))
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("insert into data (ftTarih ,ftNo,ftCariAdi,ftAciklama,ftTutar,ftKdv,ftToplam,ftTip) values(?,?,?,?,?,?,?,?)",(faturaTarihi,faturaNumarasi,cariAdi,aciklama,tutar,kdv,toplamTutar,faturaTip))
        self.con.commit()
        self.con.close()
        self.alisFatura.comboBox.setCurrentIndex(-1)
        self.alisFatura.dateEdit.setDate(QDate.currentDate())
        self.alisFatura.lineEditFaturaNo.clear()
        self.alisFatura.lineEditFaturaNo_2.clear()
        self.alisFatura.lineEditFaturaNo_3.clear()
        self.alisFatura.lineEditFaturaNo_4.clear()
        self.alisFatura.textEdit.clear()
        self.close()
        
        
        
        
        
        
        
        
        
        
