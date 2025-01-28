import sys
from PyQt5.QtWidgets import QApplication
from loginPage import Login
import sqlite3

con = sqlite3.connect("database.db")
cursor = con.cursor()
cursor.execute("create table if not exists login(kullanici_adi text,kullanici_sifre text)")
cursor.execute("create table if not exists cari_kart(firma_adi text,firma_adresi text,vergi_dairesi text,vergi_no int,telefon text,mail_adresi text)")
cursor.execute("create table if not exists data(id INTEGER,ftTarih text,ftNo text,ftCariAdi text,ftAciklama text,ftTutar float,ftKdv float,ftToplam float,ftTip text,PRIMARY KEY(id AUTOINCREMENT))")
cursor.execute("create table if not exists cek(id INTEGER,cekNo text,cekTarihi text,FirmaAdi text,Aciklama text,vadeTarihi text,tutar float,durum text,PRIMARY KEY(id AUTOINCREMENT))")
cursor.execute("create table if not exists odeme(id INTEGER,odemeTarih text,FirmaAdi text,Aciklama text,tutar float,odemeTip text,PRIMARY KEY(id AUTOINCREMENT))")
con.close()



app = QApplication(sys.argv)
pencere = Login()
pencere.show()

app.exec_()



