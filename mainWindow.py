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
        
        self.mainPageform.twCekListesi.setColumnWidth(0,210)
        self.mainPageform.twCekListesi.setColumnWidth(1,80)
        self.mainPageform.twCekListesi.setColumnWidth(2,80)
        self.mainPageform.twCekListesi.setColumnWidth(3,90)
        self.mainPageform.twCekListesi.setColumnWidth(4,90)
        self.mainPageform.twOdemeListesi.setColumnWidth(0,290)
        self.mainPageform.twOdemeListesi.setColumnWidth(1,130)
        self.mainPageform.twGelecekOdeme.setColumnWidth(0,290)
        self.mainPageform.twGelecekOdeme.setColumnWidth(1,130)
        
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
        self.alisFaturasıEkran.data_updated.connect(self.guncelle)
        self.satisFatuasıEkran.data_updated.connect(self.guncelle)
        self.cekGirisEkran.data_updated.connect(self.guncelle)
        self.odemeler_ekrani()
        self.cek_ekrani()
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
        
    def veri_al(self):
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("""WITH fatura AS(
                                SELECT
                                    cari,
                                SUM(
                                    CASE WHEN ft_tip = "af" THEN toplam ELSE 0 END
                                ) AS Alis_fatura,
                                SUM(
                                    CASE WHEN ft_tip = "sf" THEN toplam ELSE 0 END
                                ) AS Satis_fatura
                                FROM
                                    data 
                                GROUP BY cari
                                )
                                ,
                                borc AS(
                                SELECT
                                    cari,
                                SUM(
                                    CASE WHEN odeme_tip = "yo" THEN toplam ELSE 0 END
                                ) AS Yapilan_odeme,
                                SUM(
                                    CASE WHEN odeme_tip = "go" THEN toplam ELSE 0 END
                                ) AS Gelen_odeme
                                FROM
                                    odeme 
                                GROUP BY cari
                                )

                            SELECT 
                                fatura.cari,
                                fatura.Alis_fatura+borc.Gelen_odeme AS total_borc,
                                fatura.Satis_fatura+borc.Yapilan_odeme AS total_alacak 
                            FROM 
                                fatura 
                            JOIN 
                                borc 
                            ON
                                borc.cari = fatura.cari""")
        
        data = self.cursor.fetchall()
        self.con.close()
        yapilacak_odemeler = dict()
        gelecek_odemeler = dict()
        for cari in data:
            if cari[1] > cari[2]:
                yapilacak_odemeler[cari[0]] = cari[1] - cari[2]
            else:
                gelecek_odemeler[cari[0]] = cari[2] - cari[1]
        return yapilacak_odemeler , gelecek_odemeler
    
    def odemeler_ekrani(self):
        y , g = self.veri_al()
        self.mainPageform.twOdemeListesi.setRowCount(len(y))
        
        for col , (key , value) in enumerate(y.items()):
            if isinstance(value,float):
                value = "%.2f"  % value
            self.mainPageform.twOdemeListesi.setItem(col,0,QTableWidgetItem(key))
            self.mainPageform.twOdemeListesi.setItem(col,1,QTableWidgetItem(value))
    
        self.mainPageform.twGelecekOdeme.setRowCount(len(g))
        
        for col , (key , value) in enumerate(g.items()):
            if isinstance(value,float):
                value = "%.2f"  % value
            self.mainPageform.twGelecekOdeme.setItem(col,0,QTableWidgetItem(key))
            self.mainPageform.twGelecekOdeme.setItem(col,1,QTableWidgetItem(value))
        #yapilacak_odemeler , gelecek_odemeler = 0 , 0    
    def cek_ekrani(self):
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT cari,cek_no,tarih,vade_tarihi,toplam FROM cek where durum = 1")
        veri = self.cursor.fetchall()
                
        #Çek ekranı verileri
        self.mainPageform.twCekListesi.setRowCount(len(veri))
        for row , cek in enumerate(veri):
            for col, _ in enumerate(cek):
                if isinstance(_ , float):
                    _ = "{:,}".format(_)
                self.mainPageform.twCekListesi.setItem(row,col,QTableWidgetItem(str(_)))
        self.con.close()

    
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
    def guncelle(self):
        self.odemeler_ekrani()
        self.cek_ekrani()
        
        
        