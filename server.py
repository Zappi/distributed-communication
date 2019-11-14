import socket
from threading import Thread, Lock
import sys
import json


class GameServer(Thread):

    def __init__(self):
        self.port = 8888
        Thread.__init__(self)

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen()

        while True:
            conn, addr = self.sock.accept()
            data = conn.recv(1024)
            data = json.loads(data)

            print(data)


if __name__ == '__main__':
    GameServer().run()


'''
    {
      user: 'Olli',
      msg: 'Hey you',
      play: 'rock',
    }
'''
