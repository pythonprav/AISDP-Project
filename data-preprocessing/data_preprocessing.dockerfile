# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Install curl (for health checks and testing inside container)
RUN apt-get update && \
    apt-get install -y --no-install-recommends curl && \
    apt-get clean && rm -rf /var/lib/apt/lists/*

# Copy and install dependencies
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files
COPY . .

# Create directories for volumes
RUN mkdir -p /app/volumes/data /app/volumes/user

# Expose port for Flask
EXPOSE 5000

# Default command to run Flask app
CMD ["python", "preprocess.py"]