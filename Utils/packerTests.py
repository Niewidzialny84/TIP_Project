import unittest

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
        self.assertEqual(p, b'{"KEY": 2, "NAME": "Adam"}')
        key, data = Packer.unpack(p)
        self.assertEqual(key, Response.SEND_NICKNAME)
        self.assertEqual(data['NAME'], 'Adam')

    def test_NewUsersPacket(self):
        p = Packer.pack(Response.SEND_NEW_USERS, users=['Adam','Julie','George'])
        self.assertEqual(p, b'{"KEY": 3, "USERS": ["Adam", "Julie", "George"]}')
        key, data = Packer.unpack(p)
        self.assertEqual(key, Response.SEND_NEW_USERS)
        self.assertEqual(data['USERS'], ['Adam','Julie','George'])
