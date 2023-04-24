from enum import Enum
from .ta_agent import *
from .ta_state import *


class MAP_NODE_TYPES(Enum):
    PARKING = 0
    PATH = 1
    WALL = 2
    TASK_ENDPOINT = 3


class World(dict):
    def __init__(self, world_file_path, max_path_time):
        self.agents = dict()
        self.endpoints = dict()
        self.parking_locations = dict()
        self.width = 0
        self.height = 0
        self.load_file(world_file_path, max_path_time)

    def load_file(self, world_file_path, max_path_time):
        file = open(world_file_path, "r")
        if not file.mode == "r":
            print("Could not open " + world_file_path)
        else:
            print("Loading map file")
            world_data = file.readlines()
            col = 0
            row = 0
            parking_count = 0
            endpoint_count = 0
            for line in world_data:
                col = 0
                for char in line:
                    node = None
                    if char == ".":
                        node = MAP_NODE_TYPES.PATH
                    elif char == "r":
                        node = MAP_NODE_TYPES.PARKING
                        parking_count += 1
                        self.agents[parking_count] = Agent(
                            parking_count, Location(col, row), max_path_time
                        )
                        self.agents[parking_count].path[0] = Location(col, row)
                        self.parking_locations[parking_count] = Location(col, row)
                    elif char == "@":
                        node = MAP_NODE_TYPES.WALL
                    elif char == "e":
                        node = MAP_NODE_TYPES.TASK_ENDPOINT
                        self.endpoints[endpoint_count] = Location(col, row)
                        endpoint_count += 1
                    if node is not None:
                        self[col, row] = node
                    col += 1
                row += 1
        self.width = col
        self.height = row
        file.close()
