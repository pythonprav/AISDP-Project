# ---------------------------------------------------
# FULLY FIXED: winequality_app.py 
# Overwrites input.csv and cleaned_input.csv for CSV & Manual
# Uses Kubernetes (kubectl) for model inference
# ---------------------------------------------------

from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json
import subprocess

app = Flask(__name__, 
    static_folder="static", 
    template_folder="templates"
)

##################################################
# FUNCTION: RUN MODEL INFERENCE via Kubernetes
##################################################
def run_inference():
    """Trigger the model-inference container via 'kubectl exec'."""
    try:
        # Get the pod name dynamically
        command_get_pod = ["kubectl", "get", "pods", "-l", "app=model-inference", "-o", "jsonpath='{.items[0].metadata.name}'"]
        pod_name = subprocess.check_output(command_get_pod, shell=True).decode('utf-8').strip("'")

        if not pod_name:
            return {"status": "error", "details": "Could not find model-inference pod."}

        # Run inference in the model-inference pod using kubectl
        command = [
            "kubectl", "exec", pod_name, "--",
            "python3", "/app/inference.py"
        ]

        result = subprocess.run(command, capture_output=True, text=True)

        if result.returncode != 0:
            return {"status": "error", "details": result.stderr}

        predictions_path = "/app/volumes/user/predictions.json"
        if not os.path.exists(predictions_path):
            return {"status": "error", "details": "predictions.json not found"}

        with open(predictions_path, 'r') as file:
            predictions = json.load(file)

        return predictions

    except Exception as e:
        return {"status": "error", "details": str(e)}


##################################################
# 1. HOME ROUTE
##################################################
@app.route('/')
def home():
    return render_template('index.html')


##################################################
# 2. CSV INPUT PAGE
##################################################
@app.route('/model_pred_csv')
def model_pred_csv():
    return render_template('model_pred_csv.html')


##################################################
# 3. MANUAL INPUT PAGE
##################################################
@app.route('/model_pred_manual')
def model_pred_manual():
    return render_template('model_pred_manual.html')


##################################################
# 4. CSV UPLOAD & INFERENCE ROUTE
##################################################
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Handle CSV upload and trigger inference."""
    try:
        file = request.files.get('csvFile')
        if not file:
            return "No file selected.", 400

        user_dir = "/app/volumes/user"
        os.makedirs(user_dir, exist_ok=True)

        # Save input.csv
        input_csv_path = os.path.join(user_dir, 'input.csv')
        df = pd.read_csv(file)
        if 'sample' not in df.columns:
            df['sample'] = range(1, len(df) + 1)
        df.to_csv(input_csv_path, index=False)

        # Save cleaned_input.csv
        cleaned_csv_path = os.path.join(user_dir, 'cleaned_input.csv')
        df.to_csv(cleaned_csv_path, index=False)

        # Run inference
        inference_response = run_inference()

        return render_template('model_pred_csv.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500


##################################################
# 5. MANUAL INPUT & INFERENCE ROUTE
##################################################
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual input and trigger inference."""
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

        user_dir = "/app/volumes/user"
        os.makedirs(user_dir, exist_ok=True)

        # Save input.csv
        input_csv_path = os.path.join(user_dir, 'input.csv')
        df = pd.DataFrame(data)
        if 'sample' not in df.columns:
            df['sample'] = range(1, len(df) + 1)
        df.to_csv(input_csv_path, index=False)

        # Save cleaned_input.csv
        cleaned_csv_path = os.path.join(user_dir, 'cleaned_input.csv')
        df.to_csv(cleaned_csv_path, index=False)

        # Run inference
        inference_response = run_inference()

        return render_template('model_pred_manual.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500


##################################################
# 6. FETCH PREDICTIONS
##################################################
@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    """Fetch predictions from predictions.json."""
    predictions_path = "/app/volumes/user/predictions.json"
    try:
        with open(predictions_path, 'r') as file:
            predictions = json.load(file)
        return jsonify(predictions)
    except FileNotFoundError:
        return jsonify({"error": "Predictions file not found."})
    except Exception as e:
        return jsonify({"error": str(e)})


##################################################
# RUN THE FLASK APP
##################################################
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003, debug=True)