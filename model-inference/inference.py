from flask import Flask, jsonify, request
import pandas as pd
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model_path = "model-training/optimized_rf_model.pkl"
model = joblib.load(model_path)

# Load feature names
feature_names_path = "data/feature_names.csv"
feature_names = pd.read_csv(feature_names_path)["feature_name"].tolist()

# Define quality mapping
quality_map = {
    1: "1 (Very Poor)", 2: "2 (Poor)", 3: "3 (Average)",
    4: "4 (Good)", 5: "5 (Excellent)"
}

@app.route("/predict-wine-quality", methods=["POST"])
def predict():
    """
    Predict wine quality based on user input.
    """
    try:
        # Get JSON data from request
        input_data = request.get_json()

        # Convert JSON to DataFrame using feature names
        input_df = pd.DataFrame([input_data], columns=feature_names)

        # Make prediction
        prediction = model.predict(input_df)[0]  # Extract first prediction
        
        # Convert numeric prediction to readable text
        quality_label = quality_map.get(prediction, f"{prediction} (Unknown)")

        return jsonify({
            "message": "Prediction successful",
            "predicted_quality": quality_label
        })

    except Exception as e:
        return jsonify({
            "message": "Prediction failed",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)