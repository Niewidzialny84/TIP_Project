x = "test"
print(x.isascii())

# import socket
# import threading
# import pyaudio
# from PyQt5.QtWidgets import *
# from PyQt5.QtGui import *
# from PyQt5.QtCore import *

# class Client:
#     def __init__(self, ipFromClient, portFromClient):

#         self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#         self.r = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        
#         while 1:
#             try:
#                 # self.target_ip = input('Enter IP address of server --> ')
#                 # self.target_port = int(input('Enter target port of server --> '))
#                 self.target_ip = ipFromClient
#                 self.target_port = portFromClient

#                 self.s.connect((self.target_ip, self.target_port))
#                 self.r.connect((self.target_ip, self.target_port))

#                 break
#             except:
#                 print("Couldn't connect to server")

#         chunk_size = 1024
#         audio_format = pyaudio.paInt16
#         channels = 1
#         rate = 20000

#         self.p = pyaudio.PyAudio()
#         self.playing_stream = self.p.open(format=audio_format, channels=channels, rate=rate, output=True, frames_per_buffer=chunk_size)
#         self.recording_stream = self.p.open(format=audio_format, channels=channels, rate=rate, input=True, frames_per_buffer=chunk_size)
        
#         print("Connected to Server")

#         receive_thread = threading.Thread(target=self.receive_server_data).start()
#         self.send_data_to_server()

#     def receive_server_data(self):
#         while True:
#             try:
#                 data = self.s.recv(1024)
#                 self.playing_stream.write(data)
#             except:
#                 pass


#     def send_data_to_server(self):
#         while True:
#             try:
#                 data = self.recording_stream.read(1024)
#                 self.s.sendall(data)
#             except:
#                 pass

# client = Client("localhost", 9999)





# import pyaudio
# import wave
# import simpleaudio as sa
# import keyboard
# from PyQt5.QtCore import Qt
# from PyQt5.QtWidgets import *
# import socket

# host = '192.168.56.1'  # The server's hostname or IP address
# port = 9999        # The port used by the server
# buffer_size = 1024

# chunk = 1024  # Record in chunks of 1024 samples
# sample_format = pyaudio.paInt16  # 16 bits per sample
# channels = 1
# fs = 44100  # Record at 44100 samples per second
# seconds = 3
# filename = "output.wav"

# p = pyaudio.PyAudio()  # Create an interface to PortAudio

# text = "Hello, World!"
# s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
# s.connect((host, port))
# text = text.encode('utf-8')
# s.send(text)
# data = s.recv(buffer_size)
# s.close()
# print("received data:", data)

# while True:
#     if keyboard.is_pressed('r'):
#         print('Recording')

#         stream = p.open(format=sample_format,
#                         channels=channels,
#                         rate=fs,
#                         frames_per_buffer=chunk,
#                         input=True)

#         frames = []  # Initialize array to store frames

#         # Store data in chunks for 3 seconds
#         for i in range(0, int(fs / chunk * seconds)):
#             data = stream.read(chunk)
#             frames.append(data)

#         # Stop and close the stream 
#         stream.stop_stream()
#         stream.close()
#         # Terminate the PortAudio interface
#         p.terminate()

#         print('Finished recording')

#         # Save the recorded data as a WAV file
#         wf = wave.open(filename, 'wb')
#         wf.setnchannels(channels)
#         wf.setsampwidth(p.get_sample_size(sample_format))
#         wf.setframerate(fs)
#         wf.writeframes(b''.join(frames))
#         wf.close()

#     elif keyboard.is_pressed('p'):
#         print('Playing')
#         wave_obj = sa.WaveObject.from_wave_file(filename)
#         play_obj = wave_obj.play()
#         play_obj.wait_done() 
#         print('Finished playing')
        
# # from PyQt5.QtWidgets import *
# # from PyQt5.QtGui import *
# # from PyQt5.QtCore import *

# # import traceback, sys, random, string

# # class Okno(QMainWindow):
# #     def __init__(self,*args,**kwargs):
# #         super(Okno,self).__init__(*args,**kwargs) 
# #         self.setWindowTitle("TIP Communicator")
# #         self.setFixedWidth(800)
# #         self.setFixedHeight(600)

# #         self.titletext = QLabel()
# #         self.titletext.setText("Welcome in TIP Communicator")
# #         self.titletext.setAlignment(Qt.AlignCenter)
# #         self.titletext.setFont(QFont('Impact',32))
# #         self.titletext.setStyleSheet("QLabel { color: black; }")

# #         loginButton = QPushButton()
# #         self.addressField = QLineEdit()
# #         self.addressField.setPlaceholderText("IP Address")

# #         self.portField = QLineEdit()
# #         self.portField.setPlaceholderText("Port Number")

# #         self.nickField = QLineEdit()
# #         self.nickField.setPlaceholderText("Nick")

# #         confirmButton = QPushButton()
# #         confirmButton.setText("Confirm")
# #         confirmButton.clicked.connect(self.confirmButtonClicked)

# #         mainMenu = QVBoxLayout()
# #         mainMenu.setAlignment(Qt.AlignCenter)
# #         mainMenu.addWidget(self.titletext)
# #         mainMenu.addWidget(self.addressField)
# #         mainMenu.addWidget(self.portField)
# #         mainMenu.addWidget(self.nickField)
# #         mainMenu.addWidget(confirmButton)

        
# #         self.mainMenuW = QWidget()
# #         self.mainMenuW.setLayout(mainMenu)


# #         self.setCentralWidget(self.mainMenuW)

# #     def confirmButtonClicked(self):
# #         self.titletext.setText("Confirmed")
    


# # app = QApplication(sys.argv)

# # window = Okno()
# # #window.setFixedSize(800,600)
# # window.setStyleSheet("background-color: rgb(245,245,220);")
# # window.show()

# # app.exec_()