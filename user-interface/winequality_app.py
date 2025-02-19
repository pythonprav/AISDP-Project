from flask import Flask, render_template, request, jsonify
import pandas as pd
import joblib
import json
import requests
import os

# Flask App Setup
app = Flask(__name__, static_folder="static", template_folder="templates")

# Environment-aware API URL (Docker & Kubernetes)
INFERENCE_API = os.getenv("INFERENCE_API", "http://localhost:5001/predict" if os.getenv("DOCKER_ENV") else "http://model-inference:5001/predict")

# Environment-aware Storage Paths
USER_DIR = os.getenv("USER_DIR", "/app/volumes/user")
PREDICTIONS_PATH = os.path.join(USER_DIR, 'predictions.json')

# Training Columns (Ensure order is consistent)
TRAINING_COLUMNS = [
    'Sample', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 
    'residual_sugar', 'chlorides', 'free_sulfur_dioxide', 
    'total_sulfur_dioxide', 'density', 'pH', 
    'sulphates', 'alcohol', 'color'
]

##################################################
# FUNCTION: RUN MODEL INFERENCE
##################################################
def run_inference():
    """Trigger model-inference via HTTP request."""
    try:
        response = requests.post(INFERENCE_API)
        
        # Print Response to Debug
        print(f"DEBUG: Inference API Response → {response.json()}")
        if response.status_code == 200:
            predictions = response.json()

            # Ensure JSON is saved correctly
            with open(PREDICTIONS_PATH, 'w') as file:
                json.dump(predictions, file, indent=4)
            return predictions

        return {"status": "error", "details": response.text}
    
    except Exception as e:
        return {"status": "error", "details": f"Failed to connect to inference: {str(e)}"}

##################################################
# FUNCTION: SAFE FLOAT CONVERSION
##################################################
def safe_float(value):
    """Convert value to float, return None if empty."""
    try:
        return float(value) if value.strip() else None
    except ValueError:
        return None

##################################################
# FUNCTION: FORMAT INPUT DATA
##################################################
def format_input_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure proper column format."""
    if 'Sample' not in df.columns:
        df.insert(0, 'Sample', range(1, len(df) + 1))
    return df[[col for col in TRAINING_COLUMNS if col in df.columns]]

##################################################
# ROUTES
##################################################

# HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# CSV UPLOAD PAGE
@app.route('/model_pred_csv')
def model_pred_csv():
    return render_template('model_pred_csv.html')

# MANUAL INPUT PAGE
@app.route('/model_pred_manual')
def model_pred_manual():
    return render_template('model_pred_manual.html')

# CSV UPLOAD HANDLING
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Handle CSV upload & trigger inference."""
    try:
        file = request.files.get('csvFile')
        if not file:
            return "No file selected.", 400

        # Ensure directory exists
        os.makedirs(USER_DIR, exist_ok=True)
        input_csv_path = os.path.join(USER_DIR, 'input.csv')

        # Read & format input
        df = pd.read_csv(file)
        df = format_input_dataframe(df)

        # Save files
        df.to_csv(input_csv_path, index=False)
        df.to_csv(os.path.join(USER_DIR, 'cleaned_input.csv'), index=False)

        # Run Inference
        inference_response = run_inference()

        return render_template('model_pred_csv.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500

# MANUAL INPUT HANDLING
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual input & trigger inference."""
    try:
        # Collect input with safe float conversion
        data = {
            'fixed_acidity': [safe_float(request.form.get('fixed_acidity'))],
            'volatile_acidity': [safe_float(request.form.get('volatile_acidity'))],
            'citric_acid': [safe_float(request.form.get('citric_acid'))],
            'residual_sugar': [safe_float(request.form.get('residual_sugar'))],
            'chlorides': [safe_float(request.form.get('chlorides'))],
            'free_sulfur_dioxide': [safe_float(request.form.get('free_sulfur_dioxide'))],
            'total_sulfur_dioxide': [safe_float(request.form.get('total_sulfur_dioxide'))],
            'density': [safe_float(request.form.get('density'))],
            'pH': [safe_float(request.form.get('pH'))],
            'sulphates': [safe_float(request.form.get('sulphates'))],
            'alcohol': [safe_float(request.form.get('alcohol'))],
            'color': [safe_float(request.form.get('color'))]
        }

        # Convert to DataFrame & format
        df = pd.DataFrame(data)
        df.insert(0, 'Sample', range(1, len(df) + 1))
        df = format_input_dataframe(df)

        # Save CSV
        os.makedirs(USER_DIR, exist_ok=True)
        df.to_csv(os.path.join(USER_DIR, 'input.csv'), index=False)
        df.to_csv(os.path.join(USER_DIR, 'cleaned_input.csv'), index=False)

        # Run Inference
        inference_response = run_inference()

        return render_template('model_pred_manual.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500

# FETCH PREDICTIONS (For UI)
@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    """Return stored predictions."""
    try:
        with open(PREDICTIONS_PATH, 'r') as file:
            predictions = json.load(file)
        return jsonify(predictions)
    except FileNotFoundError:
        return jsonify({"error": "Predictions file not found."})
    except Exception as e:
        return jsonify({"error": str(e)})

##################################################
# START FLASK APP
##################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)