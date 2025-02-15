import pandas as pd
from flask import Flask, jsonify, request
from sklearn.model_selection import train_test_split, GridSearchCV
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score
import joblib
import json
import os
import logging

DATA_FOLDER = "mnt/data"
USER_INPUTS_DIR = "mnt/user"
TRAINING_FILE_PATH = "/mnt/data/cleaned_wine_quality.csv"
SAVED_MODEL_DIR = "/mnt/models/saved_model.pkl"


# Load environment variables
# TRAINING_FILE_PATH = os.getenv("TRAINING_FILE_PATH", "../Data/wine_quality_assignment.csv")
# TRAINING_FILE_PATH = os.getenv("TRAINING_FILE_PATH", "/app/data/wine_quality_assignment.csv")
# TRAINING_FILE_PATH = os.getenv("TRAINING_FILE_PATH", "/mnt/data/clean_wine_quality.csv")

# SAVED_MODEL_DIR = os.getenv("SAVED_MODEL_PATH", "./saved_model")
LOG_LEVEL = os.getenv("LOG_LEVEL", "INFO")

# # Load RandomForest parameters from environment variables
# RF_N_ESTIMATORS = int(os.getenv("RANDOM_FOREST_N_ESTIMATORS", "100"))
# RF_MAX_DEPTH = int(os.getenv("RANDOM_FOREST_MAX_DEPTH", "20")) if os.getenv("RANDOM_FOREST_MAX_DEPTH") != "None" else None
# RF_MIN_SAMPLES_SPLIT = int(os.getenv("RANDOM_FOREST_MIN_SAMPLES_SPLIT", "2"))
# RF_MIN_SAMPLES_LEAF = int(os.getenv("RANDOM_FOREST_MIN_SAMPLES_LEAF", "1"))
# RF_MAX_FEATURES = os.getenv("RANDOM_FOREST_MAX_FEATURES", "sqrt")

# Update logging level
logging.basicConfig(level=LOG_LEVEL, format='%(asctime)s - %(levelname)s - %(message)s')

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


def load_clean_data(filepath):
    """Load and clean the dataset."""
    try:
        post_message("Loading and Cleaning Data...")
        # Adjust the relative path to match your directory structure
        if not os.path.exists(filepath):
            raise FileNotFoundError(f"File not found: {filepath}")
        
        wine = pd.read_csv(filepath)  # Use filepath passed from the function
        # wine.drop(['Sample'], axis=1, inplace=True)
        # wine.dropna(inplace=True)
        # wine.drop_duplicates(inplace=True)
        # wine = wine[wine['quality'] != 2]  # Remove rows with quality '2'
        # wine.reset_index(drop=True, inplace=True)
        
        # # Binary encoding for 'color' column
        # wine['color'] = wine['color'].apply(lambda x: 1 if x.lower() == 'red' else 0)
        
        post_message("Data Loaded and Cleaned Successfully.")
        return wine
    except Exception as e:
        logging.error(f"Error loading and cleaning data: {e}")
        raise

# def preprocess_quality(wine):
#     """Preprocess quality column into categorical labels."""
#     try:
#         post_message("Preprocessing Quality Labels...")
#         quality_map = {
#             1: '1 Star', 2: '1 Star',
#             3: '2 Star', 4: '2 Star',
#             5: '3 Star', 6: '3 Star',
#             7: '4 Star', 8: '4 Star',
#             9: '5 Star', 10: '5 Star'
#         }
#         wine['quality'] = wine['quality'].map(quality_map)
#         post_message("Quality Labels Preprocessed.")
#         return wine
#     except Exception as e:
#         logging.error(f"Error preprocessing quality labels: {e}")
#         raise


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
        post_message("Optimizing Random Forest Model with GridSearchCV...")
        
        # Define the base RandomForest model
        rf = RandomForestClassifier(
            random_state=42,
            class_weight="balanced",
            n_jobs=-1
        )
        
        # # Define the hyperparameter grid
        # param_grid = {
        #     'n_estimators': [RF_N_ESTIMATORS, RF_N_ESTIMATORS + 50],
        #     'max_depth': [RF_MAX_DEPTH, None],
        #     'min_samples_split': [RF_MIN_SAMPLES_SPLIT, RF_MIN_SAMPLES_SPLIT + 2],
        #     'min_samples_leaf': [RF_MIN_SAMPLES_LEAF, RF_MIN_SAMPLES_LEAF + 1],
        #     'max_features': [RF_MAX_FEATURES, 'log2']
        # }

        # Define the hyperparameter grid with hardcoded values
        param_grid = {
            'n_estimators': [100, 150],       # Number of trees in the forest
            'max_depth': [20, None],          # Maximum depth of each tree
            'min_samples_split': [2, 4],      # Minimum samples required to split an internal node
            'min_samples_leaf': [1, 2],       # Minimum samples required to be at a leaf node
            'max_features': ['sqrt', 'log2']  # Number of features to consider for the best split
        }
        
        # Perform GridSearchCV
        grid_search = GridSearchCV(
            estimator=rf,
            param_grid=param_grid,
            cv=3,  # 3-fold cross-validation
            scoring='accuracy',
            n_jobs=-1,
            verbose=2
        )
        grid_search.fit(X_train, y_train)
        
        post_message(f"GridSearchCV completed. Best Parameters: {grid_search.best_params_}")
        
        # Return the best model
        return grid_search.best_estimator_
    except Exception as e:
        logging.error(f"Error during GridSearchCV: {e}")
        raise
    
@app.route('/train', methods=['POST'])
def train_model():
    """Train the model and save it."""
    global current_metrics, current_model
    try:
        # Update the default filepath to match the relative path in your project
        # data_path = request.json.get('filepath','../Data/wine_quality_assignment.csv')
        # data_path = os.getenv("TRAINING_FILE_PATH", "/app/data/wine_quality_assignment.csv")
        data_path = os.getenv("TRAINING_FILE_PATH", "/mnt/data/clean_wine_quality.csv")       
        wine = load_clean_data(data_path)
        # wine = preprocess_quality(wine)
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


# # Define the path to the saved_model folder
# SAVED_MODEL_DIR = os.path.join(os.getcwd(), "saved_model")
# joblib.dump(rf, "/mnt/models/saved_model.pkl")
post_message("Model saved successfully at /mnt/models/saved_model.pkl")


@app.route('/save-model', methods=['POST'])
def save_model():
    """Save the trained model in the saved_model folder."""
    global current_model
    try:
        if current_model:
            # Create the saved_model folder if it doesn't exist
            os.makedirs(SAVED_MODEL_DIR, exist_ok=True)
            model_path = os.path.join(SAVED_MODEL_DIR, "saved_model.pkl")
            joblib.dump(current_model, model_path)
            # post_message("Model saved successfully at /mnt/models/saved_model.pkl")
            # joblib.dump(current_model, model_path)
            post_message(f"Model saved successfully at {model_path}.")
            return jsonify({"message": f"Model saved successfully at {model_path}!"})
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


@app.route('/health', methods=['GET'])
def health_check():
    """Health check endpoint for Kubernetes"""
    return jsonify({"status": "ok"}), 200

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
