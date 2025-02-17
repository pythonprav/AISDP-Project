from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# File paths (Keep absolute paths as per Docker volume mapping)
MODEL_PATH = "/app/volumes/models/saved_model.pkl"
INPUT_PATH = "/app/volumes/user/cleaned_input.csv"
OUTPUT_PATH = "/app/volumes/user/predictions.json"


@app.route('/predict', methods=['POST'])
def predict():
    """Handle prediction requests and output structured JSON."""
    try:
        # Validate Model Path
        if not os.path.exists(MODEL_PATH):
            return jsonify({"error": f"Model file not found at {MODEL_PATH}"}), 500

        # Load the trained model
        model = joblib.load(MODEL_PATH)

        # Validate Input Path
        if not os.path.exists(INPUT_PATH):
            return jsonify({"error": f"Input file not found at {INPUT_PATH}"}), 400

        # Load Input CSV
        df = pd.read_csv(INPUT_PATH)

        # Drop 'Sample' if exists (since model was trained without it)
        if 'Sample' in df.columns:
            df.drop(columns=['Sample'], inplace=True)

        # Make Predictions
        predictions = model.predict(df)

        # Combine predictions with input features for detailed output
        results = df.copy()
        results["predicted_quality"] = predictions

        # Save predictions to JSON
        results.to_json(OUTPUT_PATH, orient="records", indent=4)

        # Return structured JSON for UI
        return jsonify({
            "message": "Predictions generated successfully.",
            "output_path": OUTPUT_PATH,
            "predictions_preview": results.head().to_dict(orient="records")
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)