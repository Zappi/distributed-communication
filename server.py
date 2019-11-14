import socket
from threading import Thread, Lock
import sys
import json


class GameServer(Thread):

    def __init__(self):
        self.port = 8889
        Thread.__init__(self)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen()
        print('asdasdasdasd')
        while True:
            print('in while')
            conn, addr = self.sock.accept()
            print('sock accepting')
            data = conn.recv(1024)
            parsed_data = data.decode('utf-8').replace("'", '"')
            print(data)
            print('data recieved')
#            parsed_data = json.loads(data)
            print('data loaded')
            print(parsed_data)


if __name__ == '__main__':
    server = GameServer().start()

