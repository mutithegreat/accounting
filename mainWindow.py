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
        """
        #Yaklaşan Gelecek Ödemeler Bilgi Ekranı
        self.cursor.execute('select ftCariAdi, sum(ftToplam) from data where ftTip = "sf" group by ftCariAdi')
        satisFatura  = self.cursor.fetchall()
        #Borclu Cariden Gelen Faturalar
        self.cursor.execute('select ftCariAdi, sum(ftToplam) from data where ftTip = "af" group by ftCariAdi')
        alisFatura = self.cursor.fetchall()
        #Borçlu Cari Gelen Ödemeler
        self.cursor.execute('select FirmaAdi,sum(tutar) from odeme where odemeTip = "go"group by FirmaAdi')
        gelenOdeme = self.cursor.fetchall()
        #Borçlu Yapılan Ödemeler
        self.cursor.execute('select FirmaAdi,sum(tutar) from odeme where odemeTip = "yo"group by FirmaAdi')
        yapilanOdeme =  self.cursor.fetchall()
        #Firma Listesi
        self.cursor.execute("select firma_adi from cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = list()
        for i in firmalar:
            firma_listesi.append(i[0])
        cariDurum = [ 0 for i in range(len(firma_listesi))]
        firma_listesi_alacak = dict(map(lambda i,j : (i,j) , firma_listesi,cariDurum))
        firma_listesi_borc = dict(map(lambda i,j : (i,j) , firma_listesi,cariDurum))       
        #Gelecek Ödemeler Verileri
        satisFatura =dict(satisFatura)
        alisFatura = dict(alisFatura)
        gelenOdeme = dict(gelenOdeme)
        yapilanOdeme = dict(yapilanOdeme)

        for borcluCari in firma_listesi_alacak:
            if borcluCari in alisFatura:
                firma_listesi_alacak[borcluCari] -= alisFatura[borcluCari]
            if borcluCari in satisFatura:
                firma_listesi_alacak[borcluCari] += satisFatura[borcluCari]
            if borcluCari in gelenOdeme:
                firma_listesi_alacak[borcluCari] -= gelenOdeme[borcluCari]
            if borcluCari in yapilanOdeme:
                firma_listesi_alacak[borcluCari] += yapilanOdeme[borcluCari]
        
        gelecekOdemeVeriListesi = list()
        for cari , tutar in firma_listesi_alacak.items():
            if tutar > 0 :
                gelecekOdemeVeriListesi.append([cari,tutar])
        
        self.mainPageform.twGelecekOdeme.setRowCount(len(gelecekOdemeVeriListesi))
        
        for iia,kka in enumerate(gelecekOdemeVeriListesi):
            for jja,tta in enumerate(kka):
                if isinstance(tta,float):
                    tta = "%.2f" % tta
                self.mainPageform.twGelecekOdeme.setItem(iia,jja,QTableWidgetItem(str(tta)))
        
        #Yapılacak Ödemeler Verileri
        
        for alacakliCari in firma_listesi_borc:
            if alacakliCari in satisFatura:
                firma_listesi_borc[alacakliCari] -= satisFatura[alacakliCari]
            if alacakliCari in alisFatura:
                firma_listesi_borc[alacakliCari] += alisFatura[alacakliCari]
            if alacakliCari in gelenOdeme:
                firma_listesi_borc[alacakliCari] += gelenOdeme[alacakliCari]
            if alacakliCari in yapilanOdeme:
                firma_listesi_borc[alacakliCari] -= yapilanOdeme[alacakliCari]
        yapilacakOdemeVeriListesi = list()
        
        for cari2 , tutar2 in firma_listesi_borc.items():
            if tutar2 > 0:
                yapilacakOdemeVeriListesi.append([cari2 , tutar2])
        self.mainPageform.twOdemeListesi.setRowCount(len(yapilacakOdemeVeriListesi))
        
        for ia,ka in enumerate(yapilacakOdemeVeriListesi):
            for ja,ta in enumerate(ka):
                if isinstance(ta,float):
                    ta = "%.2f" % ta
                
                self.mainPageform.twOdemeListesi.setItem(ia,ja,QTableWidgetItem(str(ta)))
        
        #Verilen Cekler Ekranı Bilgileri
        self.cursor.execute("SELECT FirmaAdi,cekNo,cekTarihi,vadeTarihi,tutar FROM cek where durum = 1")
        veri = self.cursor.fetchall()
        #Yapılan çek ödemeler listesini oluştur
        self.cursor.execute('select FirmaAdi,sum(tutar) from cek where durum = "0"group by FirmaAdi')
        yapilanCekOdemesiVeri = self.cursor.fetchall()
        self.con.close()
        #Çek ekranı verileri
        self.mainPageform.twCekListesi.setRowCount(len(veri))
        for i,k in enumerate(veri):
            for j,t in enumerate(k):
                if isinstance(t,float):
                    t = "{:,}".format(t)
                self.mainPageform.twCekListesi.setItem(i,j,QTableWidgetItem(str(t)))
        
        self.mainPageform.pbCariListesi.clicked.connect(self.cariPencere)
        self.mainPageform.pbCariListesi_2.clicked.connect(self.firmalar)
        self.mainPageform.pbFaturaGiris.clicked.connect(self.faturaEkrani)
        self.mainPageform.pbOdemeGiris.clicked.connect(self.satisEkrani)
        self.mainPageform.pbCekKayit.clicked.connect(self.cekEkrani)
        self.mainPageform.pbGelenOdeme.clicked.connect(self.odemeEkrani)
        self.mainPageform.pushButton.clicked.connect(self.cekSil)
        self.mainPageform.pbYapilanOdeme.clicked.connect(self.YapilanOdemeEkrani)
        self.mainPageform.pbHesapEkstre.clicked.connect(self.HesapEkstreEkrani)
        self.mainPageform.pbKayitDuzenle.clicked.connect(self.kayitDuzenle)"""
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
            self.cursor.execute("update cek set durum = ? where cekNo = ?",("0",cekNumarasi))
            self.con.commit()
            self.con.close()
    def update_data(self):
        self.mainPageform.twCekListesi.update()
        self.mainPageform.twGelecekOdeme.update()
        self.mainPageform.twOdemeListesi.update()
            
        
          
            
            
