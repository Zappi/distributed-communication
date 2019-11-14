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
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen()
        print('asdasdasdasd')
        while True:
            print('in while')
            conn, addr = self.sock.accept()
            print('sock accepting')
            data = conn.recv(10024)
            print('data recieved')
            data = json.loads(data)
            print('data loaded')

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
