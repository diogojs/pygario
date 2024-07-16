import socket
from typing import List, Tuple

from pygario.blob import Blob
from pygario.cell import Cell
from pygario.color import Color
from pygario.constants import AVAILABLE_COMMANDS, GRID_COLS, GRID_ROWS, GRID_SIZE, MAX_DATA_SIZE


class Client:
    """
    Class that handles the connection with the server,
    sends and receives information

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
    def __init__(self, host: str, port: int):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.addr = (host, port)
    
    def connect(self, name: str) -> bool:
        self.socket.connect(self.addr)
        name = name[:32].replace(';', '').replace(',', '')  # TODO: better sanitize/limit name characters
        self.socket.send(f"start;{name}".encode('utf-8'))
        id = int(self.socket.recv(MAX_DATA_SIZE))
        return id

    def get_data(self):
        # print('sending get_data')
        self.socket.send(b"get;")
        # print('getting response get_data')
        data = self.socket.recv(MAX_DATA_SIZE)
        # print(f"received response {data}")
        cmd, data = self.get_command_and_data(data)
        return cmd, data
    
    def send(self, data: bytes):
        # print(f"sending {data}")
        self.socket.send(data)
        # print(f"sent {data}")
        reply = self.socket.recv(MAX_DATA_SIZE)
        # print(f"received back {reply}")
        cmd, data = self.get_command_and_data(reply)
        return cmd, data

    def disconnect(self):
        self.socket.close()

    @staticmethod
    def get_command_and_data(data: bytes):
        cmd, *data_split = data.split(b';')
        cmd = cmd.decode('utf-8')

        if cmd not in AVAILABLE_COMMANDS:
            raise ValueError(f"Invalid command {cmd}")

        return cmd, data_split
    
    @staticmethod
    def deserialize(data: bytes):
        if len(data) != 1:
            raise RuntimeError("Unexpected data array with more than one item")

        data = data[0]
        player_blob, data = deserialize_blob(data)
        
        map_grid = []
        blobs_grid = []
        for i in range(GRID_COLS * GRID_ROWS):
            map_grid.append(list())
            blobs_grid.append(list())

        data = deserialize_cells(data, map_grid)
        data = deserialize_blobs(data, player_blob.id, blobs_grid)

        return player_blob, map_grid, blobs_grid


def deserialize_blob(data: bytes) -> Tuple[Blob, bytes]:
    from pygario.vector import Vector2D

    # data = {id,pos.x,pos.y,radius,R,G,B,name}
    id, data = get_int(data)
    pos_x, data = get_float(data)
    pos_y, data = get_float(data)
    radius, data = get_float(data)
    r, data = get_int(data)
    g, data = get_int(data)
    b, data = get_int(data)
    color = (r,g,b)
    name, data = get_str(data)
    return Blob(id, Vector2D(pos_x, pos_y), radius, color, name), data

def deserialize_cell(data: bytes) -> Tuple[Cell, bytes]:
    from pygario.vector import Vector2D

    # data = {id,pos.x,pos.y,radius}
    id, data = get_int(data)
    pos_x, data = get_float(data)
    pos_y, data = get_float(data)
    radius, data = get_float(data)
    r, g, b, data = get_color(data)
    return Cell(id, Vector2D(pos_x, pos_y), radius, (r, g, b)), data

def deserialize_cells(data: bytes, map_grid: List[List[Cell]]) -> bytes:
    assert data[0] == ord('['), f"Something wrong with received data for cells: {data}"
    data = data[1:]
    while data[0] != ord(']'):
        cell, data = deserialize_cell(data)
        grid_col = int(cell.pos.x // GRID_SIZE)
        grid_row = int(cell.pos.y // GRID_SIZE)
        map_grid[grid_col + grid_row * GRID_COLS].append(cell)
    
    data = data[2:]  # discard "],"
    return data

def deserialize_blobs(data: bytes, player_id: int, blobs_grid: List[List[Blob]]) -> bytes:
    assert data[0] == ord('['), f"Something wrong with received data for blobs: {data}"
    data = data[1:]
    while data[0] != ord(']'):
        blob, data = deserialize_blob(data)
        if blob.id == player_id:
            continue
        grid_col = int(blob.pos.x // GRID_SIZE)
        grid_row = int(blob.pos.y // GRID_SIZE)
        blobs_grid[grid_col + grid_row * GRID_COLS].append(blob)
    
    data = data[2:]  # discard "],"
    return data

def get_int(data: bytes) -> Tuple[int, bytes]:
    index = data.find(b',')
    value = data[:index]
    data = data[index+1:]
    return int(value), data

def get_str(data: bytes) -> Tuple[str, bytes]:
    index = data.find(b',')
    value = data[:index]
    data = data[index+1:]
    return value.decode(), data

def get_float(data: bytes) -> Tuple[float, bytes]:
    index = data.find(b',')
    value = data[:index]
    data = data[index+1:]
    return float(value), data

def get_color(data: bytes) -> Tuple[int, int, int, bytes]:
    r, data = get_int(data)
    g, data = get_int(data)
    b, data = get_int(data)
    return r, g, b, data