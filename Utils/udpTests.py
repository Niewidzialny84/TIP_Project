import unittest
import socket

class udpTests(unittest.TestCase):
    def setUp(self):
        self.ip = "127.0.0.1"
        self.port = 9999
        self.addr = (self.ip,self.port)
        try:
            self.server = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
            self.server.bind(self.addr)
            self.client = socket.socket(socket.AF_INET,socket.SOCK_DGRAM)
        except Exception as err:
            print(err)
            self.skipTest('Bind Wrong')
        pass

    def tearDown(self):
        self.server.close()
        self.client.close()
        pass

    def test_SimpleSendRecive(self):
        send = b'abc'
        self.client.sendto(send,self.addr)

        recv = self.server.recvfrom(1024)
        self.assertEqual(send,recv[0])

    def test_MultipleSendRecive(self):
        send = b'cbdd'
        port = 9998
        self.client.bind((self.ip,port))

        for x in range(5):
            self.client.sendto(send,self.addr)

            recv = self.server.recvfrom(1024)
            #check if message the same
            self.assertEqual(send,recv[0])
            self.assertEqual(recv[1][1], port)

    def test_FullDuplexSendRecive(self):
        send = b'xdfxx'
        clientAddr = (self.ip,9998)
        self.client.bind(clientAddr)

        for x in range(5):
            # Client -> Server
            self.client.sendto(send, self.addr)

            recv = self.server.recvfrom(1024)
            self.assertEqual(send,recv[0])

            # Server -> Client
            self.server.sendto(recv[0],clientAddr)

            recv = self.client.recvfrom(1024)
            self.assertEqual(send,recv[0])

    def test_ClientBind(self):
        self.client.bind(('',0))
        
        #sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        addr = self.client.getsockname()
        for x in range(5):
            self.client.sendto(b'abcccc',self.addr)

            recv = self.server.recvfrom(1024)
            self.assertEqual(addr[1],recv[1][1])