from PyQt5.QtWidgets import *
from PyQt5.QtGui import *
from PyQt5.QtCore import *
from PyQt5.QtCore import QObject, QThread, pyqtSignal

import tkinter as tk
from tkinter import messagebox

import os, sys
import traceback, random, string
import time

sys.path.append(os.getcwd())
from Utils.packer import *

import threading
import socket
import argparse
import pyaudio

import re

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
        self.nick = nick
        self.mute = False

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        self.session = None

        while 1:
            try:
                self.target_ip = ipFromClient
                self.target_port = portFromClient
                self.address = (self.target_ip,self.target_port)

                self.s.connect(self.address)
                self.s.send(Packer.pack(Response.SEND_NICKNAME, name=self.nick))

                break
            except:
                raise Error
                break
        

        self.udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        self.udp.bind(("",0))

        self.s.send(Packer.pack(Response.CLIENT_PORT, port = self.udp.getsockname()[1]))  
        self.udp.sendto(('a'*1024).encode(),self.address)

        chunk_size = 512
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

        self.receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.udpSendThread = threading.Thread(target=self.udpSend).start()
        self.udpReciveThread = threading.Thread(target=self.udpRecive).start()


    def udpSend(self):
        while self.running:
            try:
                if self.mute:
                    data = self.recording_stream.read(512)
                    self.udp.sendto(data,self.address)
            except Exception as ex:
                print(ex)
                break
                pass

    def udpRecive(self):
        while self.running:
            try:
                recv = self.udp.recvfrom(1024)
                self.playing_stream.write(recv[0])
            except:
                pass

    def receive_server_data(self):
        while self.running:
            try:
                recv = self.s.recv(1024)

                p = re.compile(r'(?<=\})(?=\{)')
                slices = re.split(p, recv.decode())

                for x in slices:
                    key, data = Packer.unpack(x.encode())
                    if key == Response.SEND_NEW_USERS:
                        window.userList.clear()
                        for us in data["USERS"]:
                            window.userList.addItem(us)
                    elif key == Response.SESSION:
                        self.session = data['SESSION']
                    elif key == Response.SERVER_CLOSE:
                        self.disconnect()
                        window.disconnectButtonClicked()

            except Exception as ex:
                print(ex)
                break
                pass

    def disconnect(self):
        self.s.send(Packer.pack(Response.DISCONNECT, reason = "Quit"))
        self.running = False
        self.s.close()
        self.udp.close()
        
class Window(QMainWindow):
    def __init__(self,*args,**kwargs):
        super(Window,self).__init__(*args,**kwargs) 
        self.setWindowTitle("TIP Communicator")
        self.setFixedWidth(400)
        self.setFixedHeight(600)
        self.setStyleSheet('QMainWindow {background-color: #e4e3e3;} QMessageBox {background-color: #e4e3e3;color: #204051;} QListWidget::item:selected { background-color: #e4e3e3; color: #204051; } QLabel { color: #204051; } QLineEdit {background-color: #84a9ac; border: 1px solid #3b6978} QPushButton {background-color: #84a9ac;color: #204051;border: 1px solid #3b6978; min-height:20px;min-width:50px}')
        self.setAutoFillBackground(True)

        self.BigFont = QFont('Impact',28)
        
        self.titletext = QLabel()
        self.titletextText = "Voice Communicator"
        self.titletext.setText(self.titletextText)
        self.titletext.setAlignment(Qt.AlignCenter)
        self.titletext.setFont(self.BigFont)

        self.addressField = QLineEdit()
        self.addressField.setPlaceholderText("IP Address")

        self.nickField = QLineEdit()
        self.nickField.setPlaceholderText("Nickname")

        confirmButton = QPushButton()
        confirmButton.setText("Confirm")
        confirmButton.clicked.connect(self.confirmButtonClicked)

        mainMenu = QVBoxLayout()
        mainMenu.setAlignment(Qt.AlignCenter)
        mainMenu.addWidget(self.titletext)
        mainMenu.addWidget(self.addressField)
        mainMenu.addWidget(self.nickField)
        mainMenu.addWidget(confirmButton)

        self.mainMenuW = QWidget()
        self.mainMenuW.setLayout(mainMenu)

        #Second Window

        self.muteButton = QPushButton()
        self.muteButton.setText("Unmute Microphone")
        self.muteButton.clicked.connect(self.muteButtonClicked)

        self.disconnectButton = QPushButton()
        self.disconnectButton.setText('Disconnect')
        self.disconnectButton.clicked.connect(self.disconnectButtonClicked)

        self.userList = QListWidget()
        self.userList.setStyleSheet('color: #204051; background-color: #84a9ac; border: 1px solid #3b6978')

        self.nickName = QLabel()

        secondMenu = QVBoxLayout()
        secondMenu.addWidget(self.nickName)
        secondMenu.addWidget(self.userList)
        secondMenu.setAlignment(Qt.AlignCenter)
        secondMenu.addWidget(self.muteButton)
        secondMenu.addWidget(self.disconnectButton)

        self.secondMenuW = QWidget()
        self.secondMenuW.setLayout(secondMenu)

        self.client = None

        self.Stack = QStackedWidget(self)
        self.Stack.addWidget(self.mainMenuW)
        self.Stack.addWidget(self.secondMenuW)
        self.setCentralWidget(self.Stack)

    def confirmButtonClicked(self):
        
        ip,port = self.validateAddress()
        if self.validateName() and ip != None and port != None:
            self.nickName.setText("Joined as: " + self.nickField.text())
            self.nickName.setAlignment(Qt.AlignLeft)
            self.nickName.setFont(self.BigFont)
            try:
                self.client = Client(ip, port, self.nickField.text())
                self.titletext.setText(self.titletextText)
                self.Stack.setCurrentIndex(1)
            except Error:
                self.titletext.setText("Cannot connect")
                pass
        
    def disconnectButtonClicked(self):
        self.Stack.setCurrentIndex(0)
        self.client.disconnect()
        self.client = None

    def muteButtonClicked(self):
        if self.muteButton.text() == "Mute Microphone":
            self.client.mute = False
            self.muteButton.setText("Unmute Microphone")
        else:
            self.client.mute = True
            self.muteButton.setText("Mute Microphone")
        
    def closeEvent(self, event):
        close = QMessageBox.question(self, "QUIT", "Are you sure want to quit?", QMessageBox.Yes | QMessageBox.No)
        if close == QMessageBox.Yes:
            event.accept()
            if self.client != None:
                self.client.disconnect()
        else:
            event.ignore()

    def validateName(self):
        if len(self.nickField.text()) >= 20 or self.nickField.text() == '':
            self.titletext.setText("Invalid nick")
            #messageBox.showinfo('Error','Nick must be shorter than 20 characters')
            return False
        return True

    def validateAddress(self):
        try:
            addr = self.addressField.text()
            addr = addr.split(sep=':')
            ip = addr[0]
            port = int(addr[1])

            reg = r'^(([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])\.){3}([0-9]|[1-9][0-9]|1[0-9]{2}|2[0-4][0-9]|25[0-5])$'

            if port > 0 and port <= 65535 and re.match(reg,ip):
                return ip, port
        except:
            pass
        
        self.titletext.setText("Invalid address")
        #messageBox.showerror('Error','Invalid address')

        return None,None


    
app = QApplication(sys.argv)

window = Window()
window.show()

app.exec_()
