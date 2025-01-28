from flask import Flask, jsonify, request
import pandas as pd
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model_path = "model-training/optimized_rf_model.pkl"
model = joblib.load(model_path)

# Load feature names from the CSV
feature_names_path = "data/feature_names.csv"
feature_names = pd.read_csv(feature_names_path)["feature_name"].tolist()

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict wine quality using the trained model.
    """
    try:
        # Parse the input JSON data
        input_data = request.get_json()

        # Convert JSON to DataFrame using the feature names
        input_df = pd.DataFrame(input_data, columns=feature_names)
        
        # Make predictions
        predictions = model.predict(input_df).tolist()
        
        return jsonify({
            "message": "Prediction successful",
            "predictions": predictions
        })
    except Exception as e:
        return jsonify({
            "message": "Prediction failed",
            "error": str(e)
        }), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)