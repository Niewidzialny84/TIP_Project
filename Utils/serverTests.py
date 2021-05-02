import unittest
import socket

from packer import Packer, Response

class ServerTests(unittest.TestCase):
    def setUp(self):
        try:
            self.clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientsock.connect(('127.0.0.1', 9999))
            self.clientsock2 = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            self.clientsock2.connect(('127.0.0.1', 9999))
        except Exception as err:
            self.skipTest('Server is offline')
        pass

    def tearDown(self):
        self.clientsock.close()
        self.clientsock2.close()
        pass
    
    @unittest.skip('Scenario changed')
    def test_SimpleCommunication(self):
        #User 1 login
        self.clientsock.send(Packer.pack(Response.SEND_NICKNAME, name='Adam'))

        key, data = Packer.unpack(self.clientsock.recv(1024))
        self.assertEqual(key, Response.SEND_NEW_USERS)
        self.assertEqual(data['USERS'], ['Adam'])

        #User 2 login
        self.clientsock2.send(Packer.pack(Response.SEND_NICKNAME, name='George'))

        key, data = Packer.unpack(self.clientsock2.recv(1024))
        self.assertEqual(key, Response.SEND_NEW_USERS)
        self.assertEqual(data['USERS'], ['Adam','George'])

        #User 1 Recives update of the list
        key, data = Packer.unpack(self.clientsock.recv(1024))
        self.assertEqual(key, Response.SEND_NEW_USERS)
        self.assertEqual(data['USERS'], ['Adam','George'])


        for x in range(10):
            #User 1 send packet
            val = ('A'+str(x)).encode()
            self.clientsock.send(val)

            #User 2 recives packet
            recv = self.clientsock2.recv(1024)
            self.assertEqual(val, recv)

            #User 2 sends packet
            self.clientsock2.send(val)

            #User 1 recives packet
            recv = self.clientsock.recv(1024)
            self.assertEqual(val,recv)

        #User 2 leaves
        self.clientsock2.send(Packer.pack(Response.DISCONNECT, reason='Yes v2'))

        #User 1 gets updated list
        key, data = Packer.unpack(self.clientsock.recv(1024))
        self.assertEqual(key, Response.SEND_NEW_USERS)
        self.assertEqual(data['USERS'], ['Adam'])

        #User 1 leaves
        self.clientsock.send(Packer.pack(Response.DISCONNECT, reason='Yes'))
        key, data = Packer.unpack(self.clientsock.recv(1024))
        self.assertEqual(key, None)
        self.assertEqual(data, b'')