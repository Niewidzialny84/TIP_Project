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
        loginButton.setText("Sign in")
        loginButton.clicked.connect(self.loginClicked)

        registerButton = QPushButton()
        registerButton.setText("Sign up")
        registerButton.clicked.connect(self.registerClicked)

        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(self.titletext)
        mainMenu.addWidget(loginButton)
        mainMenu.addWidget(registerButton)


        self.logintext = QLabel()
        self.logintext.setText("Type in username and password")
        self.logintext.setAlignment(Qt.AlignCenter)
        self.logintext.setFont(QFont('Impact',32))
        self.logintext.setStyleSheet("QLabel { color: black; }")

        self.userNameLoginField = QLineEdit()
        self.userNameLoginField.setPlaceholderText("Username")

        self.passwordLoginField = QLineEdit()
        self.passwordLoginField.setPlaceholderText("Password")

        confirmLoginButton = QPushButton()
        confirmLoginButton.setText("Confirm")
        confirmLoginButton.clicked.connect(self.confirmLoginButtonClicked)

        loginMenu = QVBoxLayout()
        loginMenu.setAlignment(Qt.AlignCenter)
        loginMenu.addWidget(self.logintext)
        loginMenu.addWidget(self.userNameLoginField)
        loginMenu.addWidget(self.passwordLoginField)
        loginMenu.addWidget(confirmLoginButton)


        self.registertext = QLabel()
        self.registertext.setText("Type in username and password")
        self.registertext.setAlignment(Qt.AlignCenter)
        self.registertext.setFont(QFont('Impact',32))
        self.registertext.setStyleSheet("QLabel { color: black; }")

        self.userNameRegisterField = QLineEdit()
        self.userNameRegisterField.setPlaceholderText("Username")

        self.passwordRegisterField = QLineEdit()
        self.passwordRegisterField.setPlaceholderText("Password")

        self.passwordConfirmRegisterField = QLineEdit()
        self.passwordConfirmRegisterField.setPlaceholderText("Confirm password")

        confirmRegisterButton = QPushButton()
        confirmRegisterButton.setText("Confirm")
        confirmRegisterButton.clicked.connect(self.confirmRegisterButtonClicked)

        registerMenu = QVBoxLayout()
        registerMenu.setAlignment(Qt.AlignCenter)
        registerMenu.addWidget(self.registertext)
        registerMenu.addWidget(self.userNameRegisterField)
        registerMenu.addWidget(self.passwordRegisterField)
        registerMenu.addWidget(self.passwordConfirmRegisterField)
        registerMenu.addWidget(confirmRegisterButton)

        
        self.mainMenuW = QWidget()
        self.mainMenuW.setLayout(mainMenu)

        self.loginMenuW = QWidget()
        self.loginMenuW.setLayout(loginMenu)

        self.registerMenuW = QWidget()
        self.registerMenuW.setLayout(registerMenu)



        self.setCentralWidget(self.mainMenuW)

    def loginClicked(self):
        self.titletext.setText("Login clicked")
        self.setCentralWidget(self.loginMenuW)

    def registerClicked(self):
        self.titletext.setText("Register clicked")
        self.setCentralWidget(self.registerMenuW)

    def confirmLoginButtonClicked(self):
        self.setCentralWidget(self.mainMenuW)

    def confirmRegisterButtonClicked(self):
        self.setCentralWidget(self.mainMenuW)
    


app = QApplication(sys.argv)

window = Okno()
#window.setFixedSize(800,600)
window.setStyleSheet("background-color: rgb(245,245,220);")
window.show()

app.exec_()
