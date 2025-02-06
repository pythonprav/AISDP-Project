# Use an official Python runtime as a parent image
FROM python:3.9

# Set the working directory inside the container
WORKDIR /app

# Copy application files into the container
COPY . .

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose port 5000 (Flask default)
EXPOSE 5000

# Set environment variables for Flask
ENV FLASK_APP=winequality_app.py
ENV FLASK_RUN_HOST=0.0.0.0
ENV MODEL_FILE_PATH=/app/my_wine_model.joblib  # Pass the model file path

# Command to run the Flask app
CMD ["flask", "run", "--host=0.0.0.0"]
