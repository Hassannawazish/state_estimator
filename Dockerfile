# Use official Python base image
FROM python:3.10-slim

# Set working directory
WORKDIR /app

# Install minimal dependencies (no GUI)
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

# Install Python packages
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files
COPY . .

# Set default command (can be overridden)
CMD ["python", "localization.py"]