from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *

import traceback, sys, random, string

class Okno(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Okno,self).__init__(*args,**kwargs) 
        self.setWindowTitle("TIP Communicator")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        self.titletext = QLabel()
        self.titletext.setText("Welcome in TIP Communicator")
        self.titletext.setAlignment(Qt.AlignCenter)
        self.titletext.setFont(QFont('Impact',32))
        self.titletext.setStyleSheet("QLabel { color: black; }")

        loginButton = QPushButton()
        self.addressField = QLineEdit()
        self.addressField.setPlaceholderText("IP Address")

        self.portField = QLineEdit()
        self.portField.setPlaceholderText("Port Number")

        self.nickField = QLineEdit()
        self.nickField.setPlaceholderText("Nick")

        confirmButton = QPushButton()
        confirmButton.setText("Confirm")
        confirmButton.clicked.connect(self.confirmButtonClicked)

        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(self.titletext)
        mainMenu.addWidget(self.addressField)
        mainMenu.addWidget(self.portField)
        mainMenu.addWidget(self.nickField)
        mainMenu.addWidget(confirmButton)

        
        self.mainMenuW = QWidget()
        self.mainMenuW.setLayout(mainMenu)


        self.setCentralWidget(self.mainMenuW)

    def confirmButtonClicked(self):
        self.titletext.setText("Confirmed")
    


app = QApplication(sys.argv)

window = Okno()
#window.setFixedSize(800,600)
window.setStyleSheet("background-color: rgb(245,245,220);")
window.show()

app.exec_()
