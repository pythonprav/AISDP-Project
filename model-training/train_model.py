import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score, precision_score, recall_score, f1_score
import joblib
import os

# Load and clean the dataset
def load_data(filepath):
    print("Loading preprocessed data...")
    df = pd.read_csv(filepath)
    return df

# Split data
def split_data(df):
    print("Splitting data into train, validation, and test sets...")
    X = df.drop(columns=["quality"])
    y = df["quality"]
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)
    return X_train, X_val, X_test, y_train, y_val, y_test

# Train Random Forest
def train_random_forest(X_train, y_train):
    print("Training Random Forest model...")
    rf = RandomForestClassifier(random_state=42, class_weight="balanced", n_jobs=-1)
    param_grid = {
        "n_estimators": [100, 150],
        "max_depth": [10, 20, None],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "max_features": ["sqrt", None],
    }
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, scoring="accuracy", n_jobs=-1)
    grid_search.fit(X_train, y_train)
    print(f"Best parameters: {grid_search.best_params_}")
    return grid_search.best_estimator_

# Evaluate model
def evaluate_model(model, X, y, label):
    print(f"Evaluating on {label} set...")
    y_pred = model.predict(X)
    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred, average="macro"),
        "recall": recall_score(y, y_pred, average="macro"),
        "f1_score": f1_score(y, y_pred, average="macro"),
    }
    print(f"{label} Metrics:")
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.4f}")
    print(f"{label} Classification Report:")
    print(classification_report(y, y_pred))

# Main script
if __name__ == "__main__":
    filepath = "data/cleaned_wine_quality.csv"
    model_path = "model-training/random_forest_model.pkl"
    if not os.path.exists(filepath):
        raise FileNotFoundError(f"Preprocessed data not found at {filepath}.")

    # Load data
    df = load_data(filepath)

    # Split data
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)

    # Train model
    model = train_random_forest(X_train, y_train)

    # Evaluate model
    evaluate_model(model, X_val, y_val, "Validation")
    evaluate_model(model, X_test, y_test, "Test")

    # Save the model
    print(f"Saving model to {model_path}...")
    joblib.dump(model, model_path)
    print("Model saved successfully!")