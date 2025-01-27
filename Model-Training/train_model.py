import pandas as pd
from flask import Flask, jsonify, request
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import json
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format='%(asctime)s - %(levelname)s - %(message)s')

# Initialize Flask app
app = Flask(__name__)

# Global variables for storing metrics and model
current_metrics = None
current_model = None


def post_message(message):
    """
    Post progress updates to the console and log.
    Extendable for external API integration.
    """
    print(f"POST: {message}")
    logging.info(message)


def load_and_clean_data(filepath):
    """Load and clean the dataset."""
    try:
        post_message("Loading and Cleaning Data...")
        # Adjust the relative path to match your directory structure
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        wine = pd.read_csv(filepath)  # Use filepath passed from the function
        wine.drop(['Sample'], axis=1, inplace=True)
        wine.dropna(inplace=True)
        wine.drop_duplicates(inplace=True)
        wine = wine[wine['quality'] != 2]  # Remove rows with quality '2'
        wine.reset_index(drop=True, inplace=True)
        
        # Binary encoding for 'color' column
        wine['color'] = wine['color'].apply(lambda x: 1 if x.lower() == 'red' else 0)
        
        post_message("Data Loaded and Cleaned Successfully.")
        return wine
    except Exception as e:
        logging.error(f"Error loading and cleaning data: {e}")
        raise

def preprocess_quality(wine):
    """Preprocess quality column into categorical labels."""
    try:
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
    except Exception as e:
        logging.error(f"Error preprocessing quality labels: {e}")
        raise


def split_data(wine):
    """Split data into train, validation, and test sets."""
    try:
        post_message("Splitting Data into Train, Validation, and Test Sets...")
        feature_cols = [col for col in wine.columns if col != 'quality']
        X = wine[feature_cols]
        y = wine['quality']
        X_train, X_temp, y_train, y_temp = train_test_split(
            X, y, test_size=0.3, stratify=y, random_state=42
        )
        X_val, X_test, y_val, y_test = train_test_split(
            X_temp, y_temp, test_size=0.5, stratify=y_temp, random_state=42
        )
        post_message("Data Split Completed.")
        return X_train, X_val, X_test, y_train, y_val, y_test
    except Exception as e:
        logging.error(f"Error splitting data: {e}")
        raise


def optimize_random_forest(X_train, y_train):
    """Optimize Random Forest classifier using GridSearchCV."""
    try:
        post_message("Optimizing Random Forest Model...")
        rf = RandomForestClassifier(random_state=42, class_weight='balanced', n_jobs=-1)
        param_grid = {
            'n_estimators': [100, 150],
            'max_depth': [10, 20, None],
            'min_samples_split': [2, 5],
            'min_samples_leaf': [1, 2],
            'max_features': ['sqrt', None]
        }
        grid_search = GridSearchCV(
            estimator=rf, param_grid=param_grid, cv=3, n_jobs=-1, scoring='accuracy'
        )
        grid_search.fit(X_train, y_train)
        post_message(f"Random Forest Model Optimized Successfully. Best Parameters: {grid_search.best_params_}")
        return grid_search.best_estimator_
    except Exception as e:
        logging.error(f"Error optimizing Random Forest: {e}")
        raise


@app.route('/train', methods=['POST'])
def train_model():
    """Train the model and save it."""
    global current_metrics, current_model
    try:
        # Update the default filepath to match the relative path in your project
        data_path = request.json.get('filepath','../Data/wine_quality_assignment.csv')
        wine = load_and_clean_data(data_path)
        wine = preprocess_quality(wine)
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(wine)

        # Train and optimize the model
        rf = optimize_random_forest(X_train, y_train)

        # Evaluate on validation data
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

        post_message("Model trained and validated successfully.")
        return jsonify({
            "message": "Model trained successfully!",
            "validation_metrics": current_metrics
        })
    except Exception as e:
        logging.error(f"Error in training model: {e}")
        return jsonify({"error": str(e)}), 500



@app.route('/retrain', methods=['POST'])
def retrain_model():
    """Retrain the model."""
    return train_model()


@app.route('/save-model', methods=['POST'])
def save_model():
    """Save the trained model if requested."""
    global current_model
    try:
        if current_model:
            joblib.dump(current_model, "model.pkl")
            post_message("Model saved successfully.")
            return jsonify({"message": "Model saved successfully!"})
        else:
            return jsonify({"message": "No model available to save!"})
    except Exception as e:
        logging.error(f"Error saving model: {e}")
        return jsonify({"error": str(e)}), 500


@app.route('/get-metrics', methods=['GET'])
def get_metrics():
    """Return the latest evaluation metrics."""
    if current_metrics:
        return jsonify(current_metrics)
    return jsonify({"message": "No metrics available!"})


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
