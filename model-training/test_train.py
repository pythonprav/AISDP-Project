import unittest
import os
from train_model import load_data, split_data, train_random_forest

class TestModelTraining(unittest.TestCase):
    def setUp(self):
        self.filepath = "data/cleaned_wine_quality.csv"
        self.model_path = "model-training/random_forest_model.pkl"

    def test_load_data(self):
        data = load_data(self.filepath)
        self.assertFalse(data.empty, "Data should not be empty after loading.")

    def test_split_data(self):
        data = load_data(self.filepath)
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(data)
        self.assertGreater(len(X_train), 0, "Training set should not be empty.")
        self.assertGreater(len(X_val), 0, "Validation set should not be empty.")
        self.assertGreater(len(X_test), 0, "Test set should not be empty.")

    def test_train_and_save_model(self):
        data = load_data(self.filepath)
        X_train, X_val, X_test, y_train, y_val, y_test = split_data(data)
        model = train_random_forest(X_train, y_train)
        self.assertIsNotNone(model, "Model should be trained successfully.")
        model_path = self.model_path
        self.assertTrue(os.path.exists(model_path), f"Model should be saved at {model_path}.")

if __name__ == "__main__":
    unittest.main()