# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy and install dependencies (optimized for caching)
COPY requirements.txt requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files into the container
COPY . .

# Create directories for persistent storage (inside container)
RUN mkdir -p /app/volumes/data /app/volumes/user

# Expose the application port (needed for Flask API)
EXPOSE 5000

# Default command to run Flask app
CMD ["python", "preprocess.py"]