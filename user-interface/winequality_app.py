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

# Columns based on your 'cleaned_wine_quality.csv' training data
TRAINING_COLUMNS = [
    'Sample', 'fixed_acidity', 'volatile_acidity', 'citric_acid', 
    'residual_sugar', 'chlorides', 'free_sulfur_dioxide', 
    'total_sulfur_dioxide', 'density', 'pH', 
    'sulphates', 'alcohol', 'color'
]

##################################################
# FUNCTION: RUN MODEL INFERENCE (Docker Direct Call)
##################################################
def run_inference(df: pd.DataFrame):
    """Trigger the model-inference container via Docker network (Direct API Call)."""
    try:
        response = requests.post("http://model-inference:5001/predict")

        if response.status_code == 200:
            predictions = response.json()

            # Save predictions to predictions.json
            with open(PREDICTIONS_PATH, 'w') as file:
                json.dump(predictions, file, indent=4)

            # Combine original input with predictions
            if "predictions" in predictions:
                df["Predicted Quality"] = predictions["predictions"]
            else:
                df["Predicted Quality"] = "N/A"

            return {"status": "success", "table": df.to_dict(orient="records")}
        else:
            return {"status": "error", "details": f"Model-inference error: {response.text}"}

    except Exception as e:
        return {"status": "error", "details": f"Failed to connect to model-inference: {str(e)}"}

##################################################
# FUNCTION: FORMAT INPUT DATA
##################################################
def format_input_dataframe(df: pd.DataFrame) -> pd.DataFrame:
    """Ensure proper columns and order for the model."""
    if 'Sample' not in df.columns:
        df.insert(0, 'Sample', range(1, len(df) + 1))

    # Reorder columns to match training
    df = df[[col for col in TRAINING_COLUMNS if col in df.columns]]

    return df

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

##################################################
# 4. CSV UPLOAD HANDLING
##################################################
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

        # Format input to match training
        df = format_input_dataframe(df)

        # Save input.csv and cleaned_input.csv
        df.to_csv(input_csv_path, index=False)
        df.to_csv(os.path.join(USER_DIR, 'cleaned_input.csv'), index=False)

        # Run inference
        inference_response = run_inference(df)

        return render_template(
            'model_pred_csv.html', 
            predictions=inference_response.get("table", []),
            error=inference_response.get("details")
        )

    except Exception as e:
        return str(e), 500

##################################################
# 5. MANUAL INPUT HANDLING
##################################################
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

        df = pd.DataFrame(data)
        df = format_input_dataframe(df)

        # Save CSV
        os.makedirs(USER_DIR, exist_ok=True)
        df.to_csv(os.path.join(USER_DIR, 'input.csv'), index=False)
        df.to_csv(os.path.join(USER_DIR, 'cleaned_input.csv'), index=False)

        # Run inference
        inference_response = run_inference(df)

        return render_template(
            'model_pred_manual.html',
            predictions=inference_response.get("table", []),
            error=inference_response.get("details")
        )

    except Exception as e:
        return str(e), 500
    
##################################################
# FETCH PREDICTIONS (For API)
##################################################
@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    """Return predictions from predictions.json."""
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