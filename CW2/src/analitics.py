from population import Population
import matplotlib.pyplot as plt
from save import save
from constants import *

def main():
    path = '../resources/values'
    population = Population(POPULATION_SIZE, FUNKTION)
    generations = []
    all_values = []

    for gen in range(int(MAX_EVALUATIONS / POPULATION_SIZE)):
        population.evolve()
        generations.append(gen + 1)
        all_values.append(population.get_values())

    all_values_flat = [value for generation_values in all_values for value in generation_values]
    generation_labels = [gen for gen in generations for _ in range(POPULATION_SIZE)]


    plt.figure(figsize=(10, 12))
    plt.scatter(generation_labels, all_values_flat, alpha=0.5, s=5)
    
    plt.ylim(0, 20000)
    plt.xlabel('Generation')
    plt.ylabel('Evaluation Value')
    plt.title('Evaluation Values of All Points Over Generations')
    save(path)
    plt.show()


if __name__ == "__main__":
    main()