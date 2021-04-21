from enum import Enum
import json

class Response(Enum):
    ACK = 0
    UNKNOWN_ERROR = 1
    SEND_NICKNAME = 2
    SEND_NEW_USERS = 3
    DISCONNECT = 4
    SERVER_CLOSE = 5


class Packer(object):

    @staticmethod
    def pack(key: Response, **kwargs):
        """Packaging method with specified parameters based on key Response type"""

        package = {}
        if key == Response.SEND_NICKNAME:
            name = kwargs.get('name',None)
            if name != None:
                package = {'KEY':key.value,'NAME':name}
            else:
                raise TypeError('--Pack-- Name was missing')
        elif key == Response.SEND_NEW_USERS:
            users = kwargs.get('users',None)
            if users != None:
                package = {'KEY':key.value,'USERS':users}
            else:
                raise TypeError('--Pack-- Users were missing')
        elif key == Response.DISCONNECT:
            reason = kwargs.get('reason',None)
            package = {'KEY':key.value,'REASON': reason}

        package = json.dumps(package)
        package = package.ljust(1024-len(package))
        return package.encode(encoding='ASCII')


    @staticmethod
    def unpack(data: str):
        """Unpackaging method that returns a key and the data"""
        
        package = None
        key = None
        try:
            package = json.loads(data.decode())
            key = Response(package['KEY'])
        except: 
            return key,data
            pass

        return key, package


class Secure(object):
    key = 'password'

