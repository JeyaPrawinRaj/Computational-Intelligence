import pandas as pd
import numpy as np

from sklearn.model_selection import train_test_split, StratifiedKFold, cross_val_score
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, confusion_matrix


def run_model():
    try:
        print("\n========= UNIVERSAL DATASET RANDOM FOREST =========")

        file_path = input("\nEnter dataset file path: ")
        target_col = input("Enter TARGET column name: ")
        n_trees = int(input("Enter number of decision trees: "))
        test_size = float(input("Enter test size: "))
        k_value = int(input("Enter K value for K-Fold: "))

        data = pd.read_csv(file_path)

        data.replace("?", np.nan, inplace=True)
        data.dropna(inplace=True)

        y = data[target_col]
        X = data.drop(target_col, axis=1)

        if y.dtype == 'object':
            y = y.astype('category').cat.codes

        X = pd.get_dummies(X)

        X_train, X_test, y_train, y_test = train_test_split(
            X, y, test_size=test_size, stratify=y, random_state=42
        )

        model = RandomForestClassifier(
            n_estimators=n_trees,
            criterion='entropy',
            random_state=42,
            n_jobs=-1
        )

        skf = StratifiedKFold(n_splits=k_value, shuffle=True, random_state=42)
        cross_val_score(model, X_train, y_train, cv=skf)

        model.fit(X_train, y_train)
        y_pred = model.predict(X_test)

        print(" Accuracy :", accuracy_score(y_test, y_pred))
        print(" Precision:", precision_score(y_test, y_pred, average='weighted'))
        print(" Recall   :", recall_score(y_test, y_pred, average='weighted'))
        print(" F1 Score :", f1_score(y_test, y_pred, average='weighted'))

        print("\nConfusion Matrix:")
        print(confusion_matrix(y_test, y_pred))

    except Exception as e:
        print("ERROR:", e)


if __name__ == "__main__":
    run_model()
