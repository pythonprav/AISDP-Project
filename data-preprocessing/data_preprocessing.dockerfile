# Data Preprocessing Dockerfile
FROM python:3.9-slim

# Set the working directory
WORKDIR /app

# Copy requirements and install
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code
COPY . .

# Create necessary directories
RUN mkdir -p /app/volumes/data /app/volumes/user

# Expose port 5000 for preprocessing
EXPOSE 5000

# Run the preprocessing app
CMD ["python", "preprocess.py"]