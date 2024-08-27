import agentpy as ap
from model.agents import ObjectAgent, PileAgent, RobotAgent

class WarehouseModel(ap.Model):

    def setup(self):
        self.robots = ap.AgentList(self, self.p.R, RobotAgent)
        self.objects = ap.AgentList(self, self.p.K, ObjectAgent)
        self.piles = ap.AgentList(self, self.p.P, PileAgent)

        self.grid = ap.Grid(self, (self.p.M, self.p.N), track_empty=True)

        self.grid.add_agents(self.robots, random=True, empty=True)
        self.grid.add_agents(self.objects, random=True, empty=True)
        self.grid.add_agents(self.piles, random=True, empty=True)

    def step(self):
        self.robots.step()

    def update(self):
        pass

    def end(self):
        """Mostrar el estado final de las pilas al final de la simulación."""
        print("Estado final de las pilas:")
        for pile in self.piles:
            print(f"Pila en posición {self.grid.positions[pile]} tiene {pile.get_height()} cajas.")