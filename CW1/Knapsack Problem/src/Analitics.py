import numpy as np
import time
import matplotlib.pyplot as plt
from brute_force_solution import knapsack_bruteforce
from heuristic_solution import create_objects, knapsack_heuristic
import os
import gc


def write_to_file(filename, num_items, weights, prices, max_mass, brute_force_price, brute_force_items,
                  heuristic_price, heuristic_items):
    delta_percentage = (abs(brute_force_price - heuristic_price) / brute_force_price) * 100 \
        if brute_force_price != 0 else 0
    with open(filename, 'a') as file:
        file.write(f"N = {num_items}\n")
        file.write(f"W = {weights}\n")
        file.write(f"P = {prices}\n")
        file.write(f"MAX = {max_mass:.1f}\n")
        file.write("Heuristic answer:\n")
        file.write(f"    Masses: {[int(item.get_mass()) for item in heuristic_items]}\n")
        file.write(f"    Prices: {[int(item.get_price()) for item in heuristic_items]}\n")
        file.write("Brute Force answer:\n")
        file.write(f"    Masses: {[item[0] for item in brute_force_items]}\n")
        file.write(f"    Prices: {[item[1] for item in brute_force_items]}\n")
        file.write(f"Delta = {abs(brute_force_price - heuristic_price)}\n")
        file.write(f"Error Percentage = {delta_percentage:.2f}%\n\n")
        file.write("\n")


def compare_performance(iterator, filename):
    brute_force_times = []
    heuristic_times = []
    brute_force_prices = []
    heuristic_prices = []

    for num_items in iterator:
        weights = np.random.randint(50, 100, num_items)
        prices = np.random.randint(50, 200, num_items)
        max_mass = np.sum(weights) / 2

        gc.disable()
        start_time = time.time()
        brute_force_price, brute_force_items, _ = knapsack_bruteforce(weights, max_mass, prices)
        brute_force_times.append(time.time() - start_time)
        brute_force_prices.append(brute_force_price)

        items = create_objects(weights, prices)
        start_time = time.time()
        heuristic_items, heuristic_mass, heuristic_price = knapsack_heuristic(items, max_mass)
        heuristic_times.append(time.time() - start_time)
        heuristic_prices.append(heuristic_price)
        gc.enable()

        write_to_file(filename, num_items, weights, prices, max_mass, brute_force_price, brute_force_items,
                      heuristic_price, heuristic_items)

    return brute_force_times, heuristic_times, brute_force_prices, heuristic_prices


def plot_results(iterator, times, prices, label, color='r'):

    plt.subplot(1, 2, 1)
    plt.plot(iterator, times, label=label, color=color)
    plt.xlabel("Number of Items")
    plt.ylabel("Time (seconds)")
    plt.title("Execution Time Comparison")
    plt.legend()

    plt.subplot(1, 2, 2)
    plt.plot(iterator, prices, label=label, color=color)
    plt.xlabel("Number of Items")
    plt.ylabel("Total Price")
    plt.title("Total Price Comparison")
    plt.legend()


if __name__ == '__main__':
    num_items_list = [4, 5, 6, 7, 8, 9, 10, 11, 12, 13, 14, 15, 16, 17, 18]
    #[4, 6, 8, 10, 12, 14, 16, 18, 20, 22]
    output_file = '../resources/feedback_data.txt'
    os.makedirs(os.path.dirname(output_file), exist_ok=True)
    with open(output_file, 'w') as f:
        f.write("")

    bf_time, heur_time, bf_price, heur_price = compare_performance(num_items_list, output_file)
    #plot_results(num_items_list, *compare_performance(num_items_list, output_file))

    plt.figure(figsize=(10, 5))
    plot_results(num_items_list, bf_time, bf_price, "Brute Force")
    plt.savefig('../resources/BruteForce.png')

    plt.figure(figsize=(10, 5))
    plot_results(num_items_list, heur_time, heur_price, "Heuristic", 'b')
    plt.savefig('../resources/Heuristic.png')
    plot_results(num_items_list, bf_time, bf_price, "Brute Force")
    # plt.tight_layout()
    plt.savefig('../resources/Both.png')
    plt.show()


