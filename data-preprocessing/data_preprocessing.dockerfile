# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory inside the container
WORKDIR /app

# Copy the entire data-preprocessing folder (including data and scripts)
COPY . /app/

# Ensure the 'data' directory exists
RUN mkdir -p /app/data

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the Flask app port
EXPOSE 5000

# Copy the dataset into the container
COPY raw_data /app/raw_data

# Run the preprocessing application
CMD ["python", "preprocess.py"]