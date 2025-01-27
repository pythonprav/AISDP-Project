# Model Inference (inference.py)
from flask import Flask, jsonify, request
import joblib
import pandas as pd

app = Flask(__name__)

# Load the saved model
model = joblib.load("model.pkl")

@app.route('/predict', methods=['POST'])
def predict():
    # Example: Receive input features via JSON
    input_data = request.get_json()
    df = pd.DataFrame([input_data])

    # Predict using the model
    prediction = model.predict(df)
    probability = model.predict_proba(df).max()

    return jsonify({
        "prediction": int(prediction[0]),
        "probability": float(probability)
    })

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5002)
