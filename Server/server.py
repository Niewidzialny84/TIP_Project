import socket
import threading

import time
import datetime
import pytz

#custom utils package import
import sys , os
sys.path.append(os.getcwd())
from Utils.packer import *

class ConnectedUser(object):
    current_ids = set()

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.connected = True
        self.name = None
        
        #Assign Unique Identifier
        self.id = None

        for i in range(1000):
            if not ConnectedUser.current_ids.issuperset(set([i])):
                self.id = i
                ConnectedUser.current_ids.add(i)
                break
    
    def disconnected(self):
        self.connected = False
        #Free the id
        ConnectedUser.current_ids.remove(self.id)

    def __repr__(self):
        return 'ID='+str(self.id)+' ADDR='+str(self.address)+' NAME='+str(self.name)+' STATUS='+str(self.connected)

class Server(object):
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
                user = ConnectedUser(connection,address)
                self.connections.append(user)
                #Creating new thread for every client
                threading.Thread(target=self.handle,args=(user,)).start()
            except WindowsError:
                pass
            except Exception as err:
                self.log('Some error occured ' + str(err))
                pass

    def handle(self, user: ConnectedUser):
        while self.running and user.connected:
            try:
                #Data handling
                #FIXME: Add more info into packets and split incoming data
                data = user.socket.recv(1024)
                self.sendBroadcast(user.socket,data)
            except socket.error:
                #Close connection on fail and remove from connections list
                user.socket.close()
                user.disconnected()
                self.log(str(user.address) + ' disconnected')
                self.connections.remove(user)

    def send(self,connection,data):
        try:
            connection.send(data)
        except:
            pass

    def sendAll(self,data):
        for user in self.connections:
            try:
                user.socket.send(data)
            except:
                pass

    def sendBroadcast(self,connection,data):
        #Broadcast send to all connected users except the sender
        for user in self.connections:
            if user.socket != self.sock and user.socket != connection:
                try:
                    user.socket.send(data)
                except:
                    pass

    def log(self, message: str):
        #Console logging on time
        t = '[ '+ datetime.datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")+' ]  '
        print(t + str(message))

    def stop(self):
        self.running = False
        self.sock.close()

class ConsoleApp(object):
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
            val = str(input()).upper()
            if val == 'STOP':
                self.server.log('Stopping server...')
                self.server.stop()
                break
            elif val == 'LIST':
                self.server.log('Getting current user list')
                for user in self.server.connections:
                    print(user) 
            