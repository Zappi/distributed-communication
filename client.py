import json
import threading
import socket
import sys


class Client():

    def __init__(self, client_port):
        self.identifier = None
        self.server_listener = SocketThread(self, client_port)
        self.server_listener.run()


class SocketThread():

    def __init__(self, client, client_port):
        self.client = client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', client_port))

    def run(self):
        while True:
            data, addr = self.sock.recvfrom(1024)

            try:
                data = json.loads(data)
                print(data)


if __name__ == '__main__':
    print('vittu')
