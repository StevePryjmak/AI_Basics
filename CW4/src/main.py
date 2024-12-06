import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from id3 import id3


def preprocess_data(file_path, class_column, random_state=50, sample_size=None, attribute_subset=None):
    data = pd.read_csv(file_path)
    data = data.fillna('?')
    
    if sample_size is not None:
        data = data.sample(n=sample_size, random_state=random_state)
    
    y = data[class_column]
    X = data.drop(columns=[class_column])
    
    # if attribute_subset is not None:
    #     X = X[attribute_subset]
    if attribute_subset is not None:
        if attribute_subset > X.shape[1]:
            attribute_subset = X.shape[1]
        X = X.sample(n=attribute_subset, axis=1, random_state=random_state)
    
    return train_test_split(X, y, test_size=0.4, random_state=random_state)




def predict(tree, sample):
    if tree.result is not None:
        return tree.result

    attribute_value = sample.get(tree.attribute)
    child_node = tree.children.get(attribute_value)

    if child_node is None:
        return None

    return predict(child_node, sample)


def evaluate(tree, features, labels):
    predictions = features.apply(lambda row: predict(tree, row), axis=1)
    accuracy = (predictions == labels).mean()

    conf_matrix = pd.crosstab(labels, predictions, rownames=['Actual'], colnames=['Predicted'], dropna=False)

    return accuracy, conf_matrix



def get_result(file_path, class_column, random_state=50):
    train_atributes, test_atributes, train_lables, test_lables = preprocess_data(file_path, class_column, random_state)
    tree = id3(train_atributes, train_lables)
    accuracy, conf_matrix = evaluate(tree, test_atributes, test_lables)
    return accuracy, conf_matrix


def main():
    # acc_bc, conf_matrix_bc = get_result("breast_cancer_data.csv", "Class")
    # acc_ms, conf_matrix_ms = get_result("mushroom_data.csv", "poisonous")
    accuracies_bc = []
    accuracies_ms = []
    conf_matrices_bc = []
    conf_matrices_ms = []

    for _ in range(2):
        random_state = np.random.randint(0, 1000)
        acc_bc, conf_matrix_bc = get_result("breast_cancer_data.csv", "Class", random_state)
        acc_ms, conf_matrix_ms = get_result("mushroom_data.csv", "poisonous", random_state)
        accuracies_bc.append(acc_bc)
        accuracies_ms.append(acc_ms)
        conf_matrices_bc.append(conf_matrix_bc)
        conf_matrices_ms.append(conf_matrix_ms)

    avg_acc_bc = np.mean(accuracies_bc)
    avg_acc_ms = np.mean(accuracies_ms)
    min_acc_bc = np.min(accuracies_bc)
    min_acc_ms = np.min(accuracies_ms)
    max_acc_bc = np.max(accuracies_bc)
    max_acc_ms = np.max(accuracies_ms)

    avg_conf_matrix_bc = sum(conf_matrices_bc) / 10
    avg_conf_matrix_ms = sum(conf_matrices_ms) / 10

    print("Breast Cancer Average Accuracy:", avg_acc_bc)
    print("Breast Cancer Min Accuracy:", min_acc_bc)
    print("Breast Cancer Max Accuracy:", max_acc_bc)
    print("Breast Cancer Average Confusion Matrix:\n", avg_conf_matrix_bc)
    print("Mushroom Average Accuracy:", avg_acc_ms)
    print("Mushroom Min Accuracy:", min_acc_ms)
    print("Mushroom Max Accuracy:", max_acc_ms)
    print("Mushroom Average Confusion Matrix:\n", avg_conf_matrix_ms)

    # print("Breast Cancer Accuracy:", acc_bc)
    # print("Breast Cancer Confusion Matrix:\n", conf_matrix_bc)
    # print("Mushroom Accuracy:", acc_ms)
    # print("Mushroom Confusion Matrix:\n", conf_matrix_ms)


if __name__ == "__main__":
    main()