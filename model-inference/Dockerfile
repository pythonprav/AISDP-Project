# Dockerfile for Wine Quality Inference

# Use official Python image
FROM python:3.12-slim

# Set working directory
WORKDIR /app

# Copy necessary files
COPY . .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port for the API
EXPOSE 5000

# Run the inference API
CMD ["python", "inference.py"]