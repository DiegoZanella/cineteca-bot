# Use Python base image
FROM python:3.10-slim

# Set the working directory in the container
WORKDIR /app

# Install system dependencies required for MariaDB and requests
RUN apt-get update && apt-get install -y \
    libmariadb-dev \
    libmariadb-dev-compat \
    gcc \
    locales \
    && rm -rf /var/lib/apt/lists/*

# Generate and set the Spanish locale
RUN apt-get update && apt-get install -y locales && \
    echo "es_ES.UTF-8 UTF-8" >> /etc/locale.gen && \
    locale-gen es_ES.UTF-8
ENV LANG es_ES.UTF-8
ENV LANGUAGE es_ES:es
ENV LC_ALL es_ES.UTF-8


# Copy application files
COPY . /app

# Install Python dependencies
RUN pip install --no-cache-dir -r /app/requirements.txt

# Expose the Flask API port
EXPOSE 5002

# Start the bot service
CMD ["python", "bot.py"]
