# Use Python base image with ARM64 compatibility
FROM python:3.10-slim

# Set the working directory
WORKDIR /app

# Install system dependencies including Firefox (ARM-compatible) and required libraries
RUN apt-get update && apt-get install -y \
    firefox-esr \
    wget \
    gnupg \
    libx11-xcb1 \
    libdbus-glib-1-2 \
    libxtst6 \
    libxrender1 \
    libgtk-3-0 \
    && rm -rf /var/lib/apt/lists/*

# Download the ARM64 version of geckodriver
RUN wget -q https://github.com/mozilla/geckodriver/releases/download/v0.33.0/geckodriver-v0.33.0-linux-aarch64.tar.gz \
    && tar -xvzf geckodriver-v0.33.0-linux-aarch64.tar.gz \
    && mv geckodriver /usr/local/bin/ \
    && rm geckodriver-v0.33.0-linux-aarch64.tar.gz

# Copy the application files into the container
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt

# Expose the port for Flask API
EXPOSE 5000

# Run the Flask application
CMD ["python", "app.py"]