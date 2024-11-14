import numpy as np
from population import Population
from constants import POPULATION_SIZE, MAX_EVALUATIONS, FUNKTION

NUM_RUNS = 25

def calculate_statistics(results):
    avarage_result = np.mean(results)
    stddev_result = np.std(results)
    best_result = np.min(results)
    worst_result = np.max(results)
    return avarage_result, stddev_result, best_result, worst_result

def run_experiment(population_size, max_evaluations, func, sigma):
    results = []
    for _ in range(NUM_RUNS):
        population = Population(population_size, func)
        best = population.get_best()
        for gen in range(int(max_evaluations / population_size)):
            population.evolve(sigma)
            if population.get_best().get_evaluation() < best.get_evaluation():
                best = population.get_best()
        results.append(best.get_evaluation())
        #results.append(population.get_best().get_evaluation())
    
    avarage_value, stddev, best, worst = calculate_statistics(results)
    return avarage_value, stddev, best, worst

def main():
    population_sizes = [128]
    mutation_strengths = [0.5] 

    # population_sizes = [4, 8, 16, 32, 64]
    # mutation_strengths = [0.5]

    for pop_size in population_sizes:
        for sigma in mutation_strengths:
            average_value, stddev, best, worst = run_experiment(pop_size, MAX_EVALUATIONS, FUNKTION, sigma)
            print(f"Population Size: {pop_size}, Mutation Strength: {sigma}")
            print(f"Avarage: {average_value}, Best: {best}, Worst: {worst}, Std Dev: {stddev}")
            print("-" * 50)

if __name__ == "__main__":
    main()
