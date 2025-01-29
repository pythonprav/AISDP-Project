# Web Application Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code and static files to the container
COPY app.py .
COPY templates/ ./templates/
COPY static/ ./static/

# Expose the port for the web app
EXPOSE 5003

# Define the command to run the web application
CMD ["python", "app.py"]



# version: '3'
# services:
#   model-service:
#     build: ./model_service
#     container_name: model-service
#     ports:
#       - "5001:5001"

#   flask-app:
#     build: ./flask_app
#     container_name: flask-app
#     ports:
#       - "5000:5000"
#     depends_on:
#       - model-service

