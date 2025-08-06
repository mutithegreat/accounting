from PyQt5.QtWidgets import *
from PyQt5.QtCore import QDate,pyqtSignal,QObject
from cariListesi import CariListesi
from firmalistesi import FirmaListesi
from alisFaturasi import AlisFaturasi
from satisFaturasi import SatisFaturasi
from mainWindowUi import Ui_MainWindow
from odemeGiris import OdemeGiris
from yapilanOdemeGiris import YapilanOdemeGiris
from cekGiris import CekGiris
from hesapEkstre import HesapEkstre
from kayitDuzenle import KayitDuzenle
import sqlite3

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()
        self.mainPageform = Ui_MainWindow()
        self.mainPageform.setupUi(self)
        self.carliListesiEkran = CariListesi()
        self.firmaListesiEkran = FirmaListesi()
        self.alisFaturasıEkran = AlisFaturasi()
        self.satisFatuasıEkran = SatisFaturasi()
        self.cekGirisEkran = CekGiris()
        self.odemeGirisEkran = OdemeGiris()
        self.yapilanOdemeGirisEkran = YapilanOdemeGiris()
        self.hesapEkstreEkran = HesapEkstre()
        self.kayitDuzenleEkran = KayitDuzenle()
        self.alisFaturasıEkran.data_updated.connect(self.update_data)
        
        self.mainPageform.twCekListesi.setColumnWidth(0,210)
        self.mainPageform.twCekListesi.setColumnWidth(1,80)
        self.mainPageform.twCekListesi.setColumnWidth(2,80)
        self.mainPageform.twCekListesi.setColumnWidth(3,90)
        self.mainPageform.twCekListesi.setColumnWidth(4,90)
        self.mainPageform.twOdemeListesi.setColumnWidth(0,290)
        self.mainPageform.twOdemeListesi.setColumnWidth(1,130)
        self.mainPageform.twGelecekOdeme.setColumnWidth(0,290)
        self.mainPageform.twGelecekOdeme.setColumnWidth(1,130)
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("""WITH main_table AS(
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
        
        data = self.cursor.fetchall()
        yapilacak_odemeler = dict()
        gelecek_odemeler = dict()
        for cari in data:
            if cari[1]:
                yapilacak_odemeler[cari[0]] = cari[1]
            else:
                gelecek_odemeler[cari[0]] = cari[2]
        
        self.mainPageform.twOdemeListesi.setRowCount(len(yapilacak_odemeler))
        
        for col , (key , value) in enumerate(yapilacak_odemeler.items()):
            if isinstance(value,float):
                value = "%.2f"  % value
            self.mainPageform.twOdemeListesi.setItem(col,0,QTableWidgetItem(key))
            self.mainPageform.twOdemeListesi.setItem(col,1,QTableWidgetItem(value))
    
        self.mainPageform.twGelecekOdeme.setRowCount(len(gelecek_odemeler))
        
        for col , (key , value) in enumerate(gelecek_odemeler.items()):
            if isinstance(value,float):
                value = "%.2f"  % value
            self.mainPageform.twGelecekOdeme.setItem(col,0,QTableWidgetItem(key))
            self.mainPageform.twGelecekOdeme.setItem(col,1,QTableWidgetItem(value))

        self.cursor.execute("SELECT cari,cek_no,tarih,vade_tarihi,toplam FROM cek where durum = 1")
        veri = self.cursor.fetchall()
        #Yapılan çek ödemeler listesini oluştur
        self.cursor.execute('select cari,sum(toplam) from cek where durum = "0"group by cari')
        yapilanCekOdemesiVeri = self.cursor.fetchall()
        self.con.close()
        #Çek ekranı verileri
        self.mainPageform.twCekListesi.setRowCount(len(veri))
        for row , cek in enumerate(veri):
            for col, _ in enumerate(cek):
                if isinstance(_ , float):
                    _ = "{:,}".format(_)
                self.mainPageform.twCekListesi.setItem(row,col,QTableWidgetItem(str(_)))
        
        self.mainPageform.pbCariListesi.clicked.connect(self.cariPencere)
        self.mainPageform.pbCariListesi_2.clicked.connect(self.firmalar)
        self.mainPageform.pbFaturaGiris.clicked.connect(self.faturaEkrani)
        self.mainPageform.pbOdemeGiris.clicked.connect(self.satisEkrani)
        self.mainPageform.pbCekKayit.clicked.connect(self.cekEkrani)
        self.mainPageform.pbGelenOdeme.clicked.connect(self.odemeEkrani)
        self.mainPageform.pushButton.clicked.connect(self.cekSil)
        self.mainPageform.pbYapilanOdeme.clicked.connect(self.YapilanOdemeEkrani)
        self.mainPageform.pbHesapEkstre.clicked.connect(self.HesapEkstreEkrani)
        self.mainPageform.pbKayitDuzenle.clicked.connect(self.kayitDuzenle)
    def cariPencere(self):
        self.carliListesiEkran.show()
    def firmalar(self):
        self.firmaListesiEkran.show()
    def faturaEkrani(self):
        self.alisFaturasıEkran.show()
    def satisEkrani(self):
        self.satisFatuasıEkran.show()
    def cekEkrani(self):
        self.cekGirisEkran.show()
    def odemeEkrani(self):
        self.odemeGirisEkran.show()
    def YapilanOdemeEkrani(self):
        self.yapilanOdemeGirisEkran.show()
    def HesapEkstreEkrani(self):
        self.hesapEkstreEkran.show()
    def kayitDuzenle(self):
        self.kayitDuzenleEkran.show()
    def cekSil(self):
        row = self.mainPageform.twCekListesi.currentRow()
        cekNumarasi = self.mainPageform.twCekListesi.item(row,1).text()
        msg = QMessageBox()
        msg.setWindowTitle("Onay Penceresi")
        msg.setText("{} numaralı çek ödendi olarak düzenlenecek !".format(cekNumarasi))
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msg.buttonClicked.connect(self.messageBoxAction)
        x = msg.exec_()
    def messageBoxAction(self,i):
        buttonPressed = (i.text())
        if buttonPressed == "&Yes":
            row = self.mainPageform.twCekListesi.currentRow()
            cekNumarasi = self.mainPageform.twCekListesi.item(row,1).text()
            self.mainPageform.twCekListesi.removeRow(row)
            self.con = sqlite3.connect("database.db")
            self.cursor = self.con.cursor()
            self.cursor.execute("update cek set durum = ? where cek_no = ?",("0",cekNumarasi))
            self.con.commit()
            self.con.close()
    def update_data(self):
        self.mainPageform.twCekListesi.update()
        self.mainPageform.twGelecekOdeme.update()
        self.mainPageform.twOdemeListesi.update()
            
        
          
            
            
