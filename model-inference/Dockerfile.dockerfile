# Model Inference Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and model to the container
COPY inference.py .
COPY model.pkl ./model.pkl  
# Replace 'model.pkl' with your model file name

# Expose the port for the inference API
EXPOSE 5002

# Define the command to run the inference API
CMD ["python", "inference.py"]
