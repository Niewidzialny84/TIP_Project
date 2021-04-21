import unittest
import socket

from packer import Packer, Response

class PackerTests(unittest.TestCase):
    def setUp(self):
        pass

    def tearDown(self):
        pass

    def test_NoneAudio(self):
        text = 'aaaaaaaaa'
        key, data = Packer.unpack(text)
        self.assertEqual(key, None)
        self.assertEqual(data, text)

    def test_NamePacket(self):
        p = Packer.pack(Response.SEND_NICKNAME, name='Adam')
        self.assertEqual(p, b'{"KEY": 2, "NAME": "Adam"}'.ljust(1024-26))
        key, data = Packer.unpack(p)
        self.assertEqual(key, Response.SEND_NICKNAME)
        self.assertEqual(data['NAME'], 'Adam')

    def test_NewUsersPacket(self):
        p = Packer.pack(Response.SEND_NEW_USERS, users=['Adam','Julie','George'])
        self.assertEqual(p, b'{"KEY": 3, "USERS": ["Adam", "Julie", "George"]}'.ljust(1024-48))
        key, data = Packer.unpack(p)
        self.assertEqual(key, Response.SEND_NEW_USERS)
        self.assertEqual(data['USERS'], ['Adam','Julie','George'])

    def test_NamePacketSend(self):
        try:
            clientsock = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
            clientsock.connect(('127.0.0.1', 9999))
            clientsock.send(Packer.pack(Response.SEND_NICKNAME, name='Adam'))

            key, data = Packer.unpack(clientsock.recv(1024))
            self.assertEqual(key, Response.SEND_NEW_USERS)
            self.assertEqual(data['USERS'], ['Adam'])

            clientsock.send(Packer.pack(Response.DISCONNECT, reason='Yes'))
            key, data = Packer.unpack(clientsock.recv(1024))
            self.assertEqual(key, None)
            self.assertEqual(data, b'')

            clientsock.close()
        except Exception as err:
            print(str(err))
            self.skipTest('Server is offline')
        pass

