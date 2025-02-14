# Use Python 3.9-slim as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy all files from the current directory to the container
COPY . .

# Create directories for models and user predictions
RUN mkdir -p /app/volumes/models /app/volumes/user

# Expose port 5001 for inference
EXPOSE 5001

# Run the inference service
CMD ["python", "inference.py"]