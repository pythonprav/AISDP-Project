# Use Python 3.9 as base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all necessary files into the container
COPY . .

# Create directories for models and user uploads
RUN mkdir -p /app/volumes/models /app/volumes/user

# Expose port 5001
EXPOSE 5001

# Run the Flask application
CMD ["python", "inference.py"]