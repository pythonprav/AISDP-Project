from flask import Flask, jsonify, request
import pandas as pd
import re
import json
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

DATA_FOLDER = "data"

def convert_csv_to_json():
    """
    Converts wine_quality_assignment.csv to JSON and saves it in the data folder.
    """
    csv_file = os.path.join(DATA_FOLDER, "wine_quality_assignment.csv")
    json_file = os.path.join(DATA_FOLDER, "wine_quality.json")

    # Ensure the data directory exists
    os.makedirs(DATA_FOLDER, exist_ok=True)

    # Check if CSV exists
    if not os.path.exists(csv_file):
        raise FileNotFoundError(f"❌ CSV file not found at {csv_file}. Ensure it exists in the 'data' folder.")

    # Read CSV and convert to JSON
    df = pd.read_csv(csv_file)
    df.to_json(json_file, orient='records', indent=4)

    print(f"✅ CSV has been converted to JSON and saved to {json_file}")
    return json_file  # Return the JSON file path

# Ensure CSV is converted to JSON on startup
json_file_path = convert_csv_to_json()

def clean_column(column):
    """
    Clean non-numeric values in a column by removing invalid characters.
    """
    return column.apply(lambda x: re.sub(r'[^\d\.]', '', str(x)) if isinstance(x, str) else x)

def preprocess_data_logic(df):
    """
    Perform data cleaning and preprocessing on the DataFrame.
    """
    if 'Sample' in df.columns:
        df.drop(columns=['Sample'], inplace=True)

    for col in df.columns:
        if col not in ['color', 'quality']:
            df[col] = clean_column(df[col])
            df[col] = pd.to_numeric(df[col], errors='coerce')

    df.dropna(inplace=True)
    df.drop_duplicates(inplace=True)

    if 'quality' in df.columns:
        df = df[df['quality'] != 2].copy()

    if 'color' in df.columns:
        encoder = LabelEncoder()
        df.loc[:, 'color'] = encoder.fit_transform(df['color'])

    if 'quality' in df.columns:
        quality_map = {1: 1, 2: 1, 3: 2, 4: 2, 5: 3, 6: 3, 7: 4, 8: 4, 9: 5, 10: 5}
        df.loc[:, 'quality'] = df['quality'].map(quality_map).astype(int)

    return df

@app.route('/get-data', methods=['POST'])
def preprocess_data():
    """
    Flask route to preprocess JSON data.
    """
    try:
        # Step 1: Read the JSON file
        with open(json_file_path, "r") as file:
            data = json.load(file)

        # Step 2: Convert JSON data to DataFrame
        df = pd.DataFrame(data)

        # Step 3: Apply preprocessing logic
        df = preprocess_data_logic(df)

        # Step 4: Save the cleaned dataset to CSV
        cleaned_csv = os.path.join(DATA_FOLDER, "cleaned_wine_quality.csv")
        df.to_csv(cleaned_csv, index=False)

        return jsonify({
            "message": f"✅ CSV converted to JSON at {json_file_path}. Data preprocessed successfully! Cleaned file saved to {cleaned_csv}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
