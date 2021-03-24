import socket
import threading

class Server:
    def __init__(self):
        #This should get ip address of the card
        self.ip = socket.gethostbyname(socket.gethostname())
        #This should make run socket on all interfaces
        #self.ip = ""
        self.port = 9999
        self.running = False

        try:
            #Binding adress and settings to socket
            self.sock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.sock.bind((self.ip,self.port))

            print('Running on: %s and port %s' % (self.ip, self.port))
        except:
            print('Something went wrong on port bind')
        
        self.connections = []
        

    def run(self):
        self.sock.listen(50)

        #Awating loop for connections
        while self.running:
            connection, address = self.sock.accept()
            self.connections.append(c)
            #Creating new thread for every client
            threading.Thread(target=self.handle,args=(connection,address)).start()
        
    def handle(self,connection,address):
        while self.running:
            try:
                #Data handling
                #FIXME: Add more info into packets and split incoming data
                data = connection.recv(1024)
                self.send(connection,data)
            except socket.error:
                #Close connection on fail and remove from connections list
                connection.close()
                connections.remove(connection)

    def send(self,connection,data):
        #Broadcast send to all connected users except the sender
        for user in self.connections:
            if user != self.sock and user != connection:
                try:
                    client.send(data)
                except:
                    pass

server = Server()
server.run()