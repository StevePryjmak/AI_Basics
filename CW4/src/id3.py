import numpy as np 
from node import Node

def entropy(class_labels):
    _, counts = np.unique(class_labels, return_counts=True)
    probabilities = counts / len(class_labels)
    # print(f"Val {_} count {counts} prob {probabilities}")
    # print(f"Entropy: {np.sum(probabilities * np.log2(probabilities))}")
    return -np.sum(probabilities * np.log2(probabilities))


def information_gain(atributes, lables, attribute):
    base_entropy = entropy(lables)
    values = atributes[attribute].unique()
    weighted_entropy = sum(
        (atributes[attribute] == value).sum() / len(atributes) * entropy(lables[atributes[attribute] == value])
        for value in values
    )
    return base_entropy - weighted_entropy

def id3(atributes, lables, used_attributes=None):
    if len(np.unique(lables)) == 1:
        return Node(result=lables.values[0])

    
    if used_attributes is None:
        used_attributes = set()
    if len(used_attributes) == len(atributes.columns):
        return Node(result=lables.mode()[0])

    remaining_attributes = [col for col in atributes.columns if col not in used_attributes]
    if not remaining_attributes:
        return Node(result=lables.mode()[0])

    best_attribute = max(remaining_attributes, key=lambda col: information_gain(atributes, lables, col))


    root = Node(attribute=best_attribute)
    used_attributes = used_attributes.copy()
    used_attributes.add(best_attribute)

    for value in atributes[best_attribute].unique():
        subset_X = atributes[atributes[best_attribute] == value]
        subset_y = lables[atributes[best_attribute] == value]
        if subset_X.empty or subset_y.empty:
            root.children[value] = Node(result=lables.mode()[0])
        else:
            root.children[value] = id3(subset_X, subset_y, used_attributes)

    return root