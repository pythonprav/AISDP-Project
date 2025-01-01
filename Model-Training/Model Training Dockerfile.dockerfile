#Model Training Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY Model-Training/train_model.py .
COPY ../Data/wine_quality_assignment.csv ./Data/wine_quality_assignment.csv

# Copy the requirements file to the container
COPY ../requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for rollback
ENV ROLLBACK_ENABLED=true

# Create a log directory
RUN mkdir /app/logs

# Expose the port for the API
EXPOSE 5001

# Define the command to run the training API
CMD ["python", "train_model.py"]
