from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate
from kayitDuzenleUi import Ui_kayitDuzenle
from alisFaturasi import AlisFaturasi
from satisFaturasi import SatisFaturasi
from odemeGiris import OdemeGiris
from yapilanOdemeGiris import YapilanOdemeGiris
import sqlite3

class KayitDuzenle(QWidget):
    def __init__(self):
        super().__init__()
        self.kayitDuzenle = Ui_kayitDuzenle()
        self.kayitDuzenle.setupUi(self)
        self.alisFaturasi = AlisFaturasi()
        self.satisFaturasi = SatisFaturasi()
        self.odemeGiris = OdemeGiris()
        self.yapilanOdemeGiris = YapilanOdemeGiris()
        self.kayitDuzenle.twAyrintilar.setColumnWidth(0,40)
        self.kayitDuzenle.twAyrintilar.setColumnWidth(1,100)
        self.kayitDuzenle.twAyrintilar.setColumnWidth(2,80)
        self.kayitDuzenle.twAyrintilar.setColumnWidth(3,80)
        self.kayitDuzenle.twAyrintilar.setColumnWidth(4,240)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT firma_adi FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.kayitDuzenle.cbFirmaAdi.addItems(sorted(firma_listesi))
        self.kayitDuzenle.pbKayitGoster.clicked.connect(self.kayitGoster)
        self.kayitDuzenle.pbDuzenle.clicked.connect(self.duzenle)
        self.kayitDuzenle.pbSil.clicked.connect(self.sil)
        
    def kayitGoster(self):
        firmaAdi = self.kayitDuzenle.cbFirmaAdi.currentText()
        data = list()
        self.cursor.execute("select id,odemeTip,odemeTarih,tutar,Aciklama from odeme where firmaAdi = ?" , (firmaAdi,))
        dataOdeme = self.cursor.fetchall()
        self.cursor.execute("select id,ftTip,ftTarih,ftToplam,ftAciklama from data where ftCariAdi = ?" , (firmaAdi,))
        dataFatura = self.cursor.fetchall()
        for i in dataOdeme:
            data.append(i)
        for k in dataFatura:
            data.append(k)
        items = {"go":"Gelen Ödeme" , "yo" : "Yapılan Ödeme" , "af" : "Alış Faturası" , "sf" : "Satış Faturası"}
        data.sort(key=lambda data:data[1])
        self.kayitDuzenle.twAyrintilar.setRowCount(len(data))
        for i,k in enumerate(data):
            for ii,kk in enumerate(k):
                if kk in items:
                    kk = items[kk]
                    
                if isinstance(kk,float):
                    kk = "{:,}".format(kk)
                    
                self.kayitDuzenle.twAyrintilar.setItem(i,ii,QTableWidgetItem(str(kk)))
        
    def duzenle(self):
        row = self.kayitDuzenle.twAyrintilar.currentRow()
        id = self.kayitDuzenle.twAyrintilar.item(row,0).text()
        islemBicimi = self.kayitDuzenle.twAyrintilar.item(row,1).text()
        
        if islemBicimi == "Satış Faturası":
            self.cursor.execute("select ftTarih,ftNo,ftCariAdi,ftAciklama,ftTutar,ftKdv,ftToplam from data where id = ?" , (id,))
            veri = self.cursor.fetchall()
            self.satisFaturasi.show()
            year = int(veri[0][0][0:4])
            month = int(veri[0][0][5:7])
            day = int(veri[0][0][8:])
            self.satisFaturasi.satisFatura.dateEdit.setDate(QDate(year,month,day))
            self.satisFaturasi.satisFatura.lineEditFaturaNo.setText(veri[0][1])
            self.satisFaturasi.satisFatura.comboBox.setCurrentText(veri[0][2])
            self.satisFaturasi.satisFatura.textEdit.setText(veri[0][3])
            self.satisFaturasi.satisFatura.lineEditFaturaNo_2.setText(str(veri[0][4]))
            self.satisFaturasi.satisFatura.lineEditFaturaNo_3.setText(str(veri[0][5]))
            self.satisFaturasi.satisFatura.lineEditFaturaNo_4.setText(str(veri[0][6]))
            self.cursor.execute("delete from data where id = ?" , (id,))
            self.con.commit()
            
            
        elif islemBicimi == "Alış Faturası":
            self.cursor.execute("select ftTarih,ftNo,ftCariAdi,ftAciklama,ftTutar,ftKdv,ftToplam from data where id = ?" , (id,))
            veri = self.cursor.fetchall()
            self.alisFaturasi.show()
            year = int(veri[0][0][0:4])
            month = int(veri[0][0][5:7])
            day = int(veri[0][0][8:])
            self.alisFaturasi.alisFatura.dateEdit.setDate(QDate(year,month,day))
            self.alisFaturasi.alisFatura.lineEditFaturaNo.setText(veri[0][1])
            self.alisFaturasi.alisFatura.comboBox.setCurrentText(veri[0][2])
            self.alisFaturasi.alisFatura.textEdit.setText(veri[0][3])
            self.alisFaturasi.alisFatura.lineEditFaturaNo_2.setText(str(veri[0][4]))
            self.alisFaturasi.alisFatura.lineEditFaturaNo_3.setText(str(veri[0][5]))
            self.alisFaturasi.alisFatura.lineEditFaturaNo_4.setText(str(veri[0][6]))
            self.cursor.execute("delete from data where id = ?" , (id,))
            self.con.commit()
            
            
        elif islemBicimi == "Gelen Ödeme":
            self.odemeGiris.show()
            self.cursor.execute("select odemeTarih ,FirmaAdi,Aciklama,tutar,odemeTip from odeme where id = ?" , (id,))
            veri = self.cursor.fetchall()
            year = int(veri[0][0][0:4])
            month = int(veri[0][0][5:7])
            day = int(veri[0][0][8:])
            self.odemeGiris.odemeGirisi.deOdemeTarihi.setDate(QDate(year,month,day))
            self.odemeGiris.odemeGirisi.cbFirmaAdi.setCurrentText(veri[0][1])
            self.odemeGiris.odemeGirisi.leOdemeTutar.setText(str(veri[0][3]))
            self.odemeGiris.odemeGirisi.textEdit.setText(veri[0][2])
            self.cursor.execute("delete from odeme where id = ?" , (id,))
            self.con.commit()
            
        else:
            self.yapilanOdemeGiris.show()
            self.cursor.execute("select odemeTarih ,FirmaAdi,Aciklama,tutar,odemeTip from odeme where id = ?" , (id,))
            veri = self.cursor.fetchall()
            year = int(veri[0][0][0:4])
            month = int(veri[0][0][5:7])
            day = int(veri[0][0][8:])
            self.yapilanOdemeGiris.YapilanOdemeGirisi.deOdemeTarihi.setDate(QDate(year,month,day))
            self.yapilanOdemeGiris.YapilanOdemeGirisi.cbFirmaAdi.setCurrentText(veri[0][1])
            self.yapilanOdemeGiris.YapilanOdemeGirisi.leOdemeTutar.setText(str(veri[0][3]))
            self.yapilanOdemeGiris.YapilanOdemeGirisi.textEdit.setText(veri[0][2])
            self.cursor.execute("delete from odeme where id = ?" , (id,))
            self.con.commit()
        
        
        
    def sil(self):
        row = self.kayitDuzenle.twAyrintilar.currentRow()
        msg = QMessageBox()
        msg.setWindowTitle("Onay Penceresi")
        msg.setText("{} numaralı satırdaki seçili kayıt silinecek !".format(row+1))
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msg.buttonClicked.connect(self.messageBoxAction)
        x = msg.exec_()
    def messageBoxAction(self,i):
        buttonPressed = (i.text())
        if buttonPressed == "&Yes":
            row = self.kayitDuzenle.twAyrintilar.currentRow()
            id = self.kayitDuzenle.twAyrintilar.item(row,0).text()
            islemBicimi = self.kayitDuzenle.twAyrintilar.item(row,1).text()
            self.kayitDuzenle.twAyrintilar.removeRow(row)
            
            if islemBicimi in ("Satış Faturası" , "Alış Faturası"):
                self.con = sqlite3.connect("database.db")
                self.cursor = self.con.cursor()
                self.cursor.execute("delete from data where id = ?" , (id,))
                self.con.commit()
                
            else:
                self.con = sqlite3.connect("database.db")
                self.cursor = self.con.cursor()
                self.cursor.execute("delete from odeme where id = ?" , (id,))
                self.con.commit()
        
        