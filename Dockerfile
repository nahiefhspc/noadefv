FROM python:3.11-slim

# Set working directory
WORKDIR /app

# Copy requirements.txt
COPY requirements.txt .

# Install dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Copy the rest of the application files
COPY . .

# Set the Flask app environment variable
ENV FLASK_APP=app.py

# Expose the app port
EXPOSE 8080

# Run Flask
CMD ["flask", "run", "--host=0.0.0.0", "--port=8080"]
