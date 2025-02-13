import joblib
import numpy as np
import pandas as pd
from flask import Flask, request, jsonify

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
MODEL_PATH = "saved_model.pkl"  # Change this if needed
try:
    model = joblib.load(MODEL_PATH)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Model loading failed: {e}")
    model = None  # Handle gracefully if the model is not found

# Feature columns (must match training)
FEATURE_COLUMNS = [
    "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
    "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide", "density",
    "pH", "sulphates", "alcohol", "color"
]

# Default Homepage
@app.route("/")
def home():
    return "Wine Quality Prediction API is running! Use /predict to send data."

# Prediction API Endpoint
@app.route("/predict", methods=["POST"])
def predict():
    try:
        # Get JSON input
        data = request.get_json()

        # Convert JSON to DataFrame
        df = pd.DataFrame(data)

        # Ensure feature columns are present
        if not all(col in df.columns for col in FEATURE_COLUMNS):
            return jsonify({"error": "Missing required features"}), 400
        
        # Convert 'color' (string) to numeric (0 = red, 1 = white) if needed
        if "color" in df.columns:
            df["color"] = df["color"].map({"red": 0, "white": 1})
            if df["color"].isnull().any():
                return jsonify({"error": "Invalid color values"}), 400

        # Ensure numeric conversion
        df = df[FEATURE_COLUMNS].astype(float)

        # Make predictions
        predictions = model.predict(df)

        # Return predictions
        return jsonify({"message": "Prediction successful", "predictions": predictions.tolist()})

    except Exception as e:
        return jsonify({"error": str(e), "message": "Prediction failed"}), 500

# Run the app
if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)