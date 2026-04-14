import pandas as pd
import numpy as np
import os
import math
from sklearn.tree import DecisionTreeClassifier, export_text
from sklearn.preprocessing import LabelEncoder
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score

# -----------------------------
# ENTROPY CALCULATIONS
# -----------------------------

def calculate_entropy(data_slice, target_col):
    total = len(data_slice)
    if total == 0: return 0
    counts = data_slice[target_col].value_counts()
    return -sum((c/total) * math.log2(c/total) for c in counts)

def show_entropy_calculations(df, features, target):
    print("\n" + "="*55)
    print("   STEP-BY-STEP ENTROPY / INFORMATION GAIN DERIVATION")
    print("="*55)

    initial_entropy = calculate_entropy(df, target)
    total  = len(df)
    counts = df[target].value_counts()

    print(f"\nSTEP 1: Calculate Initial Entropy of Dataset")
    print(f"        Formula: Entropy(S) = - p(i) * log2(p(i))")
    for cls, cnt in counts.items():
        print(f"        Class '{cls}': {cnt}/{total} = {cnt/total:.4f}")
    print(f"        Entropy(S) = {initial_entropy:.4f}")

    best_gain, root_node = -1, ""

    print(f"\nSTEP 2: Calculate Weighted Entropy & Information Gain per Feature")
    for feat in features:
        print(f"\n   Feature: [ {feat} ] ")
        weighted_entropy = 0
        for val in df[feat].unique():
            subset = df[df[feat] == val]
            prob   = len(subset) / total
            ent    = calculate_entropy(subset, target)
            weighted_entropy += prob * ent
            print(f"  STEP 2a: {feat}='{val}': Entropy={ent:.4f} | Weight={len(subset)}/{total}")

        ig = initial_entropy - weighted_entropy
        print(f"  STEP 2b: Weighted Entropy of '{feat}' = {weighted_entropy:.4f}")
        print(f"  STEP 2c: IG({feat}) = {initial_entropy:.4f} - {weighted_entropy:.4f} = {ig:.4f}")

        if ig > best_gain:
            best_gain, root_node = ig, feat

    print(f"\nRESULT: '{root_node}' has the highest IG ({best_gain:.4f})  ROOT NODE")
    return root_node

# -----------------------------
# GINI CALCULATIONS
# -----------------------------

def calculate_gini(data_slice, target_col):
    total = len(data_slice)
    if total == 0: return 0
    counts = data_slice[target_col].value_counts()
    return 1 - sum((c/total)**2 for c in counts)

def show_gini_calculations(df, features, target):
    print("\n" + "="*55)
    print("   STEP-BY-STEP GINI INDEX DERIVATION")
    print("="*55)

    initial_gini = calculate_gini(df, target)
    total  = len(df)
    counts = df[target].value_counts()

    print(f"\nSTEP 1: Calculate Initial Gini Index of Dataset")
    print(f"        Formula: Gini(S) = 1 -  p(i)^2")
    for cls, cnt in counts.items():
        print(f"        Class '{cls}': {cnt}/{total} = {cnt/total:.4f}  ({cnt/total:.4f})^2 = {(cnt/total)**2:.4f}")
    print(f"        Gini(S) = {initial_gini:.4f}")

    best_gain, root_node = -1, ""

    print(f"\nSTEP 2: Calculate Weighted Gini & Gini Gain per Feature")
    for feat in features:
        print(f"\n   Feature: [ {feat} ] ")
        weighted_gini = 0
        for val in df[feat].unique():
            subset = df[df[feat] == val]
            prob   = len(subset) / total
            g      = calculate_gini(subset, target)
            weighted_gini += prob * g
            print(f"  STEP 2a: {feat}='{val}': Gini={g:.4f} | Weight={len(subset)}/{total}")

        gini_gain = initial_gini - weighted_gini
        print(f"  STEP 2b: Weighted Gini of '{feat}' = {weighted_gini:.4f}")
        print(f"  STEP 2c: Gini Gain({feat}) = {initial_gini:.4f} - {weighted_gini:.4f} = {gini_gain:.4f}")

        if gini_gain > best_gain:
            best_gain, root_node = gini_gain, feat

    print(f"\nRESULT: '{root_node}' has the highest Gini Gain ({best_gain:.4f})  ROOT NODE")
    return root_node

