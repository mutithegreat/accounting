from PyQt5.QtWidgets import *
from firmaListesiUi import Ui_Form
from cariListesi import CariListesi
import sqlite3

class FirmaListesi(QWidget):
    def __init__(self):
        super().__init__()
        self.firmaListesi = Ui_Form()
        self.firmaListesi.setupUi(self)
        self.cariListesi = CariListesi()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("SELECT cari FROM cari_kart")
        firmalar = self.cursor.fetchall()
        firma_listesi = list()
        for i in firmalar:
            firma_listesi.append(i[0])
        self.firmaListesi.listWidget.addItems(firma_listesi)
        self.firmaListesi.pbFirmaDuzenle.clicked.connect(self.firma_duzenle)
        self.firmaListesi.pbFirmaSil.clicked.connect(self.firma_sil)

    def firma_sil(self):
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        firmaAdi = self.firmaListesi.listWidget.currentItem().text()
        msg = QMessageBox()
        msg.setWindowTitle("Onay Penceresi")
        msg.setText("{} firması sistemden kalıcı olarak silinecek !".format(firmaAdi))
        msg.setStandardButtons(QMessageBox.Cancel | QMessageBox.Yes)
        msg.buttonClicked.connect(self.messageBoxAction)
        x = msg.exec_()
    def messageBoxAction(self,i):
        buttonPressed = (i.text())
        if buttonPressed == "&Yes":
            firmaAdi = self.firmaListesi.listWidget.currentItem().text()
            self.cursor.execute("delete from cari_kart where cari = ?" , (firmaAdi,))
            self.con.commit()
            self.firmaListesi.listWidget.clear()
            self.con = sqlite3.connect("database.db")
            self.cursor = self.con.cursor()
            self.cursor.execute("SELECT cari FROM cari_kart")
            firmalar = self.cursor.fetchall()
            firma_listesi = list()
            
            for i in firmalar:
                firma_listesi.append(i[0])
            self.firmaListesi.listWidget.addItems(firma_listesi)
        else:
            pass
    def firma_duzenle(self):
        firmaAdi = self.firmaListesi.listWidget.currentItem().text()
        self.cariListesi.show()
        self.cursor.execute("SELECT * FROM cari_kart where cari = ?" , (firmaAdi,))
        data = self.cursor.fetchall()
        self.cariListesi.cariListesi.lineEdit.setText(data[0][0])
        self.cariListesi.cariListesi.textEdit.setText(data[0][1])
        self.cariListesi.cariListesi.lineEdit_2.setText(data[0][2])
        self.cariListesi.cariListesi.lineEdit_3.setText(str(data[0][3]))
        self.cariListesi.cariListesi.lineEdit_4.setText(str(data[0][4]))
        self.cariListesi.cariListesi.lineEdit_5.setText(str(data[0][5]))
        
        self.cursor.execute("delete from cari_kart where cari = ?",(firmaAdi,))
        self.con.commit()
    