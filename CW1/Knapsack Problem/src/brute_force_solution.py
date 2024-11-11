import numpy as np


def knapsack_bruteforce(weights, max_weight, prices):

    best_price = 0
    best_combination = None
    selected_items = []

    length = len(weights)
    for i in range(pow(2, length)):
        current_weight = 0
        current_price = 0
        temp_selected_items = []
        combination = i

        for j in range(length):
            if combination == 0:
                break
            if combination % 2 == 1:
                current_weight += weights[j]
                current_price += prices[j]
                temp_selected_items.append([int(weights[j]), int(prices[j])])
            combination >>= 1

        if current_price > best_price and current_weight <= max_weight:
            best_price = current_price
            best_combination = i
            selected_items = temp_selected_items
    return best_price, selected_items, best_combination


if __name__ == '__main__':
    item_weights = np.array([8, 3, 5, 2])
    item_prices = np.array([16, 8, 9, 6])
    price, items, _ = knapsack_bruteforce(item_weights, np.sum(item_weights) / 2, item_prices)

    print(f"Best value: {price}")
    print(f"Best combination of items: {items}")
