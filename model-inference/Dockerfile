# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the inference script and any necessary files to the container
COPY inference.py .
COPY optimized_rf_model.pkl .
COPY ../data/feature_names.csv ./data/

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "inference.py"]
