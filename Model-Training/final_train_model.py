import pandas as pd
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os
import sys
import contextlib

# Define RandomForest parameters (fixed values)
RF_N_ESTIMATORS = 100
RF_MAX_DEPTH = 20  # Set to None if you want no depth limit
RF_MIN_SAMPLES_SPLIT = 2
RF_MIN_SAMPLES_LEAF = 1
RF_MAX_FEATURES = "sqrt"

# File paths
DATA_PATH = "/app/volumes/data/cleaned_wine_quality.csv"
MODEL_PATH = "/app/volumes/models/saved_model.pkl"

def load_data():
    """Load the cleaned dataset for model training."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run preprocessing first.")
    df = pd.read_csv(DATA_PATH)
    return df

def train_model():
    """Train a RandomForest model and save it."""
    # Load the dataset
    df = load_data()

    # Separate features and target
    X = df.drop("quality", axis=1)
    y = df["quality"]

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Define the RandomForest model
    rf = RandomForestClassifier(random_state=42, class_weight="balanced", n_jobs=-1)

    # Define the hyperparameter grid
    param_grid = {
        'n_estimators': [RF_N_ESTIMATORS, RF_N_ESTIMATORS + 50],
        'max_depth': [RF_MAX_DEPTH, None],
        'min_samples_split': [RF_MIN_SAMPLES_SPLIT, RF_MIN_SAMPLES_SPLIT + 2],
        'min_samples_leaf': [RF_MIN_SAMPLES_LEAF, RF_MIN_SAMPLES_LEAF + 1],
        'max_features': [RF_MAX_FEATURES, 'log2']
    }

    # Perform GridSearchCV for hyperparameter tuning
    grid_search = GridSearchCV(
        estimator=rf,
        param_grid=param_grid,
        cv=3,  # 3-fold cross-validation
        scoring='accuracy',
        n_jobs=-1,
        verbose=0
    )
    
    with contextlib.redirect_stdout(sys.stderr):  # Redirect standard output to avoid logs
        grid_search.fit(X_train, y_train)

    # Get the best model
    best_model = grid_search.best_estimator_

    # Make predictions
    y_pred = best_model.predict(X_test)

    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Classification report with zero_division to avoid warnings
    report = classification_report(y_test, y_pred, zero_division=1)
    print(f"Classification Report:\n{report}")

    # Save the trained model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(best_model, f)

if __name__ == "__main__":
    train_model()