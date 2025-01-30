import sqlite3
from PyQt5.QtWidgets import *
from loginPageUi import Ui_Form
from mainWindow import MainWindow


class Login(QWidget):
    def __init__(self):
        super().__init__()
        self.loginForm = Ui_Form()
        self.loginForm.setupUi(self)
        self.mainPageOpen = MainWindow()
        self.loginForm.pbGiris.clicked.connect(self.giris)
        

    def giris(self):
        
        kadi = self.loginForm.lineEdit.text()
        sifre = self.loginForm.lineEdit_2.text()
        self.con = sqlite3.connect("database.db")
        self.cursor = self.con.cursor()
        self.cursor.execute("select * from login where kullanici_adi = ? and kullanici_sifre = ?",(kadi,sifre))
        data = self.cursor.fetchall()
        
        
        if len(data) > 0:
            if data[0][0] == kadi and data[0][1] == sifre:
                    
                self.hide()
                self.mainPageOpen.show()
            