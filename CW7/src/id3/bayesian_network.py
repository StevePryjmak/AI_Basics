import json
import random
import pandas as pd
from collections import Counter
import itertools

def get_bayes_data(path):
    """Load Bayesian network data from a JSON file."""
    with open(path, 'r') as file:
        return json.load(file)

def generate_row(data):
    """Generate a single row of data based on the Bayesian network."""
    node_values = {}

    for node in data:
        node_id = node["id"]
        parents = node.get("parents", [])
        probabilities = node["probabilities"]

        if not parents:
            prob_true = probabilities["true"]
            node_values[node_id] = random.choices([True, False], [prob_true, 1 - prob_true])[0]
        else:
            parent_states = ''.join('T' if node_values[parent] else 'F' for parent in parents)
            prob_true = probabilities[parent_states]["true"]
            node_values[node_id] = random.choices([True, False], [prob_true, 1 - prob_true])[0]

    row_values = [node_values[node["id"]] for node in data]
    return row_values

def write_csv(data, num_samples, output_file):
    """Write generated data to a CSV file."""
    with open(output_file, 'w') as file:
        header = [node["id"] for node in data]
        file.write(','.join(header) + '\n')

        for _ in range(num_samples):
            row = generate_row(data)
            file.write(','.join(str(value) for value in row) + '\n')


def read_csv(input_file):
    """Read the CSV data into a DataFrame."""
    return pd.read_csv(input_file)


def calculate_joint_probability(combination, bayesian_data):
    """Calculate the joint probability of a given combination of node states."""
    joint_probability = 1.0

    # Map each node to its corresponding value (True/False) in the current combination
    node_values = {node["id"]: value for node, value in zip(bayesian_data, combination)}

    for node in bayesian_data:
        node_id = node["id"]
        parents = node.get("parents", [])
        probabilities = node["probabilities"]

        # If no parents, use the base probability
        if not parents:
            prob_true = probabilities["true"]
            prob_false = 1 - prob_true
            if node_values[node_id]:
                joint_probability *= prob_true
            else:
                joint_probability *= prob_false
        else:
            # For nodes with parents, calculate the conditional probability
            parent_states = ''.join('T' if node_values[parent] else 'F' for parent in parents)
            if parent_states in probabilities:
                prob_true = probabilities[parent_states]["true"]
                prob_false = 1 - prob_true
                if node_values[node_id]:
                    joint_probability *= prob_true
                else:
                    joint_probability *= prob_false
            else:
                # If we encounter an invalid parent state, we assume it is impossible (prob = 0)
                joint_probability = 0
                break

    return joint_probability

def calculate_all_combinations_probabilities(bayesian_data):
    """Calculate the joint probabilities for all possible combinations of node states."""
    num_nodes = len(bayesian_data)
    all_combinations = itertools.product([True, False], repeat=num_nodes)

    combination_probabilities = {}
    for combination in all_combinations:
        joint_prob = calculate_joint_probability(combination, bayesian_data)
        combination_probabilities[tuple(combination)] = joint_prob

    return combination_probabilities


def calculate_actual_counts(csv_file):
    """Calculate actual counts from the CSV file."""
    df = pd.read_csv(csv_file)
    actual_counts = Counter(tuple(row) for row in df.values)
    return actual_counts


def compare_counts(actual_counts, expected_counts):
    """Compare the actual and expected counts."""
    print(f"{'Combination':<30}{'Actual Count':<15}{'Expected Count':<15}")
    for combination in expected_counts: # actual_counts
        actual = actual_counts[combination]
        expected = expected_counts.get(combination, 0)
        print(f"{str(combination):<30}{actual:<15}{expected:<15.6f}")



def main():
    input_path = "probabilities.json"
    output_file = "generated_data.csv"
    num_samples = 10000

    bayesian_data = get_bayes_data(input_path)
    write_csv(bayesian_data, num_samples, output_file)
    expected_counts = calculate_all_combinations_probabilities(bayesian_data)
    expected_counts = {combination: count * num_samples for combination, count in expected_counts.items()}
    actual_counts = calculate_actual_counts(output_file)
    compare_counts(actual_counts, expected_counts)

if __name__ == '__main__':
    main()
