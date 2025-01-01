# AISDP-Project\Model-Training\test_train_model.py

import pytest
import joblib
import requests
import os
import logging

# Configure logging
logging.basicConfig(level=logging.DEBUG, format="%(asctime)s - %(levelname)s - %(message)s")

# API endpoints
TRAIN_ENDPOINT = "http://localhost:5001/train"
METRICS_ENDPOINT = "http://localhost:5001/get-metrics"
SAVE_MODEL_ENDPOINT = "http://localhost:5001/save-model"

# Dataset path (ensure this matches the container's setup)
DATA_PATH = "../Data/wine_quality_assignment.csv"


def test_training_endpoint():
    """
    Test the /train endpoint to ensure it trains a model and saves it as model.pkl.
    """
    logging.info("Testing /train endpoint...")
    
    # Define the payload for the training endpoint
    payload = {"filepath": DATA_PATH}

    # Send POST request to the /train endpoint
    response = requests.post(TRAIN_ENDPOINT, json=payload)
    
    # Validate response
    assert response.status_code == 200, "Training endpoint did not return success."
    response_data = response.json()
    assert "message" in response_data and "Model trained successfully!" in response_data["message"], "Training response missing success message."
    assert "validation_metrics" in response_data, "Validation metrics are not included in the response."

    # Check if the model file was saved
    assert os.path.exists("model.pkl"), "Model file was not saved."

    # Load the saved model
    model = joblib.load("model.pkl")
    assert model is not None, "Trained model is None or invalid."


def test_metrics_endpoint():
    """
    Test the /get-metrics endpoint to ensure it returns validation metrics after training.
    """
    logging.info("Testing /get-metrics endpoint...")
    
    # Send GET request to the /get-metrics endpoint
    response = requests.get(METRICS_ENDPOINT)
    
    # Validate response
    assert response.status_code == 200, "Metrics endpoint did not return success."
    response_data = response.json()
    assert "accuracy" in response_data, "Accuracy is missing in metrics."
    assert "precision" in response_data, "Precision is missing in metrics."
    assert "recall" in response_data, "Recall is missing in metrics."
    assert "f1" in response_data, "F1 score is missing in metrics."


def test_save_model_endpoint():
    """
    Test the /save-model endpoint to ensure it saves the trained model upon request.
    """
    logging.info("Testing /save-model endpoint...")
    
    # Send POST request to the /save-model endpoint
    response = requests.post(SAVE_MODEL_ENDPOINT)
    
    # Validate response
    assert response.status_code == 200, "Save-model endpoint did not return success."
    response_data = response.json()
    assert "message" in response_data and "Model saved successfully!" in response_data["message"], "Save-model response missing success message."
    
    # Verify that the model file exists
    assert os.path.exists("model.pkl"), "Model file was not saved."


if __name__ == "__main__":
    # Run the tests
    pytest.main(["-v", "tests/test_train_model.py"])
