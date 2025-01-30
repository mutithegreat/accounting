import sqlite3

def parametre_cari():
    con = sqlite3.connect("database.db")
    cursor = con.cursor()
    cursor.execute("select firma_adi from cari_kart")
    data = cursor.fetchall()
    return data


