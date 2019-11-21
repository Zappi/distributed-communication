import socket
from threading import Thread, Lock
import sys
import json


def server_loop():
    game_server = GameServer()
    game_server.start()
    print("Type 'log' to view logs")

    while True:
        cmd = input('> ')

        if cmd == 'log':
            game_server.print_logs()


class GameServer(Thread):

    def __init__(self):
        self.port = 8889
        Thread.__init__(self)
        self.log = []

    def run(self):
        self.sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.sock.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
        self.sock.bind(('0.0.0.0', self.port))
        self.sock.listen()
        self.game = Game(self)

        while True:
            conn, addr = self.sock.accept()

            data = conn.recv(1024)
            parsed_data = json.loads(data)

            self.interpret_message(parsed_data, conn, addr)

    def interpret_message(self, data, sock, addr):

        if data['action'] == 'join':
            if data['player_id'] in self.game.players.keys():
                message = json.dumps({
                    "success": "True",
                    "message": "You have already registered!"
                })
                sock.send(message.encode())
            else:
                self.game.register_player(addr, data['player_id'])
                self.log.append((data['player_id'], 'join'))
                message = json.dumps(
                    {"success": "True", "message": "Player registered succesfully"})
                sock.send(message.encode())
        elif data['player_id'] not in self.game.players.keys():
            message = json.dumps(
                {"success": "True", "message": "Player not yet registered, register by using command 'join'"})
            sock.send(message.encode())
        elif data['action'] == 'play':
            not_played = self.game.recieve_play(data)
            if(not_played):
                self.log.append((data['player_id'], 'play', data['payload']))
                message = json.dumps(
                    {"success": "True", "message": "Play recieved succesfully"})
                sock.send(message.encode())
            else:
                self.log.append(
                    (data['player_id'], 'play', 'Already used turn in this round'))
                message = json.dumps(
                    {"success": "True", "message": "You have already used your turn in this round"})
                sock.send(message.encode())
        elif data['action'] == 'msg':
            for player in self.game.players.values():
                if player.player_id != data['player_id']:
                    player.send_message(data)

            self.log.append((data['player_id'], 'message', data['message']))
            message = json.dumps(
                {"success": "True", "message": "Message sent to other player"})
            sock.send(message.encode())
        elif data['action'] == 'pmsg':
            self.game.recieve_play(data)
            for player in self.game.players.values():
                if player.player_id != data['player_id']:
                    player.send_message(data)
            self.log.append(
                (data['player_id'], 'play and message', data['payload'], data['message']))
            message = json.dumps(
                {"success": "True", "message": "Play recieved and message sent to other player"})
            sock.send(message.encode())

    def print_logs(self):
        for entry in self.log:
            print(entry)


class Game():

    def __init__(self, GameServer):
        self.server = GameServer
        self.players = {}
        self.winners = []
        self.first_player_choice = None

    def register_player(self, addr, player_id):
        player = Player(addr, player_id)
        self.players[player_id] = player

    def send_game_status_to_players(self, winner_id):
        for player in self.players.values():
            if player.player_id != winner_id:
                msg = 'You lost, haha!' if winner_id else 'Tie game'
                player.send_message({
                    'player_id': player.player_id,
                    'message': msg
                })
            else:
                msg = 'You win, congratz!' if winner_id else 'Tie game'
                player.send_message({
                    'player_id': player.player_id,
                    'message': msg
                })

    def compare_results(self, first_player, second_player):
        print(self.players)
        self.server.print_logs()
        if (first_player['payload'] == '1' and second_player['payload'] == '2') or (first_player['payload'] == '2' and second_player['payload'] == '3') or (first_player['payload'] == '1' and second_player['payload'] == '3'):
            self.winners.append(second_player['player_id'])
            self.send_game_status_to_players(second_player['player_id'])

        elif (first_player['payload'] == '2' and second_player['payload'] == '1') or (first_player['payload'] == '3' and second_player['payload'] == '2') or (first_player['payload'] == '3' and second_player['payload'] == '1'):
            self.winners.append(first_player['player_id'])
            self.send_game_status_to_players(first_player['player_id'])
        else:
            self.send_game_status_to_players(None)

    def recieve_play(self, data):
        if(self.first_player_choice is not None and self.first_player_choice['player_id'] == data['player_id']):
            return None
        else:
            if(not self.first_player_choice):
                self.first_player_choice = data
            else:
                self.compare_results(self.first_player_choice, data)
                self.first_player_choice = None
            return True


class Player():

    def __init__(self, addr, udp_port):
        self.player_id = udp_port
        self.addr = addr
        self.udp_addr = (addr[0], int(udp_port))

    def send_message(self, data):
        sock = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
        sock.sendto(json.dumps(
            {data['player_id']: data['message']}).encode(), self.udp_addr)
        print('Message sent to clients')


if __name__ == '__main__':
    server_loop()
