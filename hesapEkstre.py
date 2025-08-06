from PyQt5.QtWidgets import *
from hesapEkstreUi import Ui_Form
from PyQt5.QtCore import QDate
import xlsxwriter
import sqlite3



class HesapEkstre(QWidget):
    def __init__(self):
        super().__init__()
        self.hesapEkstresi = Ui_Form()
        self.hesapEkstresi.setupUi(self)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT cari FROM cari_kart")
        firmalar = self.cursor.fetchall()
        self.con.close()
        firma_listesi = [" "]
        for i in firmalar:
            firma_listesi.append(i[0])
        self.hesapEkstresi.dateEdit.setCalendarPopup(True)
        self.hesapEkstresi.dateEdit.setWrapping(True)
        self.hesapEkstresi.dateEdit.setDate(QDate.currentDate())
        self.hesapEkstresi.dateEdit_2.setCalendarPopup(True)
        self.hesapEkstresi.dateEdit_2.setWrapping(True)
        self.hesapEkstresi.dateEdit_2.setDate(QDate.currentDate())
        self.hesapEkstresi.comboBox.addItems(sorted(firma_listesi))
        self.hesapEkstresi.pushButton.clicked.connect(self.exceleAktar)
        

    def exceleAktar(self):
        day1 = str(self.hesapEkstresi.dateEdit.date().day())
        month1 = str(self.hesapEkstresi.dateEdit.date().month())
        year1 = str(self.hesapEkstresi.dateEdit.date().year())
        
        if len(day1) == 1:
            day1 = "0" + day1
        if len(month1) == 1:
            month1 = "0" + month1
        bast = (year1,month1,day1)
        baslangicTarihi = "-".join(bast)

        day2 = str(self.hesapEkstresi.dateEdit_2.date().day())
        month2 = str(self.hesapEkstresi.dateEdit_2.date().month())
        year2 = str(self.hesapEkstresi.dateEdit_2.date().year())
        if len(month2) == 1:
            month2 = "0"+ month2
        if len(day2) == 1:
            day2 = "0" + day2
        bitt = (year2,month2,day2)
        bitisTarihi = "-".join(bitt)
        firmaAdi = self.hesapEkstresi.comboBox.currentText()
        con = sqlite3.connect("database.db")
        cursor = con.cursor()
        cursor.execute("select ftTarih ,ftNo ,ftCariAdi,ftAciklama,ftTutar,ftKdv,ftToplam,ftTip from data where ftCariAdi = ?",(firmaAdi,))
        data_fatura = cursor.fetchall()
        cursor.execute("select odemeTarih,FirmaAdi,tutar,odemeTip from odeme where FirmaAdi = ?" , (firmaAdi,))
        data_odeme = cursor.fetchall()
        cursor.execute("select cekTarihi,FirmaAdi,cekNo,tutar,durum from cek where FirmaAdi = ?" , (firmaAdi,))
        data_cek = cursor.fetchall()
        con.close()
        data = data_fatura+data_odeme+data_cek
        data.sort()
        elenmisVeri = list()
        baslik = f"{firmaAdi} Cari Hesap Ekstresi ({baslangicTarihi} - {bitisTarihi})"
        for i in data:
            if baslangicTarihi <= i[0] <= bitisTarihi :
                if "af" in i:
                    elenmisVeri.append([i[0],"Alış Faturası",i[1],i[6],""])
                elif "sf" in i:
                    elenmisVeri.append([i[0],"Satış Faturası",i[1],"",i[6]])
                elif "yo" in i:
                    elenmisVeri.append([i[0],"Yapılan Ödeme","","",i[2]])
                elif "go" in i:
                    elenmisVeri.append([i[0],"Gelen Ödeme","",i[2],""])
                elif i[4] == "1":
                    elenmisVeri.append([i[0],"Çek Ödemesi",i[2],"",i[3]])
        
        dosyaAdi = f"{firmaAdi}{bitisTarihi}.xlsx"
        wb = xlsxwriter.Workbook("../"+dosyaAdi)
        wb_data = wb.add_worksheet(firmaAdi)
        wb_data.set_row(0,25)
        wb_data.set_row(1,18)
        wb_data.set_column("A:B",15)
        wb_data.set_column("B:E",15)
        
        money_format = wb.add_format(
            {
                "num_format" : "₺#.##0;-₺#.##0"
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
                "num_format" : "₺#.##0;-₺#.##0",
                "bottom" : 6,
                "bottom_color" : "red"
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
        last_index = len(elenmisVeri)+3
        last_index_cell_borc = "D"+str(last_index)
        last_index_cell_alacak = "E"+str(last_index)
        toplamBorc , toplamAlacak = 0 , 0

        for tutar in elenmisVeri:
            if tutar[4] != "":
                toplamAlacak += tutar[4]
            if tutar[3] != "":
                toplamBorc += tutar[3]
        wb_data.write(last_index+4,3,f"=SUM(D4:{last_index_cell_borc})",header_format)
        wb_data.write(last_index+4,2,"Toplam",header_format)
        wb_data.write(last_index+4,4,f"=SUM(E4:{last_index_cell_alacak})",header_format)
        if toplamBorc > toplamAlacak:
            wb_data.write(last_index+6,2,"Toplam Borç",header_format)
            wb_data.write(last_index+6,3,toplamBorc - toplamAlacak,header_format)
        elif toplamBorc < toplamAlacak:
            wb_data.write(last_index+6,2,"Toplam Alacak",header_format)
            wb_data.write(last_index+6,4,toplamAlacak - toplamBorc,header_format)

        wb.close()
        self.hesapEkstresi.comboBox.setCurrentIndex(-1)
        self.hesapEkstresi.dateEdit.setDate(QDate.currentDate())
        self.hesapEkstresi.dateEdit_2.setDate(QDate.currentDate())
        self.close()
        