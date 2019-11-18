import json
from threading import Thread
import socket
import sys


class Client():

    def __init__(self, client_port):
        self.identifier = client_port
        self.server_tcp = ('127.0.0.1', 8889)
#        self.server_listener = SocketThread(
#            self, client_port, self.server_tcp)
#        self.server_listener.start()


    def send_play(self, play):
        message = json.dumps({
          "action": "play",
          "payload": play,
          "player_id": self.identifier
        })
        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode())
        print('message sent')
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)

        return message

    def parse_data(self, data):
        try:
            data = json.loads(data)
            if data['success'] == "True":
                return data['message']
            else:
                raise Exception(data['message'])
        except ValueError:
            print(data)

#class SocketThread(Thread):
#    def __init__(self, client, client_port, server_tcp):
#        Thread.__init__(self)
#        self.client = client
#        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
#        self.sock.connect(server_tcp)
#
#    def run(self):
#        while True:
#            data, addr = self.sock.recvfrom(1024)
#
#            try:
#                data = json.loads(data)
#                print(data)
#            finally:
#                self.sock.close()


if __name__ == '__main__':
    if sys.argv[1]:
      client = Client(sys.argv[1])
    else:
      client = Client(9999)

    while True:

        cmd = input('> ')

        if cmd.startswith('play'):
            client.send_play(cmd[5:])
        elif cmd.startswith('msg'):
            client.send_msg(cmd[4:])
        elif cmd.startswith('pmsg'):
            client.send_play(cmd[5:6])
            client.send_msg(cmd[6:])
        else:
            print('Invalid command')
