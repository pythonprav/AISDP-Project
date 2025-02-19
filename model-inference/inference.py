from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os
import json

app = Flask(__name__)

# Directory
BASE_DIR = "/mnt/data" if os.path.exists("/mnt/data") else "/app/volumes"

# File paths 
MODEL_PATH = os.getenv("MODEL_PATH", os.path.join(BASE_DIR, "models/saved_model.pkl"))
INPUT_PATH = os.getenv("INPUT_PATH", os.path.join(BASE_DIR, "user/cleaned_input.csv"))
OUTPUT_PATH = os.getenv("OUTPUT_PATH", os.path.join(BASE_DIR, "user/predictions.json"))


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

        # Make Predictions
        predictions = model.predict(df)

        # Combine predictions with input features
        results = df.copy()
        results["predicted_quality"] = predictions

        print("🔍 DEBUG: Predictions DataFrame before saving:\n", results.head())

        # Save full predictions JSON structure
        output_data = {
            "message": "Predictions generated successfully.",
            "output_path": OUTPUT_PATH,
            "predictions_preview": results.to_dict(orient="records")
            }
        
        # Write to file
        with open(OUTPUT_PATH, 'w') as json_file:
            json.dump(output_data, json_file, indent=4)

        # Return structured JSON for UI
        return jsonify({
            "message": "Predictions generated successfully.",
            "output_path": OUTPUT_PATH,
            "predictions_preview": results.head().to_dict(orient="records")  
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv("PORT", 5001)))