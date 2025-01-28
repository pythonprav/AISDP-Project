import pandas as pd

# Load the preprocessed dataset
data_path = "data/cleaned_wine_quality.csv"
df = pd.read_csv(data_path)

# Extract feature names (exclude the target column "quality")
feature_names = df.drop(columns=["quality"]).columns.tolist()

# Save the feature names to a CSV
feature_names_df = pd.DataFrame(feature_names, columns=["feature_name"])
feature_names_df.to_csv("data/feature_names.csv", index=False)

print("Feature names saved to data/feature_names.csv!")