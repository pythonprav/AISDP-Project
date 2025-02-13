from flask import Flask, jsonify, request
import pandas as pd
import re
import json
import os
from sklearn.preprocessing import LabelEncoder

app = Flask(__name__)

def convert_csv_to_json():
    """
    Converts wine_quality_assignment.csv to JSON and saves it in the data folder.
    """
    csv_file = "data/wine_quality_assignment.csv"
    json_file = "data/wine_quality.json"

    # Ensure the data directory exists
    os.makedirs("data", exist_ok=True)

    # Read CSV and convert to JSON
    df = pd.read_csv(csv_file)
    data_json = df.to_dict(orient='records')

    with open(json_file, "w") as json_output:
        json.dump(data_json, json_output, indent=4)

    print(f"CSV has been converted to JSON and saved to {json_file}")
    return json_file

def clean_column(column):
    """
    Clean non-numeric values in a column by removing invalid characters.
    """
    return column.apply(lambda x: re.sub(r'[^\d\.]', '', str(x)) if isinstance(x, str) else x)

def preprocess_data_logic(df):
    """
    Perform data cleaning and preprocessing on the DataFrame.
    """
    # Drop unwanted column 'Sample' if it exists
    if 'Sample' in df.columns:
        df.drop(columns=['Sample'], inplace=True)

    # Clean numeric columns
    for col in df.columns:
        if col not in ['color', 'quality']:  # Exclude categorical/target columns
            df[col] = clean_column(df[col])  # Remove non-numeric characters
            df[col] = pd.to_numeric(df[col], errors='coerce')  # Convert to numeric

    # Handle missing values
    df.dropna(inplace=True)

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove rows where 'quality' equals 2
    if 'quality' in df.columns:
        df = df[df['quality'] != 2].copy()  # Explicitly create a copy

    # Encode 'color' column if it exists
    if 'color' in df.columns:
        encoder = LabelEncoder()
        df.loc[:, 'color'] = encoder.fit_transform(df['color'])  # Use .loc for modification

    # Map 'quality' values to star ratings if it exists
    if 'quality' in df.columns:
        quality_map = {
            1: '1 Star', 2: '1 Star',
            3: '2 Star', 4: '2 Star',
            5: '3 Star', 6: '3 Star',
            7: '4 Star', 8: '4 Star',
            9: '5 Star', 10: '5 Star'
        }
        star_encoding = {
            '1 Star': 1,
            '2 Star': 2,
            '3 Star': 3,
            '4 Star': 4,
            '5 Star': 5
        }
        df.loc[:, 'quality'] = df['quality'].map(quality_map).map(star_encoding).astype(int)

    return df

@app.route('/get-data', methods=['POST'])
def preprocess_data():
    """
    Flask route to convert CSV to JSON and preprocess JSON data.
    """
    try:
        # Step 1: Convert CSV to JSON and get the JSON file path
        json_file = convert_csv_to_json()

        # Step 2: Read the JSON file
        with open(json_file, "r") as file:
            data = json.load(file)

        # Step 3: Convert JSON data to DataFrame
        df = pd.DataFrame(data)

        # Step 4: Apply preprocessing logic
        df = preprocess_data_logic(df)

        # Step 5: Save the cleaned dataset to CSV
        cleaned_csv = "data/cleaned_wine_quality.csv"
        df.to_csv(cleaned_csv, index=False)

        return jsonify({
            "message": f"CSV successfully converted to JSON at {json_file}. Data preprocessed successfully! Cleaned file saved to {cleaned_csv}"
        })
    
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
