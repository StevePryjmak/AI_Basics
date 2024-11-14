from constants import *
from representant import Representant
import numpy as np


class Population:
    def __init__ (self, size, func):
        self.size = size
        self.func = func
        self.representants = [Representant(np.random.uniform(-UPPER_BOUND, UPPER_BOUND, DIMENSIONALITY), func) for _ in range(size)]

    def get_best(self):
        best = self.representants[0]
        for rep in self.representants:
            if rep.get_evaluation() < best.get_evaluation():
                best = rep
        return best
    
    def evolve(self, sigma=SIGMA):
        new_population = []
        for _ in range(self.size):
            tournament = np.random.choice(self.representants, 2, replace=False)
            best = min(tournament, key=lambda rep: rep.get_evaluation())
            new_population.append(best.get_mutation(sigma))
        self.representants = new_population
    
    def get_points(self):
        return [rep.get_position() for rep in self.representants]

    def get_values(self):
        return [rep.get_evaluation() for rep in self.representants]