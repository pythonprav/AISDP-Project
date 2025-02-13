import pandas as pd
import joblib
import os

def load_model():
    """Load the trained model from the Kubernetes PV directory"""
    model_path = '/mnt/AISDP-Project/model/saved_model.pkl'
    if not os.path.exists(model_path):
        raise FileNotFoundError(f"Model file not found at: {model_path}")
    model = joblib.load(model_path)
    print("\n--------------------------------------")
    print("Model loaded successfully!")
    print(f"Model Path: {model_path}")
    print("--------------------------------------\n")
    return model

def load_data():
    """Load the cleaned wine quality dataset from the data folder"""
    data_path = '../data/cleaned_wine_quality.csv'
    if not os.path.exists(data_path):
        raise FileNotFoundError(f"Data file not found at: {data_path}")
    df = pd.read_csv(data_path)

    print("\n--------------------------------------")
    print("Loaded cleaned dataset successfully!")
    print(f"Rows: {df.shape[0]} | Columns: {df.shape[1]}")
    print("Feature Columns:")
    print(", ".join(df.columns))
    print("--------------------------------------\n")

    return df

def make_predictions(model, data):
    """Generate predictions for the dataset"""
    try:
        predictions = model.predict(data.drop(columns=["color"], errors="ignore"))

        print("\n--------------------------------------")
        print(f"First 10 Predictions: {list(predictions[:10])}")
        print("--------------------------------------\n")

        data["predicted_quality"] = predictions

        output_path = '../data/predictions.csv'
        data.to_csv(output_path, index=False)

        print("\n--------------------------------------")
        print("Predictions saved successfully!")
        print(f"File Location: {output_path}")
        print("--------------------------------------\n")

    except Exception as e:
        print(f"Prediction failed: {e}")

def main():
    """Main function to run inference"""
    print("\n--------------------------------------")
    print("Starting Wine Quality Prediction Inference...")
    print("--------------------------------------\n")

    try:
        model = load_model()
        data = load_data()
        make_predictions(model, data)
    except Exception as e:
        print(f"\nAn error occurred: {e}")

if __name__ == "__main__":
    main()