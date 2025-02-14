# # #Model Training Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY model-training/train_model.py ./  
COPY model-training/requirements.txt ./  

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for rollback and flexibility
ENV ROLLBACK_ENABLED=true
ENV TRAINING_FILE_PATH="/volumes/data/clean_wine_quality.csv"
ENV PYTHONUNBUFFERED=1
ENV LOG_LEVEL=DEBUG
ENV SAVED_MODEL_DIR="/volumes/models/saved_model.pkl"

# Expose the port for the API
EXPOSE 5001

# Add healthcheck for container status
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s \
  CMD curl --fail http://localhost:5001/health || exit 1

# Define the command to run the training API
CMD ["python", "./train_model.py"]


# 2nd old code
# # Model Training Dockerfile
# # Use an official Python runtime as the base image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # Copy the application code to the container
# COPY Model-Training/train_model.py ./Model-Training/
# # RUN mkdir -p /app/data /app/logs /app/outputs
# COPY /mnt/data/clean_wine_quality.csv ./mnt/data/clean_wine_quality.csv

# # Copy the requirements file to the container
# COPY Model-Training/requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Set environment variables for rollback and flexibility
# ENV ROLLBACK_ENABLED=true
# ENV TRAINING_FILE_PATH="/mnt/data/clean_wine_quality.csv"
# ENV PYTHONUNBUFFERED=1
# ENV LOG_LEVEL=DEBUG
# ENV SAVED_MODEL_DIR = "/mnt/models/saved_model.pkl"
# # Create directories for logs and outputs
# RUN mkdir -p /app/logs /app/outputs

# # Expose the port for the API
# EXPOSE 5001

# # Add healthcheck for container status
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl --fail http://localhost:5001/get-metrics || exit 1

# # Define the command to run the training API
# CMD ["python", "./Model-Training/train_model.py"]

# ========================================================

#OLD WORKING CODE
# # Use an official Python runtime as the base image
# FROM python:3.9-slim

# # Set the working directory in the container
# WORKDIR /app

# # # Copy the application code to the container
# # COPY Model-Training/train_model.py .
# # COPY ../Data/wine_quality_assignment.csv ./Data/wine_quality_assignment.csv

# # Copy the application code to the container
# COPY Model-Training/train_model.py ./Model-Training/
# COPY Data/wine_quality_assignment.csv ./Data/

# # Copy the requirements file to the container
# COPY ../requirements.txt .

# # Install dependencies
# RUN pip install --no-cache-dir -r requirements.txt

# # Set environment variables for rollback and flexibility
# ENV ROLLBACK_ENABLED=true
# ENV DATA_PATH="./Data/wine_quality_assignment.csv"
# ENV PYTHONUNBUFFERED=1
# ENV LOG_LEVEL=DEBUG

# # Create directories for logs and outputs
# RUN mkdir -p /app/logs /app/outputs

# # Expose the port for the API
# EXPOSE 5001

# # Add healthcheck for container status
# HEALTHCHECK --interval=30s --timeout=10s --start-period=5s CMD curl --fail http://localhost:5001/get-metrics || exit 1

# # Define the command to run the training API
# CMD ["python", "./Model-Training/train_model.py"]
