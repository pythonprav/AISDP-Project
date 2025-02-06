import unittest
import pandas as pd
import numpy as np
from preprocess import preprocess_data_logic  # Import your preprocessing function

class TestPreprocessing(unittest.TestCase):

    def setUp(self):
        """
        Set up test data for all test cases.
        """
        # Sample dataset
        self.data = pd.DataFrame({
            'Sample': [1, 2, 3],
            'fixed_acidity': [7.4, 7.8, None],
            'volatile_acidity': [0.7, 0.88, 0.76],
            'color': ['red', 'white', 'red'],
            'quality': [5, None, 6]
        })

        # Expected output after cleaning
        self.cleaned_data = pd.DataFrame({
            'fixed_acidity': [7.4, 7.8],
            'volatile_acidity': [0.7, 0.88],
            'color': [0, 1],
            'quality': [3, 3]
        })

    def test_missing_values_handling(self):
        """
        Test that missing values are handled correctly.
        """
        df = self.data.copy()
        df_cleaned = preprocess_data_logic(df)
        self.assertFalse(df_cleaned.isnull().any().any(), "There should be no missing values after cleaning.")

    def test_column_dropping(self):
        """
        Test that unwanted columns are dropped.
        """
        df = self.data.copy()
        df_cleaned = preprocess_data_logic(df)
        self.assertNotIn('Sample', df_cleaned.columns, "Column 'Sample' should be dropped.")

    def test_duplicate_removal(self):
        """
        Test that duplicate rows are removed.
        """
        df = self.data.copy()
        df = pd.concat([df, df])  # Duplicate the rows
        df_cleaned = preprocess_data_logic(df)
        self.assertEqual(len(df_cleaned), 2, "Duplicates should be removed.")

    def test_label_encoding(self):
        """
        Test that 'color' column is correctly label-encoded.
        """
        df = self.data.copy()
        df_cleaned = preprocess_data_logic(df)
        self.assertIn('color', df_cleaned.columns, "Column 'color' should exist after preprocessing.")
        self.assertTrue(all(isinstance(x, int) for x in df_cleaned['color']), "Column 'color' should be label-encoded.")

    def test_quality_mapping(self):
        """
        Test that 'quality' column is correctly mapped to star ratings.
        """
        df = self.data.copy()
        df_cleaned = preprocess_data_logic(df)
        self.assertTrue(all(df_cleaned['quality'].isin([1, 2, 3, 4, 5])),
                        "Column 'quality' should be mapped to star ratings (1 to 5).")

    def test_edge_case_empty_dataset(self):
        """
        Test that an empty dataset is handled gracefully.
        """
        df = pd.DataFrame()  # Empty DataFrame
        df_cleaned = preprocess_data_logic(df)
        self.assertTrue(df_cleaned.empty, "An empty dataset should return an empty dataset after preprocessing.")

    def test_edge_case_unexpected_values(self):
        """
        Test that unexpected values (e.g., non-numeric) are handled correctly.
        """
        df = pd.DataFrame({
            'Sample': [1],
            'fixed_acidity': ['invalid'],  # Non-numeric value
            'volatile_acidity': [0.7],
            'color': ['red'],
            'quality': [5]
        })
        df_cleaned = preprocess_data_logic(df)
        self.assertTrue(np.isnan(df_cleaned['fixed_acidity'].iloc[0]), "Non-numeric values should be converted to NaN.")
        self.assertFalse(df_cleaned.isnull().any().any(), "All NaN rows should be removed after cleaning.")

    def test_quality_removal(self):
        """
        Test that rows with quality value of 2 are removed.
        """
        df = pd.DataFrame({
            'fixed_acidity': [7.4, 7.8, 7.9],
            'volatile_acidity': [0.7, 0.88, 0.76],
            'color': ['red', 'white', 'red'],
            'quality': [2, 3, 5]  # Includes a '2'
        })
        df_cleaned = preprocess_data_logic(df)
        self.assertNotIn(2, df_cleaned['quality'].values, "Rows with quality=2 should be removed.")

if __name__ == '__main__':
    unittest.main()
