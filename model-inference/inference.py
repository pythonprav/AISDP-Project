import pandas as pd
import joblib
from flask import Flask, request, jsonify
import os

# Initialize Flask application
app = Flask(__name__)

# File paths
MODEL_PATH = '/app/volumes/models/saved_model.pkl'
INPUT_PATH = '/app/volumes/user/cleaned_input.csv'
OUTPUT_PATH = '/app/volumes/user/predictions.csv'


# Step 1: Load the model
def load_model():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError(f"Model file not found at {MODEL_PATH}")
    model = joblib.load(MODEL_PATH)
    app.logger.info("Model loaded successfully.")
    return model


# Step 2: Make predictions
def make_predictions():
    # Check if input file exists
    if not os.path.exists(INPUT_PATH):
        raise FileNotFoundError(f"Input file not found at {INPUT_PATH}")

    # Load the input data
    input_data = pd.read_csv(INPUT_PATH)
    app.logger.info("Input data loaded successfully.")

    # Load the model and make predictions
    model = load_model()
    predictions = model.predict(input_data)
    
    # Save predictions
    prediction_df = pd.DataFrame(predictions, columns=['predicted_quality'])
    prediction_df.to_csv(OUTPUT_PATH, index=False)
    app.logger.info(f"Predictions saved to {OUTPUT_PATH}")

    return predictions


# Step 3: Flask route for prediction
@app.route('/predict', methods=['GET'])
def predict():
    try:
        predictions = make_predictions()
        response = {
            "status": "success",
            "predictions": predictions.tolist()
        }
        return jsonify(response)

    except Exception as e:
        app.logger.error(f"Error during prediction: {e}")
        return jsonify({"status": "error", "message": str(e)}), 500


# Step 4: Add a root endpoint
@app.route('/')
def home():
    return "Model Inference Module is running! Visit /predict to get predictions."


# Step 5: Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True)
