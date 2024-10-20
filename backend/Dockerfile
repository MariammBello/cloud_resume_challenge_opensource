# Use an official Python runtime as a parent image
FROM python:3.9-slim

# Set/create the working directory in the container
WORKDIR /app

# Copy the current directory contents into the container at /app
COPY backend/ /app

# Install any needed packages specified in requirements.txt
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port the Flask app runs on
EXPOSE 5000

# Run app.py when the container launches
CMD ["python", "main.py"]
