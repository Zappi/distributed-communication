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

        while True:
            conn, addr = self.sock.accept()

            data = conn.recv(1024)
            parsed_data = json.loads(data)

            print(parsed_data)

            message = json.dumps({"success": "True", "message": "message recieved"})
            conn.send(message.encode())


if __name__ == '__main__':
    server = GameServer().start()
