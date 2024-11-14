from population import Population
from constants import *

def main():
    population = Population(POPULATION_SIZE, FUNKTION)

    for gen in range(int(MAX_EVALUATIONS/POPULATION_SIZE)):
        population.evolve()
        print(f"Generation {gen+1}: {population.get_best().get_evaluation()}")

if __name__ == "__main__":
    main()