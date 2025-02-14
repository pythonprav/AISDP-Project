from flask import Flask, render_template, request, jsonify
import os
import pandas as pd

app = Flask(__name__, 
    static_folder="static",     # <-- Tells Flask where your static files (css/js) live
    template_folder="templates" # <-- Tells Flask where your HTML templates live
)

##################################################
# 1. HOME ROUTE (Serves index.html)
##################################################
@app.route('/')
def home():
    """
    Render the homepage (index.html).
    """
    return render_template('index.html')

##################################################
# 2. MODEL_PRED_CSV ROUTE (Shows CSV Page)
##################################################
@app.route('/model_pred_csv')
def model_pred_csv():
    """
    Render the CSV upload page (model_pred_csv.html).
    """
    return render_template('model_pred_csv.html')

##################################################
# 3. MODEL_PRED_MANUAL ROUTE (Shows Manual Input Page)
##################################################
@app.route('/model_pred_manual')
def model_pred_manual():
    """
    Render the manual input page (model_pred_manual.html).
    """
    return render_template('model_pred_manual.html')

##################################################
# 4. CSV UPLOAD ROUTE
##################################################
@app.route('/upload_csv', methods=['POST'])
def upload_csv():
    """
    Handle CSV file uploads from model_pred_csv.html form.
    Saves the file as input.csv under volumes/user.
    """
    try:
        # Check if the 'csvFile' field is in the request
        if 'csvFile' not in request.files:
            return "No file part in the request.", 400

        file = request.files['csvFile']

        if file.filename == '':
            return "No file selected.", 400

        # Build the path to volumes/user
        user_dir = os.path.join(os.getcwd(), '../volumes/user')
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, 'input.csv')

        # Save the uploaded file
        file.save(save_path)

        # Return a message or re-render the CSV page with a success note
        return render_template('model_pred_csv.html', 
                               message="CSV uploaded successfully! Now you can run the preprocessing container or proceed with other steps.")

    except Exception as e:
        return str(e), 500

##################################################
# 5. MANUAL PREDICTION ROUTE
##################################################
@app.route('/predict_manual', methods=['POST'])
def predict_manual():
    """
    Handle the manual input form from model_pred_manual.html.
    Saves data to cleaned_input.csv under volumes/user.
    """
    try:
        # Grab data from the form fields
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

        # Construct a small DataFrame
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

        # Build the path to volumes/user
        user_dir = os.path.join(os.getcwd(), '../volumes/user')
        os.makedirs(user_dir, exist_ok=True)
        save_path = os.path.join(user_dir, 'cleaned_input.csv')

        # Save this data
        df.to_csv(save_path, index=False)

        # Just re-render the manual page with a success note
        return render_template('model_pred_manual.html',
                               message="Manual input received and saved to cleaned_input.csv. You can run inference now.")

    except Exception as e:
        return str(e), 500

##################################################
# RUN THE FLASK APP
##################################################
if __name__ == "__main__":
    # Using port 5003 as per your preference
    app.run(host="0.0.0.0", port=5003, debug=True)