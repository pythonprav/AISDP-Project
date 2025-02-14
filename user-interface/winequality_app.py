from flask import Flask, render_template, request, redirect, url_for, jsonify
import os
import pandas as pd

app = Flask(__name__)

# 1. The Home Route (Serves index.html)
@app.route('/')
def home():
    return render_template('index.html')

# 2. CSV Upload Route
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    try:
        # 2a. Check if a file was uploaded
        if 'csvFile' not in request.files:
            return "No file part in request.", 400
        
        file = request.files['csvFile']
        
        if file.filename == '':
            return "No file selected.", 400
        
        # 2b. Save the CSV to volumes/user/input.csv
        user_dir = os.path.join(os.getcwd(), '../volumes/user')
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, 'input.csv')
        file.save(save_path)

        # 2c. Redirect or respond with success
        return render_template('model_pred_csv.html', 
                               message="CSV uploaded successfully! Now you can run the preprocessing.")

    except Exception as e:
        return str(e), 500

# 3. Manual Prediction Route
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    try:
        # 3a. Extract form data
        fixed_acidity = request.form.get('fixed_acidity')
        volatile_acidity = request.form.get('volatile_acidity')
        citric_acid = request.form.get('citric_acid')
        residual_sugar = request.form.get('residual_sugar')
        chlorides = request.form.get('chlorides')
        free_sulfur_dioxide = request.form.get('free_sulfur_dioxide')
        total_sulfur_dioxide = request.form.get('total_sulfur_dioxide')
        density = request.form.get('density')
        pH = request.form.get('pH')
        sulphates = request.form.get('sulphates')
        alcohol = request.form.get('alcohol')
        color = request.form.get('color')  # "red" or "white"

        # 3b. Construct DataFrame
        data = {
            'fixed_acidity': [fixed_acidity],
            'volatile_acidity': [volatile_acidity],
            'citric_acid': [citric_acid],
            'residual_sugar': [residual_sugar],
            'chlorides': [chlorides],
            'free_sulfur_dioxide': [free_sulfur_dioxide],
            'total_sulfur_dioxide': [total_sulfur_dioxide],
            'density': [density],
            'pH': [pH],
            'sulphates': [sulphates],
            'alcohol': [alcohol],
            'color': [color]
        }
        df = pd.DataFrame(data)

        # 3c. Save this row to volumes/user/cleaned_input.csv 
        # (although the real cleaning might happen in the preprocessing container)
        user_dir = os.path.join(os.getcwd(), '../volumes/user')
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, 'cleaned_input.csv')
        df.to_csv(save_path, index=False)

        # 3d. We could call the inference container or just display a message for now
        return render_template('model_pred_manual.html',
                               message="Manual input received! Cleaned data saved. Please run inference.")

    except Exception as e:
        return str(e), 500

# 4. Possibly a route to display predictions or fetch them from volumes/user/predictions.json

# 5. Run the Flask app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5003)