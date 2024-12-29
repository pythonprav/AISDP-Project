# Data Preprocessing Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY preprocess.py .

# Expose the port the app runs on
EXPOSE 5000

# Define the command to run the application
CMD ["python", "preprocess.py"]
