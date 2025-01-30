import sqlite3


"""con = sqlite3.connect("database.db")
cursor = con.cursor()
firmaAdi = "Ayer Peyzaj"
cursor.execute("select ftTip,ftTarih,ftAciklama,ftToplam from data where ftCariAdi = ?" , (firmaAdi,))
data = cursor.fetchall()
data = list(data)
items = {"go":"Gelen Ödeme" , "yo" : "Yapılan Ödeme" , "af" : "Alış Faturası" , "sf" : "Satış Faturası"}

for i in data:
    for j in i:
        if isinstance(j,float):
            print(j)


cursor.execute("select * from data")
data_fatura = cursor.fetchall()
cursor.execute("select odemeTarih,FirmaAdi,tutar,odemeTip from odeme")
data_odeme = cursor.fetchall()
cursor.execute("select cekTarihi,FirmaAdi,cekNo,tutar,durum from cek")
data_cek = cursor.fetchall()
con.close()
data = data_fatura+data_odeme+data_cek
data.sort()







baslangicTarihi = "2023-03-18"
bitisTArihi = "2023-08-24"
firmaAdi = data[0][2]

elenmisVeri = list()
baslik = f"{firmaAdi} Cari Hesap Ekstresi"


for i in data:
    if baslangicTarihi < i[0] < bitisTArihi :
        if "af" in i:
            elenmisVeri.append([i[0],"Alış Faturası",i[1],i[6],""])
        elif "sf" in i:
            elenmisVeri.append([i[0],"Satış Faturası",i[1],"",i[6]])
        elif "yo" in i:
            elenmisVeri.append([i[0],"Yapılan Ödeme","","",i[2]])
        elif "go" in i:
            elenmisVeri.append([i[0],"Gelen Ödeme","",i[2],""])
        elif i[4] == "0":
            elenmisVeri.append([i[0],"Çek Ödemesi",i[2],"",i[3]])

toplamBorc , toplamAlacak = 0 , 0

for tutar in elenmisVeri:
    if tutar[4] != "":
        toplamAlacak += tutar[4]
    if tutar[3] != "":
        toplamBorc += tutar[3]
print(toplamBorc,toplamAlacak)



wb = xlsxwriter.Workbook(f"../{firmaAdi}{bitisTArihi}.xlsx")
wb_data = wb.add_worksheet(firmaAdi)
wb_data.set_row(0,25)
wb_data.set_row(1,18)
wb_data.set_column("A:B",15)
wb_data.set_column("B:E",15)
data_format = wb.add_format(
    {
        "border" : 1,
        "border_color" : "black"
    }
)
title_format = wb.add_format(
    {
        "bg_color" : "#D9D9D9",
        "bold" : True,
        "font_size" : 16,
        "font_color" : "#7D3005"

    }

)
header_format = wb.add_format(
    {
        "bold" : True,
        "font_color" : "#0808F8",
        "font_size" : 13,
        "num_format" : "₺#.##0;-₺#.##0"
    }
)
money_format = wb.add_format(
    {
        "num_format" : "₺#.##0;-₺#.##0"
    }
)
wb_data.merge_range("A1:E1",baslik,title_format)
wb_data.write("A2" , "Tarih" , header_format)
wb_data.write("B2" , "İşlem Türü" , header_format)
wb_data.write("C2" , "Belgo No" , header_format)
wb_data.write("D2" , "Borç" , header_format)
wb_data.write("E2" , "Alacak" , header_format)

for indeks,veri in enumerate(elenmisVeri):
    wb_data.write(indeks+3,0,veri[0])
    wb_data.write(indeks+3,1,veri[1])
    wb_data.write(indeks+3,2,veri[2])
    wb_data.write(indeks+3,3,veri[3],money_format)
    wb_data.write(indeks+3,4,veri[4],money_format)


#for indeks , satir in enumerate(elenmisVeri):
 #   for tekrar in range(len(satir)):
  #      wb_data.write(indeks+2,tekrar,satir[tekrar],data_format)


toplamBorc , toplamAlacak = 0 , 0

for tutar in elenmisVeri:
    if tutar[4] != "":
        toplamAlacak += tutar[4]
    if tutar[3] != "":
        toplamBorc += tutar[3]



last_index = len(elenmisVeri)+3
last_index_cell_borc = "D"+str(last_index)
last_index_cell_alacak = "E"+str(last_index)
toplam_borc , toplam_alacak = 0 , 0
wb_data.write(last_index+4,2,"Toplam",header_format)
if toplamBorc > toplamAlacak:
    wb_data.write(last_index+4,3,f"=SUM(D3:{last_index_cell_borc})",header_format)
elif toplamBorc < toplamAlacak:
    wb_data.write(last_index+4,4,f"=SUM(E3:{last_index_cell_alacak})",header_format)



wb.close()
"""