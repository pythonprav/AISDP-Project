# Preprocessing Test (tests/test_preprocess.py)
# import pytest
import pandas as pd
from preprocess import preprocess_data

def test_preprocessing():
    data = {"feature1": [1, 2], "feature2": [3, None]}
    df = pd.DataFrame(data)
    result = preprocess_data(df)
    assert "feature1" in result.columns
    assert result.isna().sum().sum() == 0
