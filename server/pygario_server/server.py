import socket
import pickle
from time import sleep
from typing import Dict, Iterable, List, Tuple
from random import randint
from _thread import start_new_thread

from pygario_server.blob import Blob
from pygario_server.cell import Cell
from pygario_server.color import Color
from pygario_server.constants import *
from pygario_server.vector import Vector2D

class Server:
    _LAST_ID = 0

    def __init__(self):
        self.socket: socket.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host_name = socket.gethostname()
        self.ip = socket.gethostbyname(self.host_name)
        self.port = PORT

    def run(self):
        try:
            self.socket.bind((self.ip, self.port))
        except socket.error as e:
            print("Server could not start")
            print(str(e))
            return
        
        self.socket.listen()
        print(f"Server listening on local IP {self.ip} PORT {self.port}")

        self.players: Dict[int, Blob] = dict()
        self.cells: Dict[int, Cell] = dict()
        self.eaten_players = list()

        self.initialize_map()

        is_running = True
        self.active_players = 0
        while is_running:
            if self.active_players < PLAYER_LIMIT:
                # keep accepting new connections
                connection, addr = self.socket.accept()
                print(f"[Socket] received connection from {addr}")

                self.active_players += 1
                start_new_thread(self.threaded_client, (connection, self.get_new_id()))

    def threaded_client(self, conn: socket.socket, id: int) -> None:
        """
        protocol:
        - after connection is acquired, client should send 'start'
        client messages:
        - 'start': {name: str}
        - 'move': {x: float, y: float, velocity: vector2d}
        - 'eat': {other_id: int, x: float, y: float, velocity: vector2d} 
        - 'disconnect'

        server messages:
        - 'update': {own_player: Blob, cells: List[Cell], players: List[Blob]}
        - 'kick': {reason: str}
        - 'error': {msg: str}
        """
        # handle start and create player
        data = conn.recv(MAX_RECV_DATA_SIZE)
        cmd, data = self.get_command_and_data(data)
        if cmd != 'start':
            conn.send(b'error;First message should be "start".')

        name = data[0].decode('utf-8')
        print(f"[ThreadedClient] {name} connected to the server.")

        initial_pos = self.get_start_position()
        color = Color.get_random()
        player = Blob(id, initial_pos, INITIAL_RADIUS, color, name)
        self.players[id] = player
        conn.send(str(id).encode())

        connected = True
        while connected:
            # first thing is to check if players still exists (if not, it was killed)
            if id not in self.players:
                connected = False
                if id in self.eaten_players:
                    back_data = f"kick;You were eaten."
                    conn.send(back_data.encode())
                    self.eaten_players.remove(id)
                break
            try:
                data = conn.recv(MAX_RECV_DATA_SIZE)
                cmd, data = self.get_command_and_data(data)
                data = data[0]

                if cmd == "move":
                    # data = {x: float, y: float, velocity: vector2d}
                    # TODO: validate motion velocity and new position
                    x, data = get_float(data)
                    y, data = get_float(data)
                    self.move_player(id, x, y)
                    self.send_all_data_to(conn, player)

                elif cmd == "eat":
                    # data = {x: float, y: float, radius: float, velocity: vector2d, other_id: int} 
                    # TODO: check if collision really happen and eating was valid
                    x, data = get_float(data)
                    y, data = get_float(data)
                    radius, data = get_float(data)
                    while data:
                        other_id, data = get_int(data)
                        removed = False
                        if other_id in self.players:
                            removed = True
                            self.eaten_players.append(other_id)
                            del self.players[other_id]
                        elif other_id in self.cells:
                            removed = True
                            del self.cells[other_id]
                    
                    self.move_player(id, x, y, radius)
                    
                    back_data = f"ok;{removed}"
                    conn.send(back_data.encode())

                elif cmd == "get":
                    self.send_all_data_to(conn, player)

                elif cmd == "disconnect":
                    connected = False
                    break

                sleep(0.005)
            except ValueError as e:
                print(e)
                connected = False
            except ConnectionResetError as e:
                connected = False

        print(f"[ThreadedClient] {name} disconnected.")
        self.active_players -= 1
        if id in self.players:
            del self.players[id]
        conn.close()
    
    def send_all_data_to(self, conn: socket.socket, player: Blob):
        # send back all player and map info
        # all_data = pickle.dumps((player, list(self.cells.values()), list(self.players.values())))
        all_data = Server.serialize((player, self.cells.values(), self.players.values()))
        all_data = b'update;' + all_data
        conn.send(all_data)
    
    def move_player(self, id: int, x: float, y: float, radius: float = -1):
        self.players[id].pos = Vector2D(x, y)
        if radius > 0:
            self.players[id].radius = radius

    @staticmethod
    def get_command_and_data(data: bytes):
        cmd, *data_split = data.split(b';')
        cmd = cmd.decode('utf-8')

        if cmd not in AVAILABLE_COMMANDS:
            raise ValueError(f"Invalid command {cmd}")

        return cmd, data_split

    def initialize_map(self) -> None:
        print("Initializing map")
        self.create_cells(NUMBER_OF_CELLS)
    
    def create_cells(self, number: int) -> None:
        for i in range(number):
            p = Vector2D(randint(1, MAP_WIDTH-2), randint(1, MAP_HEIGHT-2))
            r, g, b = randint(0, 6)*40, randint(0, 6)*40, randint(0, 6)*40
            new_cell = Cell(self.get_new_id(), p, CELL_RADIUS, (r, g, b))
            self.cells[new_cell.id] = new_cell
    
    def get_start_position(self) -> Vector2D:
        """
        Pick a random position to spawn a player, ensuring it is not inside
        another player
        """
        while True:
            pos = Vector2D(randint(INITIAL_RADIUS, MAP_WIDTH-INITIAL_RADIUS), randint(INITIAL_RADIUS, MAP_HEIGHT-INITIAL_RADIUS))
            new_blob = Blob(-1, pos, INITIAL_RADIUS, "", (0,0,0))
            
            for player in self.players.values():
                if player.check_collision(new_blob, INITIAL_RADIUS):
                    break
            else:
                return pos


    @classmethod
    def get_new_id(cls) -> int:
        cls._LAST_ID += 1
        return cls._LAST_ID
    
    @staticmethod
    def serialize(items: Iterable) -> bytes:
        result = b''
        for item in items:
            if isinstance(item, Iterable):
                item = list(item)
                result += b'['
                result += Server.serialize(item)
                result += b'],'
            else:
                result += item.serialize() + b','
        return result

def get_int(data: bytes) -> Tuple[int, bytes]:
    index = data.find(b',')
    value = data[:index]
    data = data[index+1:]
    return int(value), data

def get_float(data: bytes) -> Tuple[float, bytes]:
    index = data.find(b',')
    value = data[:index]
    data = data[index+1:]
    return float(value), data