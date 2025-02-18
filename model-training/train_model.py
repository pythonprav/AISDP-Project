import pandas as pd
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import classification_report, accuracy_score
import pickle
import os

# Use environment variables for paths
DATA_PATH = os.getenv("DATA_PATH", "/app/volumes/data/cleaned_wine_quality.csv")
MODEL_PATH = os.getenv("MODEL_PATH", "/app/volumes/models/saved_model.pkl")

def load_data():
    """Load the cleaned dataset for model training."""
    if not os.path.exists(DATA_PATH):
        raise FileNotFoundError(f"{DATA_PATH} not found. Run preprocessing first.")
    df = pd.read_csv(DATA_PATH)
    return df

def train_model():
    """Train a RandomForest model and save it."""
    # Load the dataset
    df = load_data()

    # Separate features and target
    X = df.drop("quality", axis=1)
    y = df["quality"]

    # Split into training and test sets
    X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

    # Initialize and train the model
    model = RandomForestClassifier(random_state=42)
    model.fit(X_train, y_train)

    # Make predictions
    y_pred = model.predict(X_test)

    # Evaluate model
    accuracy = accuracy_score(y_test, y_pred)
    print(f"Model Accuracy: {accuracy:.2f}")

    # Classification report with zero_division to avoid warnings
    report = classification_report(y_test, y_pred, zero_division=1)
    print(report)

    # Save the model
    os.makedirs(os.path.dirname(MODEL_PATH), exist_ok=True)
    with open(MODEL_PATH, "wb") as f:
        pickle.dump(model, f)
    print(f"Model saved to {MODEL_PATH}")

if __name__ == "__main__":
    train_model()