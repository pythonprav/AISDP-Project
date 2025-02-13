import joblib
import pandas as pd
import os

# Define paths
model_path = "model-training/saved_model.pkl"
cleaned_data_path = "data/cleaned_wine_quality.csv"
output_path = "data/predictions.csv"

# Load trained model
try:
    model = joblib.load(model_path)
    print("Model loaded successfully!")
except Exception as e:
    print(f"Error loading model: {e}")

# Load cleaned dataset
try:
    cleaned_data = pd.read_csv(cleaned_data_path)

    # Extract features (drop the target column 'quality' if present)
    if "quality" in cleaned_data.columns:
        X_test = cleaned_data.drop(columns=["quality"])  # Drop target variable
    else:
        X_test = cleaned_data

    print(f"Loaded cleaned dataset: {X_test.shape}")
    print(f"📌 Feature columns: {list(X_test.columns)}")

    # Make predictions
    predictions = model.predict(X_test)

    # Add predictions to DataFrame
    cleaned_data["predicted_quality"] = predictions

    # Save predictions to CSV
    os.makedirs(os.path.dirname(output_path), exist_ok=True)
    cleaned_data.to_csv(output_path, index=False)
    print(f"Predictions saved to: {output_path}")

except Exception as e:
    print(f"Error during inference: {e}")