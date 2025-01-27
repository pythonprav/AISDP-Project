# tests/test_inference.py
# import pytest
import requests

def test_inference():
    response = requests.post(
        "http://localhost:5002/predict",
        json={"feature1": 1, "feature2": 3}
    )
    assert response.status_code == 200
    assert "prediction" in response.json()
