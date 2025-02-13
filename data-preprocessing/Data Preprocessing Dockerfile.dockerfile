# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy necessary files into the container
COPY requirements.txt .  
COPY preprocess.py .  

# Ensure the required directories exist inside the container
RUN mkdir -p /app/data /app/raw_data /mnt/user

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Define a health check endpoint for Kubernetes
HEALTHCHECK --interval=30s --timeout=10s --retries=3 CMD curl --fail http://localhost:5000/health || exit 1

# Run the preprocessing application
CMD ["python", "preprocess.py"]