# -----------------------------
# ROOT ONLY (CSV - NO INTERMEDIATE STEPS)
# -----------------------------

def find_root_entropy(df, features, target):
    initial_entropy = calculate_entropy(df, target)
    best_gain, root_node = -1, ""
    results = []
    for feat in features:
        weighted_entropy = sum(
            (len(df[df[feat]==val]) / len(df)) * calculate_entropy(df[df[feat]==val], target)
            for val in df[feat].unique()
        )
        ig = initial_entropy - weighted_entropy
        results.append((feat, ig, weighted_entropy))
        if ig > best_gain:
            best_gain, root_node = ig, feat

    print(f"\n{'Feature':<15} {'Weighted Entropy':>18} {'Info Gain (IG)':>16}")
    print("-" * 52)
    for feat, ig, we in results:
        marker = "  ROOT" if feat == root_node else ""
        print(f"  {feat:<13} {we:>18.4f} {ig:>16.4f}{marker}")
    print(f"\n  Initial Entropy : {initial_entropy:.4f}")
    print(f"  ROOT NODE       : '{root_node}' (IG = {best_gain:.4f})")
    return root_node

def find_root_gini(df, features, target):
    initial_gini = calculate_gini(df, target)
    best_gain, root_node = -1, ""
    results = []
    for feat in features:
        weighted_gini = sum(
            (len(df[df[feat]==val]) / len(df)) * calculate_gini(df[df[feat]==val], target)
            for val in df[feat].unique()
        )
        gini_gain = initial_gini - weighted_gini
        results.append((feat, gini_gain, weighted_gini))
        if gini_gain > best_gain:
            best_gain, root_node = gini_gain, feat

    print(f"\n{'Feature':<15} {'Weighted Gini':>15} {'Gini Gain':>12}")
    print("-" * 45)
    for feat, gg, wg in results:
        marker = "  ROOT" if feat == root_node else ""
        print(f"  {feat:<13} {wg:>15.4f} {gg:>12.4f}{marker}")
    print(f"\n  Initial Gini : {initial_gini:.4f}")
    print(f"  ROOT NODE    : '{root_node}' (Gini Gain = {best_gain:.4f})")
    return root_node

# -----------------------------
# BUILD & EVALUATE TREE
# -----------------------------

