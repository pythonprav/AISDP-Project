# Model Training (train_model.py)
from flask import Flask, jsonify, request
import pandas as pd
from sklearn.ensemble import RandomForestClassifier
import joblib

app = Flask(__name__)

@app.route('/train', methods=['POST'])
def train_model():
    # Load preprocessed training data
    train_data = pd.read_csv("train_data.csv")
    
    # Features and target
    X = train_data.drop('quality', axis=1)
    y = train_data['quality']
    
    # Train a Random Forest model
    model = RandomForestClassifier(n_estimators=100, random_state=42)
    model.fit(X, y)
    
    # Save the trained model
    joblib.dump(model, "model.pkl")
    
    return jsonify({"message": "Model trained successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5001)
