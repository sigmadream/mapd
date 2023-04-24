from mesa import Model
from mesa.space import MultiGrid
from mesa.datacollection import DataCollector
from .mesa_agents import Parking, Wall, Space, Robot
from src.ta.ta_world import MAP_NODE_TYPES
import src.mesa.mesa_scheduler as mesa_scheduler


class Warehouse(Model):
    def __init__(self, world, tsp_seqs, last_sim_step):
        self.schedule = mesa_scheduler.BaseScheduler(self)
        self.world = world
        self.tsp_seq = tsp_seqs
        self.last_sim_step = last_sim_step
        self.time_step = 0
        self.task_count = 0
        self.grid = MultiGrid(world.width, world.height, torus=False)
        self.data_collector = DataCollector({"task_count": "task_count"})
        self.robot_count = 0
        for element in world:
            if world[element] == MAP_NODE_TYPES.WALL:
                agent = Wall(element, self)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
            elif world[element] == MAP_NODE_TYPES.TASK_ENDPOINT:
                agent = Space(element, self)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
            elif world[element] == MAP_NODE_TYPES.PARKING:
                agent = Parking(element, self)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
                self.robot_count += 1
                agent = Robot(element, self, world.agents[self.robot_count].path)
                self.grid.place_agent(agent, element)
                self.schedule.add(agent)
        self.running = True

    def step(self):
        new_task_count = 0
        for seq_id in self.tsp_seq:
            if self.tsp_seq[seq_id].qsize() > 0:
                if self.time_step >= self.tsp_seq[seq_id].queue[0].release_time:
                    if self.time_step in self.world.agents[seq_id].path:
                        if (
                            self.tsp_seq[seq_id].queue[0].delivery_endpoint
                            == self.world.agents[seq_id].path[self.time_step]
                        ):
                            self.tsp_seq[seq_id].get()
            new_task_count += self.tsp_seq[seq_id].qsize()
        self.task_count = new_task_count
        if self.time_step >= self.last_sim_step:
            self.running = False
        self.time_step += 1
        self.schedule.step()
        self.data_collector.collect(self)
