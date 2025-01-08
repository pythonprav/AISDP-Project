from flask import Flask, request, jsonify
import joblib
import traceback

# Initialize Flask app
app = Flask(__name__)

# Mock model for testing purposes
class MockModel:
    def predict(self, X):
        # Simulate predictions (random wine quality values between 3 and 9)
        return np.random.randint(3, 10, size=len(X))

# Initialize the mock model
model = MockModel()
print("Using a mock model for testing.")

# Define the /predict endpoint
@app.route('/predict', methods=['POST'])
def predict():
    if model is None:
        return jsonify({"error": "Model not loaded"}), 500

    try:
        # Parse the input JSON
        input_data = request.get_json()

        # Define the feature columns (update as per your dataset)
        feature_columns = [
            "fixed_acidity", "volatile_acidity", "citric_acid", "residual_sugar",
            "chlorides", "free_sulfur_dioxide", "total_sulfur_dioxide",
            "density", "pH", "sulphates", "alcohol"
        ]

        # Extract feature values in the correct order
        feature_values = [input_data.get(col) for col in feature_columns]
        if None in feature_values:
            missing_cols = [col for col, val in zip(feature_columns, feature_values) if val is None]
            return jsonify({"error": f"Missing or invalid features: {', '.join(missing_cols)}"}), 400

        # Make prediction
        prediction = model.predict([feature_values])[0]

        # Return the prediction as JSON
        return jsonify({"prediction": prediction})

    except Exception as e:
        print(f"Error during prediction: {e}")
        return jsonify({"error": "Prediction failed", "details": traceback.format_exc()}), 500

# Run the Flask app
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)