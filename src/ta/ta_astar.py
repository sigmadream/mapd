from heapq import *
from src.ta.ta_state import *
from src.ta.ta_world import MAP_NODE_TYPES


def get_heuristic(start_location, goal_location):
    return abs(start_location.col - goal_location.col) + abs(
        start_location.row - goal_location.row
    )


class AStar:
    def __init__(self, world):
        self.dim_x = world.width
        self.dim_y = world.height
        self.obstacles = {}
        self.other_agent_paths = []

    def state_possible(self, current_state, new_state):
        not_obstacle = False
        if (new_state.location.col, new_state.location.row) not in self.obstacles:
            not_obstacle = True
        return (
            0 <= new_state.location.col < self.dim_x
            and 0 <= new_state.location.row < self.dim_y
            and not_obstacle
            and not self.is_collision(current_state, new_state)
        )

    def is_collision(self, current_state, new_state):
        return False

    def get_neighbours(self, current_state):
        neighbours = []
        neighbour_time_step = current_state.time + 1
        new_state = State(
            neighbour_time_step,
            Location(current_state.location.col, current_state.location.row),
        )
        if self.state_possible(current_state, new_state):
            neighbours.append(new_state)
        new_state = State(
            neighbour_time_step,
            Location(current_state.location.col, current_state.location.row + 1),
        )
        if self.state_possible(current_state, new_state):
            neighbours.append(new_state)
        new_state = State(
            neighbour_time_step,
            Location(current_state.location.col, current_state.location.row - 1),
        )
        if self.state_possible(current_state, new_state):
            neighbours.append(new_state)
        new_state = State(
            neighbour_time_step,
            Location(current_state.location.col - 1, current_state.location.row),
        )
        if self.state_possible(current_state, new_state):
            neighbours.append(new_state)
        new_state = State(
            neighbour_time_step,
            Location(current_state.location.col + 1, current_state.location.row),
        )
        if self.state_possible(current_state, new_state):
            neighbours.append(new_state)
        return neighbours

    def create_obstacles(self, world, other_agent_paths, remaining_parking):
        for element in world:
            if world[element] == MAP_NODE_TYPES.WALL:
                self.obstacles[element] = True
        for location in remaining_parking:
            self.obstacles[location] = True
        self.other_agent_paths = other_agent_paths

    def search(
        self,
        time_step,
        start_location,
        goal_location,
        other_agent_paths,
        world,
        parking_locations,
        agent,
        release_time=0,
        find_step=0,
    ):
        self.create_obstacles(world, other_agent_paths, parking_locations)
        initial_state = State(time_step, start_location)
        came_from = {}
        open_list = [initial_state]
        closed_set = set()
        initial_state.g_score = 0
        initial_state.f_score = get_heuristic(start_location, goal_location)
        while open_list:
            current = heappop(open_list)
            if current.location == goal_location:
                if not current.time < release_time:
                    new_path = [current]
                    while current in came_from:
                        current = came_from[current]
                        new_path.append(current)
                    return new_path[::-1]
            closed_set |= {current}
            neighbours = self.get_neighbours(current)
            neighbour: State
            for neighbour in neighbours:
                if (neighbour not in closed_set) and (neighbour not in open_list):
                    came_from[neighbour] = current
                    neighbour.g = current.g + 1
                    neighbour.f = neighbour.g + get_heuristic(
                        neighbour.location, goal_location
                    )
                    heappush(open_list, neighbour)
        return False
