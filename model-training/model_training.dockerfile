# Use an official Python runtime as the base image
FROM python:3.9-slim

# Set the working directory in the container
WORKDIR /app

# Copy the application code to the container
COPY . /app/

# Ensure directories for logs, outputs, and models
RUN mkdir -p /app/volumes/data /app/volumes/models /app/logs /app/outputs

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Set environment variables for model training
ENV TRAINING_FILE_PATH="/app/volumes/data/cleaned_wine_quality.csv"
ENV SAVED_MODEL_PATH="/app/volumes/models/saved_model.pkl"
ENV LOG_LEVEL=DEBUG

# Expose the port for the training application
EXPOSE 5001

# Run the model training script
CMD ["python", "train_model.py"]