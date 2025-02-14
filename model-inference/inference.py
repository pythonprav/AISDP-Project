from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Define file paths
MODEL_PATH = "volumes/models/saved_model.pkl"
INPUT_PATH = "volumes/user/cleaned_input.csv"
OUTPUT_PATH = "volumes/user/predictions.json"


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests."""
    try:
        # Check if model file exists
        if not os.path.exists(MODEL_PATH):
            return jsonify({"error": f"Model file not found at {MODEL_PATH}"}), 500

        # Load the model
        model = joblib.load(MODEL_PATH)

        # Check if input file exists
        if not os.path.exists(INPUT_PATH):
            return jsonify({"error": f"Input file not found at {INPUT_PATH}"}), 400

        # Load and predict
        df = pd.read_csv(INPUT_PATH)
        predictions = model.predict(df)

        # Save predictions to JSON
        predictions_df = pd.DataFrame(predictions, columns=["predicted_quality"])
        predictions_df.to_json(OUTPUT_PATH, orient="records")

        return jsonify({
            "message": "Predictions generated successfully.",
            "predictions_preview": predictions_df.head().to_dict(orient="records"),
            "output_path": OUTPUT_PATH
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)