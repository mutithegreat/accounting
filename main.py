import sys
from PyQt5.QtWidgets import QApplication
from loginPage import Login
import sqlite3

con = sqlite3.connect("database.db")
cursor = con.cursor()
cursor.execute("create table if not exists login(kullanici_adi text,kullanici_sifre text)")
cursor.execute("create table if not exists cari_kart(id INTEGER,cari text,adres text,vergi_dairesi text,vergi_no int,telefon text,mail_adresi text,PRIMARY KEY(id AUTOINCREMENT))")
cursor.execute("create table if not exists data(id INTEGER,tarih text,ft_no text,cari text,aciklama text,tutar float,kdv float,toplam float,ft_tip text,PRIMARY KEY(id AUTOINCREMENT))")
cursor.execute("create table if not exists cek(id INTEGER,cek_no text,tarih text,cari text,aciklama text,vade_tarihi text, toplam float,durum text,PRIMARY KEY(id AUTOINCREMENT))")
cursor.execute("create table if not exists odeme(id INTEGER,odeme_tarihi text,cari text,aciklama text,toplam float,odeme_tip text,PRIMARY KEY(id AUTOINCREMENT))")
con.close()



app = QApplication(sys.argv)
pencere = Login()
pencere.show()

app.exec_()



