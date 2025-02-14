from flask import Flask, request, jsonify
import pandas as pd
import joblib
import os

app = Flask(__name__)

# Define file paths
MODEL_PATH = "/app/volumes/models/saved_model.pkl"
USER_INPUT_FILE = "/app/volumes/user/cleaned_input.csv"

# Load the model on startup
if os.path.exists(MODEL_PATH):
    model = joblib.load(MODEL_PATH)
else:
    raise FileNotFoundError(f"Model file not found at {MODEL_PATH}. Run model training first!")

@app.route('/predict', methods=['POST'])
def predict():
    """
    Handle predictions for new user-provided data.
    """
    try:
        # Ensure the user input file exists
        if not os.path.exists(USER_INPUT_FILE):
            return jsonify({"error": "No cleaned input file found. Please upload and preprocess input data."}), 400

        # Load the cleaned input data
        df = pd.read_csv(USER_INPUT_FILE)

        # Make predictions
        predictions = model.predict(df)

        # Attach predictions to the dataframe
        df['predicted_quality'] = predictions

        # Save the prediction results
        prediction_file = "/app/volumes/user/predictions.csv"
        df.to_csv(prediction_file, index=False)

        return jsonify({
            "message": "Predictions generated successfully.",
            "prediction_file": prediction_file,
            "predictions_preview": df.head(5).to_dict(orient='records')
        })

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)