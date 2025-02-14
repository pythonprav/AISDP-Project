# Use Python 3.9 as the base image
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements file and install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code into the container
COPY . .

# Create necessary directories for persistent storage
RUN mkdir -p /app/volumes/data /app/volumes/user

# Expose the application port
EXPOSE 5000

# Run the preprocessing application
CMD ["python", "preprocess.py"]