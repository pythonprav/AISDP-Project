from flask import Flask, jsonify, request
import pandas as pd
import re
from sklearn.preprocessing import LabelEncoder
import os

app = Flask(__name__)

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

    # If dataset is empty after removing NaN, return an empty DataFrame
    if df.empty:
        return df

    # Remove duplicate rows
    df.drop_duplicates(inplace=True)

    # Remove rows where 'quality' equals 2
    if 'quality' in df.columns:
        df = df.dropna(subset=['quality'])  # Ensure NaN values are removed before filtering
        df.loc[:, 'quality'] = df['quality'].astype(int)  # Ensure quality is an integer
        df = df[df['quality'] != 2]  # Remove rows where quality is 2


    # If dataset is empty after filtering quality, return an empty DataFrame
    if df.empty:
        return df

    # Encode 'color' column if it exists
    if 'color' in df.columns:
        encoder = LabelEncoder()
        df.loc[:, 'color'] = encoder.fit_transform(df['color'])

    # Map 'quality' values to star ratings if it exists
    if 'quality' in df.columns:
        quality_map = {
            1: '1 Star', 2: '1 Star',
            3: '2 Star', 4: '2 Star',
            5: '3 Star', 6: '3 Star',
            7: '4 Star', 8: '4 Star',
            9: '5 Star', 10: '5 Star'
        }
        star_encoding = {'1 Star': 1, '2 Star': 2, '3 Star': 3, '4 Star': 4, '5 Star': 5}
        df.loc[:, 'quality'] = df['quality'].map(quality_map).map(star_encoding)

    return df

@app.route('/get-data', methods=['POST'])
def preprocess_data():
    """
    Flask route to preprocess incoming JSON data.
    """
    try:
        # Receive raw data via JSON
        data = request.get_json()

        # Validate input
        if not data:
            return jsonify({"error": "No data received"}), 400

        # Convert data to DataFrame
        df = pd.DataFrame(data)

        # Apply preprocessing logic
        df = preprocess_data_logic(df)

        # Check if dataset is empty after preprocessing
        if df.empty:
            return jsonify({"error": "Preprocessed dataset is empty"}), 400

        # Define output directory and ensure it exists
        output_dir = "Data"
        os.makedirs(output_dir, exist_ok=True)
        output_filepath = os.path.join(output_dir, "cleaned_wine_quality.csv")

        # Save the cleaned data to the Data folder
        df.to_csv(output_filepath, index=False)

        return jsonify({"message": f"Data preprocessed successfully! Cleaned file saved to {output_filepath}"})

    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
