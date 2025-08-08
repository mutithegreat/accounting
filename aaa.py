import sqlite3
import random

con = sqlite3.connect("database.db")
cursor = con.cursor()

cari_list = ["ahmet","mehmet","süleyman"]
tarih_list = ["2025-02-02","2025-04-04" , "2025-06-06","2025-08-08"]
aciklama_list = ["Dalaman","Fethiye","Çanakkale"]
fatura_tip = ["af","sf"]

for i in range(20):
    faturaTarihi = random.choice(tarih_list)
    faturaNumarasi = random.randrange(1,100)
    cariAdi = random.choice(cari_list)
    aciklama = random.choice(aciklama_list)
    tutar = random.randrange(100,1500,100)
    kdv = tutar * 0.2
    toplamTutar = tutar + kdv
    faturaTip = random.choice(fatura_tip)
    cursor.execute("insert into data (tarih ,ft_no,cari,aciklama,tutar,kdv,toplam,ft_tip) values(?,?,?,?,?,?,?,?)",(faturaTarihi,faturaNumarasi,cariAdi,aciklama,tutar,kdv,toplamTutar,faturaTip))
    con.commit()

for cek in range(10):
    cekNumarasi = random.randint(1,100)
    CekTarihi = random.choice(tarih_list)
    firmaAdi = random.choice(cari_list)
    aciklama = random.choice(aciklama_list)
    vadeTarihi = random.choice(tarih_list)
    tutar = random.randrange(100,1500,100)
    durum = "1"
    cursor.execute("insert into cek(cek_no,tarih,cari,aciklama,vade_tarihi,toplam,durum) values(?,?,?,?,?,?,?)",(cekNumarasi,CekTarihi,firmaAdi,aciklama,vadeTarihi,tutar,durum))
    con.commit()
    
for _ in range(20):
    odemeTarihi = random.choice(tarih_list)
    firmaAdi = random.choice(cari_list)
    aciklama = random.choice(aciklama_list)
    tutar = random.randrange(100,1500,100)
    durum = random.choice(["go","yo"])
    
    cursor.execute("insert into odeme(odeme_tarihi,cari,aciklama,toplam,odeme_tip) values(?,?,?,?,?)",(odemeTarihi,firmaAdi,aciklama,tutar,durum))
    con.commit()
for ind , cari in enumerate(cari_list):
    adres = random.choice(aciklama_list)
    vergi_dairesi = random.choice(aciklama_list)
    vergi_no = random.randrange(1,100)
    telefon = random.randrange(1,100)
    mail_adresi = random.randrange(1,100)
    cursor.execute("Insert into cari_kart(cari , adres ,vergi_dairesi , vergi_no , telefon , mail_adresi) values(?,?,?,?,?,?)",(cari,adres,vergi_dairesi,vergi_no,telefon,mail_adresi))
    con.commit()
con.close()
