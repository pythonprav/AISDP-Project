# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Create necessary directories (ensures volume paths exist)
RUN mkdir -p /app/uploads /app/models

# Expose port 5000 for Flask
EXPOSE 5003

# Set environment variables for Flask and model storage
ENV FLASK_APP=winequality_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV MODEL_PATH=/app/models/saved_model.pkl
ENV UPLOAD_FOLDER=/app/uploads

# Command to run the Flask application
CMD ["flask", "run", "--host=0.0.0.0"]
