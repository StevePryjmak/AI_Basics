import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from id3 import id3
from bayesian_network import generate_row, get_bayes_data, write_csv  # Assuming your Bayesian network functions are in a module


def preprocess_data(data, class_column, random_state=50, sample_size=None, attribute_subset=None):
    """Preprocess data for ID3 training."""
    data = data.fillna('?')

    if sample_size is not None:
        data = data.sample(n=sample_size, random_state=random_state)

    y = data[class_column]
    X = data.drop(columns=[class_column])

    if attribute_subset is not None:
        if attribute_subset > X.shape[1]:
            attribute_subset = X.shape[1]
        X = X.sample(n=attribute_subset, axis=1, random_state=random_state)

    return train_test_split(X, y, test_size=0.4, random_state=random_state)


def predict(tree, sample):
    """Recursively predict the label using the decision tree."""
    if tree.result is not None:
        return tree.result

    attribute_value = sample.get(tree.attribute)
    child_node = tree.children.get(attribute_value)

    if child_node is None:
        return None

    return predict(child_node, sample)


def evaluate(tree, features, labels):
    """Evaluate the decision tree on the test set."""
    predictions = features.apply(lambda row: predict(tree, row), axis=1)
    accuracy = (predictions == labels).mean()

    conf_matrix = pd.crosstab(labels, predictions, rownames=['Actual'], colnames=['Predicted'], dropna=False)

    return accuracy, conf_matrix


def get_result(data, class_column, random_state=50):
    """Train and evaluate the ID3 tree using the given data."""
    train_attributes, test_attributes, train_labels, test_labels = preprocess_data(data, class_column, random_state)
    tree = id3(train_attributes, train_labels)
    accuracy, conf_matrix = evaluate(tree, test_attributes, test_labels)
    return accuracy, conf_matrix


def main():
    bayesian_data = get_bayes_data("probabilities.json")
    num_samples = 50000
    # output_file = "generated_data.csv"
    output_file = "output.csv"
    # write_csv(bayesian_data, num_samples, output_file)
    generated_data = pd.read_csv(output_file)

    class_column = generated_data.columns[-1]

    accuracies = []
    conf_matrices = []

    for _ in range(100):
        random_state = np.random.randint(0, 1000)
        acc, conf_matrix = get_result(generated_data, class_column, random_state)
        accuracies.append(acc)
        conf_matrices.append(conf_matrix)

    avg_acc = np.mean(accuracies)
    min_acc = np.min(accuracies)
    max_acc = np.max(accuracies)
    std_acc = np.std(accuracies)
    avg_conf_matrix = sum(conf_matrices) / len(conf_matrices)

    print("Generated Data Average Accuracy:", avg_acc)
    print("Generated Data Min Accuracy:", min_acc)
    print("Generated Data Max Accuracy:", max_acc)
    print("Generated Data Std Accuracy:", std_acc)
    print("Generated Data Average Confusion Matrix:\n", avg_conf_matrix)


if __name__ == "__main__":
    main()
