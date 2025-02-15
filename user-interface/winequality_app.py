from flask import Flask, render_template, request, jsonify
import os
import pandas as pd
import json
import subprocess

app = Flask(__name__, 
    static_folder="static",     # <-- Tells Flask where your static files (css/js) live
    template_folder="templates" # <-- Tells Flask where your HTML templates live
)


##################################################
# FUNCTION: RUN MODEL INFERENCE
##################################################
def run_inference():
    """Trigger the model-inference container."""
    try:
        # Command to run the model-inference container
        command = [
            "docker", "run", "--rm",
            "-v", "/app/volumes/data:/app/volumes/data",
            "-v", "/app/volumes/models:/app/volumes/models",
            "-v", "/app/volumes/user:/app/volumes/user",
            "pariikubavat/model-inference:latest"
        ]
        
        # Execute the Docker command
        result = subprocess.run(command, capture_output=True, text=True)
        
        # Check result
        if result.returncode != 0:
            return {"status": "error", "details": result.stderr}
        
        # Read predictions from the generated predictions.json
        predictions_path = "/app/volumes/user/predictions.json"
        with open(predictions_path, 'r') as file:
            predictions = json.load(file)

        return predictions

    except Exception as e:
        return {"status": "error", "details": str(e)}


##################################################
# 1. HOME ROUTE (Serves index.html)
##################################################
@app.route('/')
def home():
    """Render the homepage."""
    return render_template('index.html')


##################################################
# 2. CSV INPUT PAGE
##################################################
@app.route('/model_pred_csv')
def model_pred_csv():
    """Render the CSV upload page."""
    return render_template('model_pred_csv.html')


##################################################
# 3. MANUAL INPUT PAGE
##################################################
@app.route('/model_pred_manual')
def model_pred_manual():
    """Render the manual input page."""
    return render_template('model_pred_manual.html')


##################################################
# 4. CSV UPLOAD & INFERENCE ROUTE
##################################################
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """Handle CSV file upload and trigger inference."""
    try:
        file = request.files.get('csvFile')
        if not file or file.filename == '':
            return "No file selected.", 400

        # Save uploaded CSV as input.csv
        user_dir = os.path.join(os.getcwd(), '../volumes/user')
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, 'input.csv')
        file.save(save_path)

        # Run inference
        inference_response = run_inference()

        # Show predictions in the same page
        return render_template('model_pred_csv.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500


##################################################
# 5. MANUAL INPUT & INFERENCE ROUTE
##################################################
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """Handle manual input, run inference, and show predictions."""
    try:
        # Collect form inputs
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

        # Save to cleaned_input.csv
        user_dir = os.path.join(os.getcwd(), '../volumes/user')
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, 'cleaned_input.csv')
        pd.DataFrame(data).to_csv(save_path, index=False)

        # Run inference
        inference_response = run_inference()

        # Show predictions on the page
        return render_template('model_pred_manual.html', predictions=inference_response)

    except Exception as e:
        return str(e), 500


##################################################
# 6. FETCH PREDICTIONS
##################################################
@app.route('/get_predictions', methods=['GET'])
def get_predictions():
    """Fetch predictions from predictions.json and display them in the UI."""
    predictions_path = os.path.join(os.getcwd(), '../volumes/user/predictions.json')
    try:
        with open(predictions_path, 'r') as file:
            predictions = json.load(file)

        return jsonify(predictions)

    except FileNotFoundError:
        return jsonify({"error": "Predictions file not found. Run inference first."})
    except Exception as e:
        return jsonify({"error": str(e)})


##################################################
# RUN THE FLASK APP
##################################################
if __name__ == "__main__":
    # Using port 5003 as per your preference
    app.run(host="0.0.0.0", port=5003, debug=True)