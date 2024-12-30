# This file is the base training file
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import (
    classification_report,
    accuracy_score,
    precision_score,
    recall_score,
    f1_score
)
import warnings

warnings.filterwarnings("ignore", category=UserWarning)
warnings.filterwarnings("ignore", category=RuntimeWarning)


def post_message(message):
    """Post progress updates to the console."""
    print(f"POST: {message}")


def load_and_clean_data(filepath):
    """Load and clean the dataset."""
    post_message("Loading and Cleaning Data...")
    wine = pd.read_csv(filepath)
    wine.drop(['Sample', 'color'], axis=1, inplace=True)
    wine.dropna(inplace=True)
    wine.drop_duplicates(inplace=True)
    wine = wine[wine['quality'] != 2]  # Removing rows with quality '2'
    wine.reset_index(drop=True, inplace=True)
    post_message("Data Loaded and Cleaned Successfully.")
    return wine


def preprocess_quality(wine):
    """Preprocess quality column into categorical labels."""
    post_message("Preprocessing Quality Labels...")
    quality_map = {
        1: '1 Star',
        2: '1 Star',
        3: '2 Star',
        4: '2 Star',
        5: '3 Star',
        6: '3 Star',
        7: '4 Star',
        8: '4 Star',
        9: '5 Star',
        10: '5 Star'
    }
    wine['quality'] = wine['quality'].map(quality_map)
    post_message("Quality Labels Preprocessed.")
    return wine


def split_data(wine):
    """Split data into train, validation, and test sets."""
    post_message("Splitting Data into Train, Validation, and Test Sets...")
    feature_cols = [col for col in wine.columns if col != 'quality']
    X = wine[feature_cols]
    y = wine['quality']
    X_train, X_temp, y_train, y_temp = train_test_split(X, y, test_size=0.3, stratify=y, random_state=42)
    X_val, X_test, y_val, y_test = train_test_split(X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42)
    post_message("Data Split Completed.")
    return X_train, X_val, X_test, y_train, y_val, y_test


def evaluate_model(y_true, y_pred):
    """Calculate and return evaluation metrics."""
    return {
        'accuracy': accuracy_score(y_true, y_pred),
        'precision': precision_score(y_true, y_pred, average='macro'),
        'recall': recall_score(y_true, y_pred, average='macro'),
        'f1': f1_score(y_true, y_pred, average='macro')
    }


def optimize_random_forest(X_train, y_train):
    """Optimize Random Forest classifier using GridSearchCV."""
    post_message("Optimizing Random Forest Model...")
    rf = RandomForestClassifier(
        random_state=42,
        class_weight='balanced',
        n_jobs=-1
    )
    param_grid = {
        'n_estimators': [100, 150],  # Reduced for faster execution
        'max_depth': [10, 20, None],  # Includes None for no depth limit
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['sqrt', None]
    }
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    post_message(f"Random Forest Model Optimized Successfully. Best Parameters: {grid_search.best_params_}")
    return grid_search.best_estimator_


def display_metrics(metrics, label):
    """Display metrics in the terminal."""
    print(f"\n{label} Metrics:")
    for metric, value in metrics.items():
        print(f"{metric.capitalize()}: {value:.4f}")


def main(filepath):
    # Load and preprocess data
    wine = load_and_clean_data(filepath)
    wine = preprocess_quality(wine)
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(wine)

    # Optimize and Train Random Forest
    rf = optimize_random_forest(X_train, y_train)

    # Evaluate on Validation Data
    post_message("Evaluating Model on Validation Data...")
    y_val_pred = rf.predict(X_val)
    val_metrics = evaluate_model(y_val, y_val_pred)
    display_metrics(val_metrics, "Validation")
    print("\nValidation Classification Report:")
    print(classification_report(y_val, y_val_pred))

    # Evaluate on Test Data
    post_message("Evaluating Model on Test Data...")
    y_test_pred = rf.predict(X_test)
    test_metrics = evaluate_model(y_test, y_test_pred)
    display_metrics(test_metrics, "Test")
    print("\nTest Classification Report:")
    print(classification_report(y_test, y_test_pred))


    # Display Feature Importance
    post_message("Analyzing Feature Importance...")
    feature_importance = pd.Series(rf.feature_importances_, index=X_train.columns).sort_values(ascending=False)
    print("\nFeature Importance:")
    print(feature_importance)

    # Re-Training Option
    satisfied = input("Are you satisfied with the model's performance? (yes/no): ").strip().lower()
    while satisfied == 'no':
        post_message("Re-Training the Model...")
        rf = optimize_random_forest(X_train, y_train)
        post_message("Model Re-Trained Successfully.")
        y_val_pred = rf.predict(X_val)
        val_metrics = evaluate_model(y_val, y_val_pred)
        display_metrics(val_metrics, "Re-Trained Validation")
        satisfied = input("Are you satisfied with the model's performance? (yes/no): ").strip().lower()

    # Save Model
    save_model = input("Save the model? (yes/no): ").strip().lower()
    if save_model == 'yes':
        import joblib
        joblib.dump(rf, 'optimized_rf_model.pkl')
        post_message("Model Saved Successfully.")
    else:
        post_message("Model Not Saved.")


if __name__ == "__main__":
    main('C:\\Users\\srira\\Downloads\\wine_quality_assignment.csv')
