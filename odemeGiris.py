from PyQt5.QtWidgets import *
from odemeGirisUi import Ui_widget
from PyQt5.QtCore import QDate
import sqlite3

class OdemeGiris(QWidget):
    def __init__(self):
        super().__init__()
        self.odemeGirisi = Ui_widget()
        self.odemeGirisi.setupUi(self)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT cari FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.con.close()
        self.odemeGirisi.cbFirmaAdi.addItems(sorted(firma_listesi))
        self.odemeGirisi.deOdemeTarihi.setCalendarPopup(True)
        self.odemeGirisi.deOdemeTarihi.setWrapping(True)
        self.odemeGirisi.deOdemeTarihi.setDate(QDate.currentDate())
        self.odemeGirisi.pushButton.clicked.connect(self.gelenOdemeKaydet)
        
    def gelenOdemeKaydet(self):
        #Gelen ödemeler veritabanı odeme sayfasına durumu 'go' olarak kayıt edilir.
        durum = "go"
        day = str(self.odemeGirisi.deOdemeTarihi.date().day())
        month = str(self.odemeGirisi.deOdemeTarihi.date().month())
        year = str(self.odemeGirisi.deOdemeTarihi.date().year())
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month
        ft = (year,month,day)
        odemeTarihi = "-".join(ft)
        firmaAdi = self.odemeGirisi.cbFirmaAdi.currentText()
        aciklama = self.odemeGirisi.textEdit.toPlainText()
        tutar = float(self.odemeGirisi.leOdemeTutar.text())
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("insert into odeme(odemeTarih,FirmaAdi,Aciklama,tutar,odemeTip) values(?,?,?,?,?)",(odemeTarihi,firmaAdi,aciklama,tutar,durum))
        self.con.commit()
        self.odemeGirisi.deOdemeTarihi.setDate(QDate.currentDate())
        self.odemeGirisi.cbFirmaAdi.setCurrentIndex(-1)
        self.odemeGirisi.textEdit.clear()
        self.odemeGirisi.leOdemeTutar.clear()
        self.close()
        