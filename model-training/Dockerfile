#Model Training Dockerfile
# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the requirements file to the container
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the application code to the container
COPY train_model.py .
COPY data/ /app/data/

# Expose the port for the API
EXPOSE 5001

# Define the command to run the training API
CMD ["python", "train_model.py"]