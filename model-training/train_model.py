import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib

def post_message(message):
    """
    Print progress updates to the console.
    """
    print(f"POST: {message}")

def load_data(filepath):
    """
    Load the preprocessed data and remove rare classes.
    """
    print("Loading preprocessed data...")
    df = pd.read_csv(filepath)

    if 5 in df['quality'].unique():
        df = df[df['quality'] != 5]
        print("Removed classes with very low representation (e.g., quality == 5).")
    else:
        print("Class '5' not found. Skipping removal.")
    
    return df

def split_data(df):
    """
    Split data into train, validation, and test sets.
    """
    print("Splitting data into train, validation, and test sets...")
    
    X = df.drop(columns=["quality"])
    y = df["quality"]

    # Initial split into train and temp (stratified)
    X_train, X_temp, y_train, y_temp = train_test_split(
        X, y, test_size=0.3, stratify=y, random_state=42
    )

    # Second split into validation and test (stratified)
    X_val, X_test, y_val, y_test = train_test_split(
        X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
    )
    
    return X_train, X_val, X_test, y_train, y_val, y_test

def optimize_random_forest(X_train, y_train):
    """
    Optimize Random Forest classifier using GridSearchCV.
    """
    print("Optimizing Random Forest model...")
    rf = RandomForestClassifier(random_state=42, class_weight="balanced", n_jobs=-1)
    
    param_grid = {
        "n_estimators": [100, 150],
        "max_depth": [10, 20, None],
        "min_samples_split": [2, 5],
        "min_samples_leaf": [1, 2],
        "max_features": ["sqrt", None]
    }
    
    grid_search = GridSearchCV(
        estimator=rf, param_grid=param_grid, cv=3, scoring="accuracy", n_jobs=-1
    )
    grid_search.fit(X_train, y_train)
    print(f"Best Parameters: {grid_search.best_params_}")
    
    return grid_search.best_estimator_

def evaluate_model(model, X, y, dataset_name):
    """
    Evaluate the model and display metrics.
    """
    print(f"Evaluating model on {dataset_name} data...")
    y_pred = model.predict(X)
    metrics = {
        "accuracy": accuracy_score(y, y_pred),
        "precision": precision_score(y, y_pred, average="macro"),
        "recall": recall_score(y, y_pred, average="macro"),
        "f1_score": f1_score(y, y_pred, average="macro")
    }
    print(f"{dataset_name} Metrics: {metrics}")
    return metrics

def main():
    # Filepaths
    data_filepath = "data/cleaned_wine_quality.csv"
    model_save_path = "model-training/optimized_rf_model.pkl"
    
    # Load preprocessed data
    df = load_data(data_filepath)
    
    # Split data into train, validation, and test sets
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(df)
    
    # Optimize and train Random Forest
    model = optimize_random_forest(X_train, y_train)
    
    # Evaluate on validation set
    val_metrics = evaluate_model(model, X_val, y_val, "Validation")
    
    # Evaluate on test set
    test_metrics = evaluate_model(model, X_test, y_test, "Test")
    
    # Save the trained model
    joblib.dump(model, model_save_path)
    print(f"Model saved at: {model_save_path}")

if __name__ == "__main__":
    main()