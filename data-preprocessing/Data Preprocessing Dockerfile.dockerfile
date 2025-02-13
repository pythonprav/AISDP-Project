# Data Preprocessing Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy only the necessary files to improve efficiency
COPY requirements.txt .  
COPY preprocess.py .   

# Ensure the required directories exist inside the container
RUN mkdir -p /app/data /app/raw_data /mnt/user

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Run the preprocessing application
CMD ["python", "preprocess.py"]
