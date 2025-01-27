# Data Preprocessing (preprocess.py)
from flask import Flask, jsonify, request
import pandas as pd
from sklearn.model_selection import train_test_split

app = Flask(__name__)

@app.route('/get-data', methods=['POST'])
def preprocess_data():
    # Example: Receive raw data via JSON
    data = request.get_json()

    # Convert data to DataFrame
    df = pd.DataFrame(data)

    # Data cleaning and preprocessing
    df.fillna(df.mean(), inplace=True)  # Replace missing values with mean
    df = pd.get_dummies(df, drop_first=True)  # One-hot encoding
    
    # Split into train and test sets
    train_data, test_data = train_test_split(df, test_size=0.2, random_state=42)
    
    # Save preprocessed data for downstream tasks
    train_data.to_csv("train_data.csv", index=False)
    test_data.to_csv("test_data.csv", index=False)

    return jsonify({"message": "Data preprocessed successfully!"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
