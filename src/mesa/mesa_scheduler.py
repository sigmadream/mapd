from collections import OrderedDict, defaultdict

from typing import Dict, Iterator, List, Optional, Union, Type
from mesa.agent import Agent
from mesa.model import Model

TimeT = Union[float, int]


class BaseScheduler:
    def __init__(self, model: Model) -> None:
        self.model = model
        self.steps = 0
        self.time: TimeT = 0
        self._agents: Dict[int, Agent] = OrderedDict()

    def add(self, agent: Agent) -> None:
        self._agents[agent.unique_id] = agent

    def remove(self, agent: Agent) -> None:
        del self._agents[agent.unique_id]

    def step(self) -> None:
        for agent in self.agent_buffer(shuffled=False):
            agent.step()
        self.steps += 1
        self.time += 1

    def get_agent_count(self) -> int:
        return len(self._agents.keys())

    @property
    def agents(self) -> List[Agent]:
        return list(self._agents.values())

    def agent_buffer(self, shuffled: bool = False) -> Iterator[Agent]:
        agent_keys = list(self._agents.keys())
        if shuffled:
            self.model.random.shuffle(agent_keys)

        for key in agent_keys:
            if key in self._agents:
                yield self._agents[key]
