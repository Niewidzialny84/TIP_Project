from enum import Enum

class Response(Enum):
    ACK = 0
    UNKNOWN_ERROR = 1
    LOGIN = 2
    NEW_USER = 3

class Packer(object):

    @staticmethod
    def pack(type: Response, size: int, data):
        #TODO: addme
        return 1


    @staticmethod
    def unpack(size: int, bytes):
        #TODO: addme too
        return 1

class Secure(object):
    self.key = 'password'


