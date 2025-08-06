from PyQt5 import QtCore
from PyQt5.QtWidgets import *
from PyQt5.QtWidgets import QWidget
from yapilanodemeGirisUi import Ui_widget
from PyQt5.QtCore import QDate
import sqlite3

class YapilanOdemeGiris(QWidget):
    def __init__(self):
        super().__init__()
        self.YapilanOdemeGirisi = Ui_widget()
        self.YapilanOdemeGirisi.setupUi(self)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT cari FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.con.close()
        self.YapilanOdemeGirisi.cbFirmaAdi.addItems(sorted(firma_listesi))
        self.YapilanOdemeGirisi.deOdemeTarihi.setCalendarPopup(True)
        self.YapilanOdemeGirisi.deOdemeTarihi.setWrapping(True)
        self.YapilanOdemeGirisi.deOdemeTarihi.setDate(QDate.currentDate())
        self.YapilanOdemeGirisi.pushButton.clicked.connect(self.YapilanOdemeKaydet)
        
    def YapilanOdemeKaydet(self):
        #Yapılan ödemeler veritabanı odeme sayfasına durumu 'yo' olarak kayıt edilir.
        durum = "yo"
        day = str(self.YapilanOdemeGirisi.deOdemeTarihi.date().day())
        month = str(self.YapilanOdemeGirisi.deOdemeTarihi.date().month())
        year = str(self.YapilanOdemeGirisi.deOdemeTarihi.date().year())
        if len(day) == 1:
            day = "0" + day
        if len(month) == 1:
            month = "0" + month
        ft = (year,month,day)
        odemeTarihi = "-".join(ft)
        firmaAdi = self.YapilanOdemeGirisi.cbFirmaAdi.currentText()
        aciklama = self.YapilanOdemeGirisi.textEdit.toPlainText()
        tutar = float(self.YapilanOdemeGirisi.leOdemeTutar.text())
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("insert into odeme(odemeTarih,FirmaAdi,Aciklama,tutar,odemeTip) values(?,?,?,?,?)",(odemeTarihi,firmaAdi,aciklama,tutar,durum))
        self.con.commit()
        self.YapilanOdemeGirisi.deOdemeTarihi.setDate(QDate.currentDate())
        self.YapilanOdemeGirisi.cbFirmaAdi.setCurrentIndex(-1)
        self.YapilanOdemeGirisi.textEdit.clear()
        self.YapilanOdemeGirisi.leOdemeTutar.clear()
        self.close()
        