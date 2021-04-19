from server import ConsoleApp
from os import getenv
from sys import argv

if __name__ == '__main__':
    #ipaddr = getenv('IP')
    port = getenv('PORT')

    #temporary hard code port
    #FIXME: Remove or comment on deploy
    port = 9999

    if port is None:
        if len(argv) == 2:
            port = argv[1]
        else:
            print('Missing argument or too many')

    if port is not None:
        app = ConsoleApp(port)