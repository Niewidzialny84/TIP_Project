import socket
import threading

import time
import datetime
import pytz

#custom utils package import
import sys , os
sys.path.append(os.getcwd())
from Utils.packer import *

import re

class ConnectedUser(object):
    current_ids = set()

    def __init__(self, socket, address):
        self.socket = socket
        self.address = address
        self.connected = True
        self.name = None
        
        #Assign Unique Identifier
        self.id = None

        #UDP connection address
        self.UDP = None

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
        return 'ID='+str(self.id)+' ADDR='+str(self.address)+' NAME='+str(self.name)+' STATUS='+str(self.connected)+ ' UDP='+str(self.UDP)

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

            self.udp = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.udp.bind((self.ip,self.port))
        except:
            self.log('Something went wrong on port bind')
        
        self.connections = []
        

    def run(self):
        self.log('Running on: ' + str(self.ip) + ':' + str(self.port) )

        self.sock.listen(50)

        #UDP thread
        threading.Thread(target=self.handleUDP).start()

        #Awating loop for connections
        while self.running:
            self.log('Awaiting more connections...')
            try: 
                connection, address = self.sock.accept()

                self.log(str(address) + ' connected')

                user = ConnectedUser(connection,address)

                self.connections.append(user)
                #Creating new thread for every client
                threading.Thread(target=self.handleTCP,args=(user,)).start()
            except WindowsError as err:
                self.log('WinErr' + str(err))
                pass
            except Exception as err:
                self.log('Some error occured ' + str(err))
                pass

    def handleTCP(self, user: ConnectedUser):
        """TCP data handling for each client"""

        while self.running and user.connected:
            try:
                #recive data
                recv = user.socket.recv(1024)
                #print(data)

                #FIXME: Multiple packets in one
                p = re.compile(r'(?<=\})(?=\{)')
                slices = re.split(p, recv)
                for x in slices:
                    #parse data
                    key , data = Packer.unpack(data)

                    #Nickname handling
                    if key == Response.SEND_NICKNAME:
                        user.name = data['NAME']
                        self.sendAll(Packer.pack(Response.SEND_NEW_USERS,users=self.userList()))
                        self.send(user.socket,Packer.pack(Response.SESSION,session=user.id))
                    #Client disconnect packet handling
                    elif key == Response.DISCONNECT:
                        raise socket.error('User disconnected')
                    elif key == Response.CLIENT_PORT:
                        user.UDP = (user.socket.getsockname()[0],data['PORT'])
            except socket.error:
                #Close connection on fail and remove from connections list
                user.socket.close()
                user.disconnected()
                self.log(str(user.address) + ' disconnected')
                self.connections.remove(user)
                
                self.sendAll(Packer.pack(Response.SEND_NEW_USERS,users=self.userList()))
    
    def handleUDP(self):
        """Broadcast pass on udp"""

        while self.running:
            try:
                recv = self.udp.recvfrom(1024)
                self.sendBroadcastUDP(recv[0],recv[1])
            except socket.error:
                pass

    def sendBroadcastUDP(self,data,exclude):
        for user in self.connections:
            if user.UDP != exclude or user.UDP != None:
                try:
                    self.udp.sendto(data,user.UDP)
                except:
                    pass


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
    
    def userList(self):
        l = []
        for user in self.connections:
            l.append(user.name)
        return l

    def log(self, message: str):
        #Console logging on time
        t = '[ '+ datetime.datetime.now(self.timezone).strftime("%Y-%m-%d %H:%M:%S")+' ]  '
        print(t + str(message))

    def stop(self):
        self.running = False
        self.sock.close()
        self.udp.close()

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
                self.thread.join()
                break
            elif val == 'LIST':
                self.server.log('Getting current user list')
                for user in self.server.connections:
                    print(user) 
            