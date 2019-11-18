import json
from threading import Thread, Lock
import socket
import sys
import time


class Client():

    def __init__(self, client_port):
        self.identifier = client_port
        self.server_tcp = ('127.0.0.1', 8889)
        self.lock = Lock()
        self.server_listener = SocketThread(
            self, client_port, self.server_tcp, self.lock)
        self.server_listener.start()
        self.server_message = []

    def send_msg(self, action, play = None, msg = None):
        message = json.dumps({
          "action": action,
          "payload": play,
          "message": msg,
          "player_id": self.identifier
        })

        self.sock_tcp = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock_tcp.connect(self.server_tcp)
        self.sock_tcp.send(message.encode())
        print('message sent')
        data = self.sock_tcp.recv(1024)
        self.sock_tcp.close()
        message = self.parse_data(data)

        print(message)

    def parse_data(self, data):
        try:
            data = json.loads(data)
            if data['success'] == "True":
                return data['message']
            else:
                raise Exception(data['message'])
        except ValueError:
            print(data)

    def get_messages(self):

        message = self.server_message
        self.server_message = []
        return set(message)

class SocketThread(Thread):

    def __init__(self, client, client_port, server_tcp, lock):
        
        Thread.__init__(self)
        self.client = client
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        self.sock.bind(("0.0.0.0", int(client_port)))
        self.lock = lock
        self.time_reference = time.time()

    def run(self):

        while True:
          data, addr = self.sock.recvfrom(1024)
          self.lock.acquire()
          try:
            self.client.server_message.append(data)
            self.print_messages()
          finally:
            self.lock.release()

    def print_messages(self):

        messages = client.get_messages()
        if len(messages) != 0:
            for message in messages:
                message = json.loads(message)
                sender, value = message.popitem()
                print(sender," : ", value)


if __name__ == '__main__':
    if sys.argv[1]:
      client = Client(sys.argv[1])
    else:
      client = Client(9999)
    
    print("Send a play with 'play <num>' \n"
          "1 = rock, 2 = paper, 3 = scissors \n" 
          "Send a message with 'msg <message>'\n"
          "Send a play and message with 'pmsg <num> <message>")

    while True:
        cmd = input('> ')

        if cmd.startswith('play'):
            client.send_msg('play', cmd[5:])
        elif cmd.startswith('msg'):
            client.send_msg('msg', None, cmd[4:])
        elif cmd.startswith('pmsg'):
            client.send_msg('pmsg', cmd[5:6], cmd[6:])
        else:
            print('Invalid command')
