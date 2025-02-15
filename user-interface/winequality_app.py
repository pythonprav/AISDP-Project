# ---------------------------------------------------
# FINAL: winequality_app.py 
# ✅ Runs Inference Correctly (Kubernetes)
# ✅ Handles CSV and Manual Input
# ✅ Displays Predictions Properly on UI
# ---------------------------------------------------

from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json
import subprocess

# -----------------------------------------------
# APP SETUP
# -----------------------------------------------
app = Flask(__name__, 
    static_folder="static", 
    template_folder="templates"
)

##################################################
# FUNCTION: RUN MODEL INFERENCE via Kubernetes
##################################################
def run_inference():
    """Trigger the model-inference container via 'kubectl exec' and return predictions."""
    try:
        # 🟡 Step 1: Get Pod Name Correctly
        command_get_pod = "kubectl get pods -l app=model-inference -o jsonpath='{.items[0].metadata.name}'"
        result = subprocess.run(command_get_pod, shell=True, capture_output=True, text=True)
        pod_name = result.stdout.strip().strip("'")

        if result.returncode != 0 or not pod_name:
            print(f"❌ Error Finding Pod: {result.stderr}")
            return {"status": "error", "details": "Model-inference pod not found."}

        print(f"✅ Model-Inference Pod Found: {pod_name}")

        # 🟡 Step 2: Run Inference via `kubectl exec`
        command = [
            "kubectl", "exec", pod_name, "--",
            "python3", "/app/inference.py"
        ]
        inference_result = subprocess.run(command, capture_output=True, text=True)

        if inference_result.returncode != 0:
            print(f"⚠️ Inference Error: {inference_result.stderr}")
            return {"status": "error", "details": inference_result.stderr}

        print("📝 Inference Output:", inference_result.stdout)

        # 🟡 Step 3: Load predictions.json
        predictions_path = "/app/volumes/user/predictions.json"
        if not os.path.exists(predictions_path):
            print("⚠️ No predictions.json found after inference.")
            return {"status": "error", "details": "No predictions found. Check inference logs."}

        with open(predictions_path, 'r') as file:
            predictions = json.load(file)

        print("📊 Predictions:", predictions)
        return predictions

    except Exception as e:
        print(f"❌ Inference Failed: {e}")
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