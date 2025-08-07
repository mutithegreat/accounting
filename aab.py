# from passlib.hash import sha256_crypt

# sifre = "a"
# sifreli_metin = sha256_crypt.hash(sifre)
# print(sifreli_metin)
import sqlite3
con = sqlite3.connect("database.db")
cursor = con.cursor()
cursor.execute("select cari from cari_kart")
data = cursor.fetchall()
data = [i[0] for i in data]
print(data)