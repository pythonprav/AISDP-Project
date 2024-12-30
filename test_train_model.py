# tests/test_train.py
import pytest
import joblib
import requests
import os


def test_training_endpoint():
    """
    Test the /train endpoint in train_model.py to ensure it trains a model and saves it as model.pkl.
    """
    # Define the API endpoint and payload
    url = "http://localhost:5001/train"
    payload = {"filepath": "wine_quality_assignment.csv"}  # Ensure the file exists in the directory

    # Send POST request to trigger training
    response = requests.post(url, json=payload)
    
    # Validate the API response
    assert response.status_code == 200, "Training endpoint did not return success."
    response_data = response.json()
    assert "message" in response_data and "Model trained successfully!" in response_data["message"]
    assert "validation_metrics" in response_data, "Metrics are not included in the response."
    
    # Check that the model file is saved
    assert os.path.exists("model.pkl"), "Model file was not saved."
    
    # Load the model to ensure it is valid
    model = joblib.load("model.pkl")
    assert model is not None, "Trained model is None or invalid."


def test_metrics_endpoint():
    """
    Test the /get-metrics endpoint to ensure it returns validation metrics after training.
    """
    # Define the API endpoint
    url = "http://localhost:5001/get-metrics"
    
    # Send GET request to retrieve metrics
    response = requests.get(url)
    
    # Validate the API response
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
    # Define the API endpoint
    url = "http://localhost:5001/save-model"
    
    # Send POST request to save the model
    response = requests.post(url)
    
    # Validate the API response
    assert response.status_code == 200, "Save-model endpoint did not return success."
    response_data = response.json()
    assert "message" in response_data and "Model saved successfully!" in response_data["message"]
    
    # Verify that the model file exists
    assert os.path.exists("model.pkl"), "Model file was not saved."


if __name__ == "__main__":
    # Run the tests
    pytest.main(["-v", "test_train_model.py"])
