import numpy as np


class Item:
    def __init__(self, mass, price):
        if mass <= 0:
            raise ValueError("Mass must be positive.")
        if price < 0:
            raise ValueError("Price cannot be negative.")

        self._mass = mass
        self._price = price
        self._ratio = price / mass

    def __str__(self):
        return f"mass={self._mass}, price={self._price}, ratio={self._ratio:.2f}"

    def get_mass(self):
        return self._mass

    def get_price(self):
        return self._price

    def get_ratio(self):
        return self._ratio


def create_objects(weights: np.array, prices: np.array) -> np.array:
    return np.array([Item(weights[_], prices[_]) for _ in range(len(weights))])


def knapsack_heuristic(items, max_mass):
    items = np.array(sorted(items, key=lambda _: _.get_ratio(), reverse=True))
    curr_mass = 0
    curr_price = 0
    selected_items = []
    for item in items:
        if curr_mass+item.get_mass() > max_mass:
            continue
        curr_mass += item.get_mass()
        curr_price += item.get_price()
        selected_items.append(item)

    return selected_items, curr_mass, curr_price


if __name__ == "__main__":
    item_weights = np.array([8, 3, 5, 2])
    item_prices = np.array([16, 8, 9, 6])

    items_obj = create_objects(item_weights, item_prices)

    mass_limit = np.sum(item_weights) / 2
    ans, total_mass, total_price = knapsack_heuristic(items_obj, mass_limit)

    print(f"Max mass allowed: {mass_limit}")
    print(f"Total mass of selected items: {total_mass}")
    print(f"Total price of selected items: {total_price}")
    print("Selected items:")
    for i in ans:
        print(i)
