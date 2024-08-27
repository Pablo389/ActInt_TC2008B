import agentpy as ap
from model.agents import ObjectAgent, PileAgent, RobotAgent
import numpy as np

class WarehouseModel(ap.Model):

    def setup(self):
        self.robots = ap.AgentList(self, self.p.R, RobotAgent)
        self.objects = ap.AgentList(self, self.p.K, ObjectAgent)
        self.piles = ap.AgentList(self, self.p.P, PileAgent)

        self.grid = ap.Grid(self, (self.p.M, self.p.N), track_empty=True)

        self.grid.add_agents(self.robots, random=True, empty=True)
        self.grid.add_agents(self.objects, random=True, empty=True)
        self.grid.add_agents(self.piles, random=True, empty=True)

        self.print_grid()

    def step(self):
        self.robots.step()
        self.t += 1

    def update(self):
        pass

    def end(self):
        """Mostrar el estado final de las pilas al final de la simulación."""
        print("Estado final de las pilas:")
        for pile in self.piles:
            print(f"Pila en posición {self.grid.positions[pile]} tiene {pile.get_height()} cajas.")
    
    def print_grid(self):
        "Impresión de la cuadrícula en consola"
        grid_matrix = np.full((self.p.M, self.p.N), '.', dtype=str)
        
        for agent in self.robots:
            x, y = self.grid.positions[agent]
            grid_matrix[x, y] = 'R' if not agent.carrying_object else 'r'
        
        for agent in self.objects:
            if agent in self.grid.positions:
                x, y = self.grid.positions[agent]
                grid_matrix[x, y] = 'O'
        
        for agent in self.piles:
            x, y = self.grid.positions[agent]
            grid_matrix[x, y] = 'P'
        
        print(f"Step: {self.t}")
        for row in grid_matrix:
            print(' '.join(row))
        print()