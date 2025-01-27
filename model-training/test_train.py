# tests/test_train.py
# import pytest
import joblib
from train_model import train_model

def test_training():
    train_model()
    model = joblib.load("model.pkl")
    assert model is not None
