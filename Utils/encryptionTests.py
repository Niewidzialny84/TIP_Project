import unittest
import socket
import pyDH


class encryptionTests(unittest.TestCase):
    def setUp(self):
        self.ip = "127.0.0.1"
        self.port = 9999
        self.addr = (self.ip,self.port)
        try:
            self.server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.server.bind(self.addr)
            self.client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.client.bind(('127.0.0.1',9998))
        except Exception as err:
            print(err)
            self.skipTest('Bind Wrong')
        pass

    def tearDown(self):
        self.server.close()
        self.client.close()
        pass

    def test_SendingKey(self):
        clientDH = pyDH.DiffieHellman()
        clientPubKey = clientDH.gen_public_key()
        
        self.client.sendto(str(clientPubKey).encode(),self.addr)
        recv = self.server.recvfrom(1024)

        serverDH = pyDH.DiffieHellman()
        serverPubKey = serverDH.gen_public_key()
        serverShared = serverDH.gen_shared_key(int(recv[0].decode()))

        self.server.sendto(str(serverPubKey).encode(),recv[1])
        recv = self.client.recvfrom(1024)
        clientShared = clientDH.gen_shared_key(int(recv[0].decode()))
        self.assertEqual(clientShared,serverShared)
