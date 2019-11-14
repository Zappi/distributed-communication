import json
from threading import Thread
import socket
import sys


class Client():

    def __init__(self, client_port):
        self.server_port = 8888
        self.identifier = None
        self.server_listener = SocketThread(
            self, client_port, self.server_port)
        self.server_listener.start()


class SocketThread(Thread):
    def __init__(self, client, client_port, server_port):
        Thread.__init__(self)
        self.client = client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.connect(('127.0.0.1', server_port))

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            try:
                data = json.loads(data)
                print(data)
            finally:
                sock.close()
                print('ok boomer')


if __name__ == '__main__':
    client = Client(9999)
    while True:

        cmd = input('> ')

        if cmd.startswith('play'):
            print('pelaa :)')
        elif cmd.startswith('msg'):
            print('message')
        elif cmd.startswith('pmsg'):
            print('play and message')
        else:
            print('Invalid command')
