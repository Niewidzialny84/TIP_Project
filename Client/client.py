from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
import threading
import socket
import argparse
import os
import sys
import pyaudio
import tkinter as tk
from tkinter import messagebox
from PyQt5.QtCore import QObject, QThread, pyqtSignal
sys.path.append(os.getcwd())
from Utils.packer import *
import traceback, sys, random, string

messageBox = tk.Tk()
messageBox.wm_withdraw()

class Error(Exception):
    """Error"""
    pass

class invalidNick(Error):
    """Invalid Nick"""
    pass

class Client:
    def __init__(self, ipFromClient, portFromClient, nick):
        
        self.running = True

        self.mute = True

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while 1:
            try:
                # self.target_ip = input('Enter IP address of server --> ')
                # self.target_port = int(input('Enter target port of server --> '))
                self.target_ip = ipFromClient
                self.target_port = portFromClient

                self.s.connect((self.target_ip, self.target_port))
                break
            except:
                print("Couldn't connect to server")
        
        self.nick = nick

        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

        self.receive_thread = threading.Thread(target=self.receive_server_data).start()
        # self.send_data_to_server()
        self.send_thread = threading.Thread(target=self.send_data_to_server).start()

    def receive_server_data(self):
        self.s.send(Packer.pack(Response.SEND_NICKNAME, name=self.nick))
        while self.running:
            try:
                key, data = Packer.unpack(self.s.recv(1024))
                if key == Response.SEND_NEW_USERS:
                    window.userList.clear()
                    for us in data["USERS"]:
                        window.userList.addItem(us)
                else:
                    self.playing_stream.write(data)
            except Exception as ex:
                print(ex)
                pass


    def send_data_to_server(self):
        # while self.mute:
        while self.running:
            try:
                # if self.mute:
                data = self.recording_stream.read(1024)
                self.s.send(data)
            except Exception as ex:
                print(ex)
                pass

    def disconnect(self):
        self.s.send(Packer.pack(Response.DISCONNECT, reason = "Quit"))
        self.running = False
        
class Window(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Window,self).__init__(*args,**kwargs) 
        self.setWindowTitle("TIP Communicator")
        self.setFixedWidth(800)
        self.setFixedHeight(600)

        self.titletext = QLabel()
        self.titletext.setText("Welcome in TIP Communicator")
        self.titletext.setAlignment(Qt.AlignCenter)
        self.titletext.setFont(QFont('Impact',32))
        colorText = QColor('#05d9e8')
        self.titletext.setStyleSheet("QLabel { color: colorText; }")

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

        colorBack = QColor('#01012b')
        self.setStyleSheet("background-color: colorBack;")
        self.mainMenuW = QWidget()
        self.mainMenuW.setLayout(mainMenu)

        self.muteButton = QPushButton()
        self.muteButton.setText("Mute")
        self.muteButton.clicked.connect(self.muteButtonClicked)

        self.userList = QListWidget()

        self.nickName = QLabel()

        secondMenu = QVBoxLayout()
        secondMenu.addWidget(self.nickName)
        secondMenu.addWidget(self.userList)
        secondMenu.setAlignment(Qt.AlignCenter)
        secondMenu.addWidget(self.muteButton)

        self.secondMenuW = QWidget()
        self.secondMenuW.setLayout(secondMenu)

        self.setCentralWidget(self.mainMenuW)

        self.client = None

    def confirmButtonClicked(self):
        try:
            if self.nickField.text().isascii() and len(self.nickField.text()) <= 20:
                self.setCentralWidget(self.secondMenuW)
                self.nickName.setText("Welcome " + self.nickField.text())
                self.nickName.setAlignment(Qt.AlignCenter)
                self.nickName.setFont(QFont('Impact',32))
                colorText = QColor('#05d9e8')
                self.nickName.setStyleSheet("QLabel { color: colorText; }")
                # self.userList.addItem(self.nickField.text())

                self.client = Client(self.addressField.text(), int(self.portField.text()), self.nickField.text())

                # users = self.client.returnList()
                # print(users)
            else:
                raise invalidNick
        except invalidNick:
            self.titletext.setText("Invalid nick")
            messagebox.showinfo("Error", "Nick must be shorter than 20 characters and must consist of ASCII signs")
            # tk.messagebox.showinfo("Error", "Nick must be shorter than 20 characters and must consist of ASCII signs")
        except:
            self.titletext.setText("Error with connection")

    def muteButtonClicked(self):
        if self.muteButton.text() == "Mute":
            self.client.mute = False
            self.muteButton.setText("Unmute")
        else:
            # self.client.send_thread.start()
            self.client.mute = True
            self.muteButton.setText("Mute")
        
    def closeEvent(self, event):
        close = QMessageBox.question(self, "QUIT", "Are you sure want to stop process?", QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
            if self.client != None:
                self.client.disconnect()
        else:
            event.ignore()


    
app = QApplication(sys.argv)

window = Window()
window.setStyleSheet("background-color: rgb(245,245,220);")
window.show()

app.exec_()
