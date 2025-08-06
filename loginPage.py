import sqlite3
from PyQt5.QtWidgets import *
from loginPageUi import Ui_Form
from mainWindow import MainWindow
from passlib.hash import sha256_crypt

class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.loginForm = Ui_Form()
        self.loginForm.setupUi(self)
        self.mainPageOpen = MainWindow()
        self.loginForm.pbGiris.clicked.connect(self.giris)
        

    def giris(self):
        #Formdan kullanıcı adı ve sifre alınıyor
        k_adi = self.loginForm.lineEdit.text()
        sifre = self.loginForm.lineEdit_2.text()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("select * from login where kullanici_adi = ?",(k_adi,))
        #Veritabanından karşılaştırmak üzere kullanıcı adı ve sah256 işe şifrelenmiş şifre bilgisi alınıyor
        result = self.cursor.fetchall()
        #Formdan gelen veri ile veritabanından gelen şifrelenmiş veri karşılaştırlıyor.
        if result and result[0][0] == k_adi and sha256_crypt.verify(sifre,result[0][1]):
            self.hide()
            self.mainPageOpen.show()
        