from flask import Flask, jsonify, request
import pandas as pd
import joblib

# Initialize Flask app
app = Flask(__name__)

# Load the trained model
model_path = "model-training/optimized_rf_model.pkl"
model = joblib.load(model_path)

# Extract feature names dynamically from the preprocessed dataset
data_path = "data/cleaned_wine_quality.csv"
df = pd.read_csv(data_path)
feature_names = df.drop(columns=["quality"]).columns.tolist()

@app.route("/predict", methods=["POST"])
def predict():
    """
    Predict the wine quality using the trained model.
    """
    try:
        # Parse the input JSON data
        input_data = request.get_json()
        
        # Convert JSON to DataFrame
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