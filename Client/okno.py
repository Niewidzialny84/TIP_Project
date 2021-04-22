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
from PyQt5.QtCore import QObject, QThread, pyqtSignal

import traceback, sys, random, string

class Client:
    def __init__(self, ipFromClient, portFromClient):  

        print("Client") 
        print(ipFromClient)
        print(portFromClient)

        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
        while 1:
            try:
                self.target_ip = ipFromClient
                self.target_port = portFromClient

                self.s.connect((self.target_ip, self.target_port))
                self.r.connect((self.target_ip, self.target_port))

                break
            except:
                print("Couldn't connect to server")

        chunk_size = 1024
        audio_format = pyaudio.paInt16
        channels = 1
        rate = 20000

        self.p = pyaudio.PyAudio()
        self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
        self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
        print("Connected to Server")

        receive_thread = threading.Thread(target=self.receive_server_data).start()
        self.send_data_to_server()

    def receive_server_data(self):
        while True:
            try:
                data = self.s.recv(1024)
                self.playing_stream.write(data)
            except:
                pass


    def send_data_to_server(self):
        while True:
            try:
                data = self.recording_stream.read(1024)
                self.s.sendall(data)
            except:
                pass

class Worker(QObject):
    def __init__(self, ip, port):
        self.ip = ip
        self.port = port

    finished = pyqtSignal()
    progress = pyqtSignal(int)

    def run(self):
        print("Worker")
        print(self.ip)
        print(self.port)
        client = Client(self.ip, self.port)

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

    def voiceChat(self, ip, port):
        print("Okno")
        self.thread = QThread()
        self.worker = Worker(ip, port)
        print("Okno 2")
        self.worker.moveToThread(self.thread)
        self.thread.started.connect(self.worker.run)
        print("Okno 3")
        self.worker.finished.connect(self.thread.quit)
        self.worker.finished.connect(self.worker.deleteLater)
        self.thread.finished.connect(self.thread.deleteLater)
        self.worker.progress.connect(self.reportProgress)
        self.thread.start()
        print("Okno 4")

    def confirmButtonClicked(self):
        try:
            self.setCentralWidget(self.secondMenuW)
            self.nickName.setText("Welcome " + self.nickField.text())
            self.nickName.setAlignment(Qt.AlignCenter)
            self.nickName.setFont(QFont('Impact',32))
            colorText = QColor('#05d9e8')
            self.nickName.setStyleSheet("QLabel { color: colorText; }")
            self.userList.addItem(self.nickField.text())

            self.voiceChat(self.addressField.text(), int(self.portField.text()))
            # client = Client(self.addressField.text(), int(self.portField.text()))
        except:
            self.titletext.setText("Error with connection")

    def muteButtonClicked(self):
        if self.muteButton.text() == "Mute":
            self.muteButton.setText("Unmute")
        else:
            self.muteButton.setText("Mute")


    
app = QApplication(sys.argv)

window = Okno()
window.setStyleSheet("background-color: rgb(245,245,220);")
window.show()

app.exec_()