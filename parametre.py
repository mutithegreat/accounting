import sqlite3

def parametre_cari():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("select cari from cari_kart")
    data = cursor.fetchall()
    firma_listesi = [i[0] for i in data]
    return firma_listesi





