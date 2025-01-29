from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from cekGirisUi import Ui_widget
import sqlite3

class CekGiris(QWidget):
    def __init__(self):
        super().__init__()
        self.cekGirisi = Ui_widget()
        self.cekGirisi.setupUi(self)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT firma_adi FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.con.close()
        self.cekGirisi.cbFirmaAdi.addItems(sorted(firma_listesi))
        self.cekGirisi.deCekTarihi.setCalendarPopup(True)
        self.cekGirisi.deCekTarihi.setWrapping(True)
        self.cekGirisi.deCekTarihi.setDate(QDate.currentDate())
        self.cekGirisi.deCekVadesi.setCalendarPopup(True)
        self.cekGirisi.deCekVadesi.setWrapping(True)
        self.cekGirisi.deCekVadesi.setDate(QDate.currentDate())
        self.cekGirisi.pushButton.clicked.connect(self.kaydet)
    def kaydet(self):
        dayCek = str(self.cekGirisi.deCekTarihi.date().day())
        monthCek = str(self.cekGirisi.deCekTarihi.date().month())
        yearCek = str(self.cekGirisi.deCekTarihi.date().year())
        durum = "1"
        if len(dayCek) == 1:
            dayCek = "0" + dayCek
        if len(monthCek) == 1:
            monthCek = "0" + monthCek
        ct = (yearCek,monthCek,dayCek)
        CekTarihi = "-".join(ct)

        day = str(self.cekGirisi.deCekTarihi.date().day())
        month = str(self.cekGirisi.deCekTarihi.date().month())
        year = str(self.cekGirisi.deCekTarihi.date().year())
        if len(month) == 1:
            month = "0"+ month
        if len(day) == 1:
            day = "0" + day
        vt = (year,month,day)
        vadeTarihi = "-".join(vt)
        firmaAdi = self.cekGirisi.cbFirmaAdi.currentText()
        aciklama = self.cekGirisi.textEdit.toPlainText()
        cekNumarasi = self.cekGirisi.lineEdit_2.text()
        tutar = float(self.cekGirisi.lineEdit.text().replace(",","."))
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("insert into cek(cekNo,cekTarihi,FirmaAdi,Aciklama,vadeTarihi,tutar,durum) values(?,?,?,?,?,?,?)",(cekNumarasi,CekTarihi,firmaAdi,aciklama,vadeTarihi,tutar,durum))
        self.con.commit()
        self.con.close()
        self.cekGirisi.cbFirmaAdi.setCurrentIndex(-1)
        self.cekGirisi.deCekTarihi.setDate(QDate.currentDate())
        self.cekGirisi.deCekVadesi.setDate(QDate.currentDate())
        self.cekGirisi.lineEdit.clear()
        self.cekGirisi.textEdit.clear()
        self.cekGirisi.lineEdit_2.clear()
        self.close()
        


        
        