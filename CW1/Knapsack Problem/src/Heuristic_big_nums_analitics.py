import numpy as np
import time
import matplotlib.pyplot as plt
from heuristic_solution import create_objects, knapsack_heuristic
import gc


def compare_performance(iterator):
    heuristic_times = []
    heuristic_prices = []
    heuristic_masses = []
    max_masses = []

    for num_items in iterator:
        weights = np.random.randint(1, 100, num_items)
        prices = np.random.randint(1, 200, num_items)
        max_mass = np.sum(weights) / 2

        gc.disable()
        items = create_objects(weights, prices)
        start_time = time.time()
        heuristic_items, heuristic_mass, heuristic_price = knapsack_heuristic(items, max_mass)
        heuristic_times.append(time.time() - start_time)

        gc.enable()

        heuristic_prices.append(heuristic_price)
        heuristic_masses.append(heuristic_mass)
        max_masses.append(max_mass)

    return heuristic_times, heuristic_prices, heuristic_masses, max_masses

def plot_time_and_price(iterator, times, prices, label, color='b'):
    plt.subplot(1, 2, 1)
    plt.plot(iterator, times, label=f'{label} Time', color=color)
    plt.xlabel("Number of Items")
    plt.ylabel("Time (seconds)")
    plt.title("Execution Time")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(iterator, prices, label=f'{label} Price', color=color)
    plt.xlabel("Number of Items")
    plt.ylabel("Total Price")
    plt.title("Heuristic Total Price")
    plt.legend()

def plot_masses(iterator, masses, max_masses):
    plt.plot(iterator, masses, label="Heuristic Mass", color='r')
    plt.plot(iterator, max_masses, label="Max Mass", linestyle='--', color='g')
    plt.xlabel("Number of Items")
    plt.ylabel("Mass")
    plt.title("Heuristic Mass vs Max Mass")
    plt.legend()


if __name__ == '__main__':
    num_items_list = [_ for _ in range(4, 100000, 1000)]
    heur_time, heur_price, heur_mass, max_mass = compare_performance(num_items_list)


    plt.figure(figsize=(10, 5))
    plot_time_and_price(num_items_list, heur_time, heur_price, "Heuristic")
    plt.tight_layout()
    plt.savefig('../resources/Heuristic_Price_Time.png')
    plt.show()


    plt.figure(figsize=(7, 5))
    plot_masses(num_items_list, heur_mass, max_mass)
    plt.tight_layout()
    plt.savefig('../resources/Heuristic_Masses.png')
    plt.show()
