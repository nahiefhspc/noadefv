# Use the official Python image from DockerHub
FROM python:3.11-slim

# Set the working directory
WORKDIR /app

# Copy the requirements.txt to the container
COPY requirements.txt /app/requirements.txt

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of your application files to the container
COPY . /app

# Expose the port for Flask (default 5000)
EXPOSE 5000

# Command to run your application using Flask
CMD ["flask", "run", "--host=0.0.0.0"]
