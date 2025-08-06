from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from satisFaturaUi import Ui_Form
import sqlite3

class SatisFaturasi(QWidget):
    def __init__(self):
        super().__init__()
        self.satisFatura = Ui_Form()
        self.satisFatura.setupUi(self)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT cari FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.con.close()
        self.satisFatura.comboBox.addItems(sorted(firma_listesi))
        self.satisFatura.pushButton_2.clicked.connect(self.hesapla)
        self.satisFatura.pushButton.clicked.connect(self.kaydet)
        self.satisFatura.dateEdit.setCalendarPopup(True)
        self.satisFatura.dateEdit.setWrapping(True)
        self.satisFatura.dateEdit.setDate(QDate.currentDate())
        
    def hesapla(self):
        tutar = float(self.satisFatura.lineEditFaturaNo_2.text().replace(",","."))
        kdvOrani = int(self.satisFatura.comboBox_2.currentText())
        kdv = (kdvOrani * tutar) / 100
        self.satisFatura.lineEditFaturaNo_2.setText(str(tutar))
        self.satisFatura.lineEditFaturaNo_3.setText(str(kdv))
        toplamTutar = tutar + kdv
        self.satisFatura.lineEditFaturaNo_4.setText(str(toplamTutar))

        
    def kaydet(self):
        faturaTip = "sf"
        day = str(self.satisFatura.dateEdit.date().day())
        month = str(self.satisFatura.dateEdit.date().month())
        year = str(self.satisFatura.dateEdit.date().year())
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month 
        ft = (year,month,day)
        faturaTarihi = "-".join(ft)
        faturaNumarasi = self.satisFatura.lineEditFaturaNo.text()
        cariAdi = self.satisFatura.comboBox.currentText()
        aciklama = self.satisFatura.textEdit.toPlainText()
        tutar = float(self.satisFatura.lineEditFaturaNo_2.text().replace(",","."))
        kdvOrani = int(self.satisFatura.comboBox_2.currentText())
        kdv = (kdvOrani * tutar) / 100
        self.satisFatura.lineEditFaturaNo_3.setText(str(kdv))
        toplamTutar = tutar + kdv
        self.satisFatura.lineEditFaturaNo_4.setText(str(toplamTutar))
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("insert into data (ftTarih ,ftNo,ftCariAdi,ftAciklama,ftTutar,ftKdv,ftToplam,ftTip) values(?,?,?,?,?,?,?,?)",(faturaTarihi,faturaNumarasi,cariAdi,aciklama,tutar,kdv,toplamTutar,faturaTip))
        self.con.commit()
        self.con.close()
        self.satisFatura.comboBox.setCurrentIndex(-1)
        self.satisFatura.dateEdit.setDate(QDate.currentDate())
        self.satisFatura.lineEditFaturaNo.clear()
        self.satisFatura.lineEditFaturaNo_2.clear()
        self.satisFatura.lineEditFaturaNo_3.clear()
        self.satisFatura.lineEditFaturaNo_4.clear()
        self.satisFatura.textEdit.clear()
        self.close()
        
        
        
        
        
        
