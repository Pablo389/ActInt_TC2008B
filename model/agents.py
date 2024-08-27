import agentpy as ap
import random

class ObjectAgent(ap.Agent):
    def setup(self):
        self.agentType = 2  # 2 for objects (boxes)
        self.pos = None

class PileAgent(ap.Agent):
    def setup(self):
        self.agentType = 3  # 3 for piles
        self.height = 0

    def add(self):
        self.height += 1

    def get_height(self):
        """Obtener la altura actual de la pila."""
        return self.height
    
class RobotAgent(ap.Agent):

    def setup(self):
        self.agentType = 1  # 1 for robots
        self.carrying_object = None

    def see(self):
        """Detect surroundings and store the location of nearby objects, piles, and robots."""
        self.perception = {
            'objects': [],
            'piles': [],
            'robots': []
        }
        neighbors = self.model.grid.neighbors(self)
        for neighbor in neighbors:
            if isinstance(neighbor, ObjectAgent):
                self.perception['objects'].append(neighbor)
            elif isinstance(neighbor, PileAgent):
                self.perception['piles'].append(neighbor)
            elif isinstance(neighbor, RobotAgent):
                self.perception['robots'].append(neighbor)

    def is_position_valid(self, position):
        """Check if a position is valid based on the current robot state."""
        if not (0 <= position[0] < self.model.p.M and 0 <= position[1] < self.model.p.N):
            return False  # Position is outside the grid

        agents_at_pos = self.model.grid.agents[position]

        # Avoid spaces occupied by other robots
        if any(isinstance(agent, RobotAgent) for agent in agents_at_pos):
            return False

        # If carrying an object, avoid spaces with other boxes
        if self.carrying_object and any(isinstance(agent, ObjectAgent) for agent in agents_at_pos):
            return False

        # Avoid spaces with piles
        if any(isinstance(agent, PileAgent) for agent in agents_at_pos):
            return False

        return True

    def pick(self):
        """Pick up an object if available at the current position."""
        if not self.carrying_object:
            objects_at_pos = [agent for agent in self.model.grid.agents[self.model.grid.positions[self]] if isinstance(agent, ObjectAgent)]
            if objects_at_pos:
                self.carrying_object = objects_at_pos[0]
                self.model.grid.remove_agents(self.carrying_object)

    def drop(self):
        """Drop the carried object in front of a pile if the pile is not full."""
        if self.carrying_object:
            available_piles = [pile for pile in self.perception['piles'] if pile.get_height() < 5]
            if available_piles:
                target_pile = available_piles[0]
                my_pos = self.model.grid.positions[self]
                pile_pos = self.model.grid.positions[target_pile]
                if abs(my_pos[0] - pile_pos[0]) + abs(my_pos[1] - pile_pos[1]) == 1:  # Adjacent to the pile
                    target_pile.add()
                    self.carrying_object = None
                else:
                    self.move_towards(target_pile)
            else:
                self.move_random()

    def move_towards(self, target):
        """Move towards the target position (north, south, east, or west) only if valid."""
        target_pos = self.model.grid.positions[target]
        my_pos = self.model.grid.positions[self]

        possible_moves = []

        if target_pos[0] < my_pos[0] and self.is_position_valid((my_pos[0] - 1, my_pos[1])):
            possible_moves.append((-1, 0))
        elif target_pos[0] > my_pos[0] and self.is_position_valid((my_pos[0] + 1, my_pos[1])):
            possible_moves.append((1, 0))
        if target_pos[1] < my_pos[1] and self.is_position_valid((my_pos[0], my_pos[1] - 1)):
            possible_moves.append((0, -1))
        elif target_pos[1] > my_pos[1] and self.is_position_valid((my_pos[0], my_pos[1] + 1)):
            possible_moves.append((0, 1))

        if possible_moves:
            self.model.grid.move_by(self, random.choice(possible_moves))

    def move_random(self):
        """Move in a random valid direction."""
        my_pos = self.model.grid.positions[self]
        directions = [(0, 1), (1, 0), (0, -1), (-1, 0)]
        random.shuffle(directions)
        for direction in directions:
            new_pos = (my_pos[0] + direction[0], my_pos[1] + direction[1])
            if self.is_position_valid(new_pos):
                self.model.grid.move_by(self, direction)
                break

    def step(self):
        """Define the robot's behavior at each step."""
        self.see()
        if self.carrying_object:
            self.drop()
        else:
            if self.perception['objects']:
                self.move_towards(self.perception['objects'][0])
                self.pick()
            else:
                self.move_random()