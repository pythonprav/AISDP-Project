import pandas as pd
from flask import Flask, jsonify, request
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import json

app = Flask(__name__)

current_metrics = None  # Store metrics for web display
current_model = None    # Store the latest trained model


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
        1: '1 Star', 2: '1 Star',
        3: '2 Star', 4: '2 Star',
        5: '3 Star', 6: '3 Star',
        7: '4 Star', 8: '4 Star',
        9: '5 Star', 10: '5 Star'
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


def optimize_random_forest(X_train, y_train):
    """Optimize Random Forest classifier using GridSearchCV."""
    post_message("Optimizing Random Forest Model...")
    rf = RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1)
    param_grid = {
        'n_estimators': [100, 150],
        'max_depth': [10, 20, None],
        'min_samples_split': [2, 5],
        'min_samples_leaf': [1, 2],
        'max_features': ['sqrt', None]
    }
    grid_search = GridSearchCV(estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='accuracy')
    grid_search.fit(X_train, y_train)
    post_message(f"Random Forest Model Optimized Successfully. Best Parameters: {grid_search.best_params_}")
    return grid_search.best_estimator_


@app.route('/train', methods=['POST'])
def train_model():
    """Train the model and save it."""
    global current_metrics, current_model
    data_path = request.json.get('filepath', 'wine_quality_assignment.csv')
    wine = load_and_clean_data(data_path)
    wine = preprocess_quality(wine)
    X_train, X_val, X_test, y_train, y_val, y_test = split_data(wine)

    # Train the model
    rf = optimize_random_forest(X_train, y_train)

    # Evaluate on Validation Data
    y_val_pred = rf.predict(X_val)
    current_metrics = {
        'accuracy': accuracy_score(y_val, y_val_pred),
        'precision': precision_score(y_val, y_val_pred, average='macro'),
        'recall': recall_score(y_val, y_val_pred, average='macro'),
        'f1': f1_score(y_val, y_val_pred, average='macro')
    }
    current_model = rf

    # Save feature names for inference
    feature_names = list(X_train.columns)
    with open("feature_names.json", "w") as f:
        json.dump(feature_names, f)

    return jsonify({
        "message": "Model trained successfully!",
        "validation_metrics": current_metrics
    })


@app.route('/retrain', methods=['POST'])
def retrain_model():
    """Retrain the model."""
    return train_model()


@app.route('/save-model', methods=['POST'])
def save_model():
    """Save the trained model if requested."""
    global current_model
    if current_model:
        joblib.dump(current_model, "model.pkl")
        return jsonify({"message": "Model saved successfully!"})
    return jsonify({"message": "No model available to save!"})


@app.route('/get-metrics', methods=['GET'])
def get_metrics():
    """Return the latest evaluation metrics."""
    if current_metrics:
        return jsonify(current_metrics)
    return jsonify({"message": "No metrics available!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