def build_tree(df, feat_list, target, metric, train_ratio, choice):
    le_map     = {}
    encoded_df = df.copy()
    for col in df.columns:
        le = LabelEncoder()
        encoded_df[col] = le.fit_transform(df[col].astype(str))
        le_map[col]     = dict(enumerate(le.classes_))

    X = encoded_df[feat_list]
    y = encoded_df[target]

    if train_ratio < 1.0:
        X_train, X_test, y_train, y_test = train_test_split(
            X, y, train_size=train_ratio, random_state=42)
    else:
        X_train, X_test, y_train, y_test = X, X, y, y

    clf = DecisionTreeClassifier(criterion=metric)
    clf.fit(X_train, y_train)

    #  Manual: show full tree structure
    #if choice == '1':
        #print("\n" + "="*55)
        #print(f"  FINAL DECISION TREE  ({metric.upper()})")
        #print("="*55)
        #print("\nCategory Mappings:")
        #for col, mapping in le_map.items():
            #print(f"  {col}: {mapping}")
        #print("\n" + export_text(clf, feature_names=feat_list))
    #  CSV: show only metrics
    if choice == '2':
        y_pred = clf.predict(X_test)
        print("\n" + "="*55)
        print("  PERFORMANCE METRICS")
        print("="*55)
        print(f"  Accuracy  : {accuracy_score(y_test, y_pred):.4f}")
        print(f"  Precision : {precision_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
        print(f"  Recall    : {recall_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")
        print(f"  F1 Score  : {f1_score(y_test, y_pred, average='weighted', zero_division=0):.4f}")

# -----------------------------
# MAIN MENU
# -----------------------------

def main_menu():
    while True:
        print("\n=== DECISION TREE LAB MENU ===")
        print("1. Manual Input")
        print("2. Dataset Input (CSV)")
        print("3. Exit")
        choice = input("Select (1/2/3): ").strip()

        if choice == '3': break

        train_ratio = 1.0

        #  MANUAL INPUT
        if choice == '1':
            feat_list = input("Enter features (space separated): ").split()
            target    = input("Enter target column: ").strip()
            rows      = int(input("Number of records: "))
            data = []
            for i in range(rows):
                print(f"Row {i+1}:")
                row         = {f: input(f"  {f}: ") for f in feat_list}
                row[target] = input(f"  {target}: ")
                data.append(row)
            df = pd.DataFrame(data)

            print("\n--- INPUT DATA TABLE ---")
            print(df.to_string(index=False))

            print("\nChoose Splitting Metric:")
            print("1. Entropy (Information Gain)")
            print("2. Gini Index")
            m_choice = input("Select (1/2): ").strip()

            if m_choice == '1':
                metric = 'entropy'
                show_entropy_calculations(df, feat_list, target)
            elif m_choice == '2':
                metric = 'gini'
                show_gini_calculations(df, feat_list, target)
            else:
                print("Invalid metric."); continue

            build_tree(df, feat_list, target, metric, train_ratio, choice)

        #  CSV INPUT
        elif choice == '2':
            fname = input("Enter CSV filename (or full path): ").strip()
            if not os.path.exists(fname):
                print("File not found!"); continue

            full_df = pd.read_csv(fname)
            print(f"\nColumns: {list(full_df.columns)}")
            target = input("Enter target column: ").strip()

            if target not in full_df.columns:
                print("Target column not found!"); continue

            max_r = len(full_df)
            req   = int(input(f"How many records? (Max {max_r}): "))
            full_df = full_df.head(min(req, max_r))

            avail = [c for c in full_df.columns if c != target]
            print(f"Available features: {avail}")
            num_attr  = int(input(f"How many attributes? (Max {len(avail)}): "))
            print(f"Enter {num_attr} attribute names (space separated):")
            feat_list = input("> ").split()

            invalid = [f for f in feat_list if f not in full_df.columns]
            if invalid:
                print(f"Invalid features: {invalid}"); continue

            print(f"\n--- DATASET SUMMARY ---")
            print(f"  Records   : {len(full_df)}")
            print(f"  Attributes: {feat_list}")
            print(f"  Target    : {target}")

            train_p     = float(input("Enter train percentage (e.g., 70): "))
            train_ratio = train_p / 100
            df          = full_df[feat_list + [target]].dropna()

            print("\n--- INPUT DATA TABLE (First 10 Rows) ---")
            print(df.head(10).to_string(index=False))

            print("\nChoose Splitting Metric:")
            print("1. Entropy (Information Gain)")
            print("2. Gini Index")
            m_choice = input("Select (1/2): ").strip()

            if m_choice == '1':
                metric = 'entropy'
                print("\n--- ROOT NODE ANALYSIS (ENTROPY) ---")
                find_root_entropy(df, feat_list, target)
            elif m_choice == '2':
                metric = 'gini'
                print("\n--- ROOT NODE ANALYSIS (GINI) ---")
                find_root_gini(df, feat_list, target)
            else:
                print("Invalid metric."); continue

            build_tree(df, feat_list, target, metric, train_ratio, choice)

        else:
            print("Invalid choice.")

if __name__ == "__main__":
    main_menu()
