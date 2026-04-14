import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split
from collections import Counter
from tabulate import tabulate

def euclidean(a, b):
    return np.sqrt(np.sum((a - b) ** 2))

def manhattan(a, b):
    return np.sum(np.abs(a - b))

def chebyshev(a, b):
    return np.max(np.abs(a - b))

def get_distance_function(name):
    dist_map = {
        "manhattan": manhattan,
        "chebyshev": chebyshev
    }
    return dist_map.get(name, euclidean)

def knn(x_train, y_train, x_test, k, dist_func, weighted):
    distances = []
    for i in range(len(x_train)):
        dist = dist_func(x_train[i], x_test)
        distances.append((i, dist, y_train[i]))
    sorted_distances = sorted(distances, key=lambda x: x[1])
    neighbors = sorted_distances[:k]

    if weighted:
        votes = {}
        for idx, dist, label in neighbors:
            weight = 1 / (dist**2) if dist != 0 else 1000
            votes[label] = votes.get(label, 0) + weight
        prediction = max(votes, key=votes.get)
    else:
        labels = [label for _, _, label in neighbors]
        prediction = Counter(labels).most_common(1)[0][0]

    return prediction, distances, neighbors

def evaluate_metrics(y_true, y_pred):
    classes = set(y_true)
    total = len(y_true)
    accuracy = sum(1 for i in range(total)
                   if y_true[i] == y_pred[i]) / total

    precision_sum = 0
    recall_sum = 0
    f1_sum = 0

    for cls in classes:
        tp = sum(1 for i in range(total)
                 if y_pred[i] == cls and y_true[i] == cls)
        fp = sum(1 for i in range(total)
                 if y_pred[i] == cls and y_true[i] != cls)
        fn = sum(1 for i in range(total)
                 if y_pred[i] != cls and y_true[i] == cls)

        precision = tp / (tp + fp) if (tp + fp) != 0 else 0
        recall = tp / (tp + fn) if (tp + fn) != 0 else 0
        f1 = (2 * precision * recall) / (precision + recall) \
            if (precision + recall) != 0 else 0

        precision_sum += precision
        recall_sum += recall
        f1_sum += f1

    n_classes = len(classes)
    return accuracy, precision_sum/n_classes, recall_sum/n_classes, f1_sum/n_classes

def csv_mode():
    path = input("CSV path: ").strip()
    try:
        df = pd.read_csv(path)
    except Exception as e:
        print("Error reading CSV:", e)
        return

    print("\nAvailable Columns:", list(df.columns))

    feature_cols = [c.strip() for c in input(
        "Feature columns (comma separated): ").split(",")]
    class_col = input("Class column: ").strip()

    X = df[feature_cols].values
    y = df[class_col].values

    train_percent = float(input("Training percentage: "))
    metric_name = input("Metric (euclidean/manhattan/chebyshev): ").lower()
    weighted = input("Weighted? (yes/no): ").lower() == "yes"

    test_size = 1 - (train_percent / 100)

    x_train, x_test, y_train, y_test = train_test_split(
        X, y, test_size=test_size, random_state=42
    )

    k = int(0.1 * len(x_train))
    if k == 0:
        k = 1
    if k % 2 == 0:
        k += 1

    print("\n--- DATA SPLIT INFO ---")
    print("Total rows:", len(df))
    print("x_train length:", len(x_train))
    print("x_test length :", len(x_test))
    print("k value       :", k)

    dist_func = get_distance_function(metric_name)
    results_table = []
    headers = ["S.No"] + feature_cols + \
        ["Actual Class", "Predicted Class"]

    y_pred = []

    for i in range(len(x_test)):
        pred, _, _ = knn(
            x_train, y_train, x_test[i], k, dist_func, weighted)
        y_pred.append(pred)

        row = [i+1] + [f"{val:.4f}" for val in x_test[i]] + \
            [y_test[i], pred]
        results_table.append(row)

    acc, prec, rec, f1 = evaluate_metrics(y_test, y_pred)
    print("\n--- EVALUATION METRICS ---")
    print(f"Accuracy : {acc:.4f}")
    print(f"Precision: {prec:.4f}")
    print(f"Recall   : {rec:.4f}")
    print(f"F1 Score : {f1:.4f}")
def manual_mode():
    rows = int(input("Existing rows: "))
    cols = int(input("Number of features: "))

    f_names = [input(f"Feature {i+1} name: ").strip()
               for i in range(cols)]
    c_name = input("Class column name: ").strip()

    data = []
    for i in range(rows):
        r = [float(input(f"Row {i+1} - {f_names[j]}: "))
             for j in range(cols)]
        r.append(input(f"Row {i+1} - {c_name}: "))
        data.append(r)

    df = pd.DataFrame(data, columns=f_names + [c_name])

    print("\n--- Enter New Data Point to Classify ---")
    new_point = np.array([float(input(f"Value for {name}: "))
                          for name in f_names])

    X_train = df[f_names].values
    y_train = df[c_name].values

    metric = input("Metric (euclidean/manhattan/chebyshev): ").lower()
    weighted = input("Weighted? (yes/no): ").lower() == "yes"
    k = int(input("Enter k value: "))

    dist_func = get_distance_function(metric)
    pred, all_distances, neighbors = knn(
        X_train, y_train, new_point, k, dist_func, weighted)

    table = []
    headers = ["S.No"] + f_names + ["Class Label", "Distance Found", "1/d"]

    for idx, dist, label in all_distances:
        inv_d2 = 1 / (dist**2) if dist != 0 else 1000  # avoid div by 0
        row = [idx+1] + \
            [f"{val:.4f}" for val in X_train[idx]] + \
            [label, round(dist, 4), round(inv_d2, 6)]
        table.append(row)

    print("\n--- INTERMEDIARY CALCULATION RESULTS ---")
    print(tabulate(table, headers=headers, tablefmt="pretty"))

    print("\n--- VOTING SUMMARY ---")
    if weighted:
        votes = {}
        for idx, dist, label in neighbors:
            weight = 1 / (dist**2) if dist != 0 else 1000
            votes[label] = votes.get(label, 0) + weight

        for label, total_weight in votes.items():
            print(f"Class {label} -> Total Weight: {round(total_weight, 6)}")
    else:
        counts = {}
        for _, _, label in neighbors:
            counts[label] = counts.get(label, 0) + 1

        for label, total in counts.items():
            print(f"Class {label} -> Total Votes: {total}")

    print("\nFINAL PREDICTED CLASS:", pred)

def main():
    print("1. CSV Dataset\n2. Manual Dataset")
    choice = input("Choice: ")

    if choice == "1":
        csv_mode()
    else:
        manual_mode()

if __name__ == "__main__":
    main()
