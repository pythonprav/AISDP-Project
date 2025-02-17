from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json
import requests

# Flask App Setup
app = Flask(__name__, static_folder="static", template_folder="templates")

# Directory Paths
USER_DIR = "/app/volumes/user"
PREDICTIONS_PATH = os.path.join(USER_DIR, 'predictions.json')

##################################################
# FUNCTION: RUN MODEL INFERENCE (Docker Direct Call)
##################################################
def run_inference():
    """Trigger the model-inference container via Docker network (Direct API Call)."""
    try:
        response = requests.post("http://model-inference:5001/predict")

        if response.status_code == 200:
            return response.json()
        else:
            return {"status": "error", "details": f"Model-inference error: {response.text}"}

    except Exception as e:
        return {"status": "error", "details": f"Failed to connect to model-inference: {str(e)}"}

##################################################
# ROUTES
##################################################

# 1. HOME PAGE
@app.route('/')
def home():
    return render_template('index.html')

# 2. CSV UPLOAD PAGE
@app.route('/model_pred_csv')
def model_pred_csv():
    return render_template('model_pred_csv.html')

# 3. MANUAL INPUT PAGE
@app.route('/model_pred_manual')
def model_pred_manual():
    return render_template('model_pred_manual.html')

# 4. CSV UPLOAD HANDLING
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Handle CSV upload and trigger inference."""
    try:
        file = request.files.get('csvFile')
        if not file:
            return "No file selected.", 400

        # Save input.csv
        os.makedirs(USER_DIR, exist_ok=True)
        input_csv_path = os.path.join(USER_DIR, 'input.csv')
        df = pd.read_csv(file)

        # Add 'Sample' column if missing
        if 'Sample' not in df.columns:
            df['Sample'] = range(1, len(df) + 1)
        df.to_csv(input_csv_path, index=False)

        # Save cleaned_input.csv
        cleaned_csv_path = os.path.join(USER_DIR, 'cleaned_input.csv')
        df.to_csv(cleaned_csv_path, index=False)

        # Call Inference (Direct Docker Network)
        inference_response = run_inference()
        return render_template('model_pred_csv.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500

# 5. MANUAL INPUT HANDLING
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual input and trigger inference."""
    try:
        # Collect input from form
        data = {
            'fixed_acidity': [request.form.get('fixed_acidity')],
            'volatile_acidity': [request.form.get('volatile_acidity')],
            'citric_acid': [request.form.get('citric_acid')],
            'residual_sugar': [request.form.get('residual_sugar')],
            'chlorides': [request.form.get('chlorides')],
            'free_sulfur_dioxide': [request.form.get('free_sulfur_dioxide')],
            'total_sulfur_dioxide': [request.form.get('total_sulfur_dioxide')],
            'density': [request.form.get('density')],
            'pH': [request.form.get('pH')],
            'sulphates': [request.form.get('sulphates')],
            'alcohol': [request.form.get('alcohol')],
            'color': [request.form.get('color')]
        }

        # Save input.csv
        os.makedirs(USER_DIR, exist_ok=True)
        input_csv_path = os.path.join(USER_DIR, 'input.csv')
        df = pd.DataFrame(data)

        # Add 'Sample' column if missing
        if 'Sample' not in df.columns:
            df['Sample'] = range(1, len(df) + 1)
        df.to_csv(input_csv_path, index=False)

        # Save cleaned_input.csv
        cleaned_csv_path = os.path.join(USER_DIR, 'cleaned_input.csv')
        df.to_csv(cleaned_csv_path, index=False)

        # Call Inference (Direct Docker Network)
        inference_response = run_inference()
        return render_template('model_pred_manual.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500

##################################################
# START FLASK APP
##################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)