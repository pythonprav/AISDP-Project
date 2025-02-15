# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy the requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

RUN apt-get update && apt-get install -y docker.io

# Copy the entire user-interface folder into the container
COPY . /app

# Expose port
EXPOSE 5003

# Run the Flask app
CMD ["python", "winequality_app.py"]