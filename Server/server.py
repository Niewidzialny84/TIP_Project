import socket
import threading

import time
import datetime
import pytz

#custom utils package import
import sys , os
sys.path.append(os.getcwd())
from Utils.packer import a

class Server:
    def __init__(self,port):
        #This should get ip address of the card
        #self.ip = socket.gethostbyname(socket.gethostname())
        #This should make run socket on all interfaces
        self.ip = ""
        self.port = port
        self.running = True

        self.timezone = pytz.timezone('Europe/Warsaw')

        try:
            #Binding adress and settings to socket
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind((self.ip,self.port))

        except:
            self.log('Something went wrong on port bind')
        
        self.connections = []
        

    def run(self):
        self.log('Running on: ' + str(self.ip) + ':' + str(self.port) )

        self.sock.listen(50)

        #Awating loop for connections
        while self.running:
            self.log('Awaiting more connections...')
            try: 
                connection, address = self.sock.accept()
                self.log(str(address) + ' connected')
                self.connections.append(connection)
                #Creating new thread for every client
                threading.Thread(target=self.handle,args=(connection,address)).start()
            except WindowsError:
                pass
            except Exception as err:
                self.log('Some error occured ' + str(err))
                pass

    def handle(self,connection,address):
        loop = False
        while self.running and not loop:
            try:
                #Data handling
                #FIXME: Add more info into packets and split incoming data
                data = connection.recv(1024)
                self.send(connection,data)
            except socket.error:
                #Close connection on fail and remove from connections list
                connection.close()
                self.log(str(connection))
                loop = True
                # self.connections.remove(connection)

    def send(self,connection,data):
        #Broadcast send to all connected users except the sender
        for user in self.connections:
            if user != self.sock and user != connection:
                try:
                    user.send(data)
                except:
                    pass

    def log(self, message: str):
        #Console logging on time
        t = '[ '+ datetime.datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")+' ]  '
        print(t + str(message))

    def stop(self):
        self.running = False
        self.sock.close()

class ConsoleApp:
    def __init__(self, port: int):
        #self.ipaddr = ipaddr
        self.port = port

        self.server = Server(self.port)

        self.thread = threading.Thread(target=self.server.run)      

        self.server.log('Starting server')
        self.thread.start()
        
        self.run()

    def run(self):
        while(True):
            val = str(input())
            if val.upper() == 'STOP':
                self.server.log('Stopping server...')
                self.server.stop()
                break
                