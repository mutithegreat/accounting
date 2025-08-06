# from passlib.hash import sha256_crypt

# sifre = "a"
# sifreli_metin = sha256_crypt.hash(sifre)
# print(sifreli_metin)
import sqlite3
con = sqlite3.connect("database.db")
cursor = con.cursor()
cursor.execute("""WITH main_table AS(
                            SELECT
                                d.cari,
                            SUM(
                                CASE WHEN d.ft_tip = "af" AND o.odeme_tip = "go" THEN d.toplam+o.toplam ELSE 0 END
                            ) AS Yapılacak_Odeme,
                            SUM(
                                CASE WHEN d.ft_tip = "sf" AND o.odeme_tip = "yo" THEN o.toplam+d.toplam ELSE 0 END
                            ) AS Gelecek_Odeme
                            FROM
                            data AS d
                            JOIN 
                                odeme AS o
                            ON d.cari = o.cari
                            GROUP BY d.cari
                            ) 
                            SELECT
                                cari, 
                                SUM(
                                CASE WHEN Yapılacak_Odeme > Gelecek_Odeme THEN Yapılacak_Odeme - Gelecek_Odeme ELSE 0 END
                            ) AS Yapılacak_Odeme,
                            SUM(
                                CASE WHEN Yapılacak_Odeme < Gelecek_Odeme THEN Gelecek_Odeme - Yapılacak_Odeme ELSE 0 END
                            ) AS Gelecek_Odeme
                                    
                            FROM 
                                main_table
                            GROUP BY cari""")
data = cursor.fetchall()
yapilacak_odemeler = dict()
gelecek_odemeler = dict()
print(data)
for cari in data:
    if cari[1]:
        yapilacak_odemeler[cari[0]] = cari[1]
    else:
        gelecek_odemeler[cari[0]] = cari[2]


for j , (i , k) in enumerate(yapilacak_odemeler.items()):
    print(j,0,i)
    print(j,1,k)
        
        
