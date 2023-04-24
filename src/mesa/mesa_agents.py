from mesa import Agent


class Robot(Agent):
    def __init__(self, pos, model, path):
        super().__init__(pos, model)
        self.pos = pos
        self.path = path

    def step(self):
        if self.model.time_step in self.path:
            self.model.grid.remove_agent(self)
            self.pos = (
                (self.path[self.model.time_step]).col,
                (self.path[self.model.time_step]).row,
            )
            self.model.grid.place_agent(self, self.pos)


class Wall(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos


class Parking(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos


class Space(Agent):
    def __init__(self, pos, model):
        super().__init__(pos, model)
        self.pos = pos
