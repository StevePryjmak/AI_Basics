from constants import SIGMA, DIMENSIONALITY, UPPER_BOUND
import numpy as np

class Representant:
    def __init__(self, position, func):
        self.funktor = func
        self.position = position
        self.value = func(self.position)

    def get_mutation(self, sigma=SIGMA, dimensionality=DIMENSIONALITY, upper_bound=UPPER_BOUND):
        mutation_vector = np.random.normal(0, sigma, dimensionality)
        new_position = self.position + mutation_vector
        new_position = np.clip(new_position, -upper_bound, upper_bound)
        return Representant(new_position, self.funktor)
    
    def get_position(self):
        return self.position

    def get_evaluation(self):
        return self.value