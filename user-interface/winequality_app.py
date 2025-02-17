from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json
import subprocess

app = Flask(__name__, static_folder="static", template_folder="templates")

# Correct volume paths
USER_DIR = "/app/volumes/user"
PREDICTIONS_PATH = os.path.join(USER_DIR, 'predictions.json')

# Function to run inference via kubectl
def run_inference():
    try:
        # Get model-inference pod name
        command_get_pod = "kubectl get pods -l app=model-inference -o jsonpath='{.items[0].metadata.name}'"
        result = subprocess.run(command_get_pod, shell=True, capture_output=True, text=True)
        pod_name = result.stdout.strip().strip("'")

        if result.returncode != 0 or not pod_name:
            return {"status": "error", "details": "Model-inference pod not found."}

        # Run inference via kubectl exec
        command = ["kubectl", "exec", pod_name, "--", "python3", "/app/inference.py"]
        inference_result = subprocess.run(command, capture_output=True, text=True)

        if inference_result.returncode != 0:
            return {"status": "error", "details": inference_result.stderr}

        # Load predictions from JSON
        if not os.path.exists(PREDICTIONS_PATH):
            return {"status": "error", "details": "No predictions.json found."}

        with open(PREDICTIONS_PATH, 'r') as file:
            predictions = json.load(file)
        return predictions

    except Exception as e:
        return {"status": "error", "details": str(e)}


# ROUTES
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/model_pred_csv')
def model_pred_csv():
    return render_template('model_pred_csv.html')

@app.route('/model_pred_manual')
def model_pred_manual():
    return render_template('model_pred_manual.html')

@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Handle CSV upload and run inference."""
    try:
        file = request.files.get('csvFile')
        if not file:
            return "No file selected.", 400

        os.makedirs(USER_DIR, exist_ok=True)
        input_csv_path = os.path.join(USER_DIR, 'input.csv')
        df = pd.read_csv(file)

        # Add Sample column
        if 'Sample' not in df.columns:
            df['Sample'] = range(1, len(df) + 1)
        df.to_csv(input_csv_path, index=False)

        cleaned_csv_path = os.path.join(USER_DIR, 'cleaned_input.csv')
        df.to_csv(cleaned_csv_path, index=False)

        inference_response = run_inference()
        return render_template('model_pred_csv.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500

@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual input and run inference."""
    try:
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

        os.makedirs(USER_DIR, exist_ok=True)
        input_csv_path = os.path.join(USER_DIR, 'input.csv')
        df = pd.DataFrame(data)

        if 'Sample' not in df.columns:
            df['Sample'] = range(1, len(df) + 1)
        df.to_csv(input_csv_path, index=False)

        cleaned_csv_path = os.path.join(USER_DIR, 'cleaned_input.csv')
        df.to_csv(cleaned_csv_path, index=False)

        inference_response = run_inference()
        return render_template('model_pred_manual.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)