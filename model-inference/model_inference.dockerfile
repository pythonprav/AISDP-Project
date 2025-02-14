# Base Python image
FROM python:3.9-slim

# Set working directory
WORKDIR /app

# Copy requirements and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application files
COPY . .

# Create necessary directories
RUN mkdir -p /app/volumes/models /app/volumes/user

# Expose the port
EXPOSE 6000

# Command to run the inference service
CMD ["python", "inference.py"]