# Start from a stable Python 10 environment
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# 1. Update apt and install all the system dependencies
# This replaces packages.txt
RUN apt-get update && apt-get install -y \
    # For OpenCV
    libgl1 \
    libglib2.0-0 \
    # For PyAV (FFmpeg) build
    ffmpeg \
    pkg-config \
    libavformat-dev \
    libavcodec-dev \
    libavdevice-dev \
    libavutil-dev \
    libavfilter-dev \
    libswscale-dev \
    libswresample-dev \
    # Clean up
    && rm -rf /var/lib/apt/lists/*

# 2. Copy your requirements file and install Python packages
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 3. Copy the rest of your application code
COPY . .

# 4. Set the command to run your app
# We add --server.port $PORT so Render can route traffic
CMD ["streamlit", "run", "app.py", "--server.port", "10000"]
