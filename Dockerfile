# Start from a stable Python 10 environment
FROM python:3.10-slim

# Set a working directory
WORKDIR /app

# 1. Update apt and install all the system dependencies
#    ADDED 'build-essential' for C compilers
RUN apt-get update && apt-get install -y \
    # For building packages
    build-essential \
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

# 2. SET THE ENVIRONMENT VARIABLE
#    This tells pkg-config where to find the libraries
ENV PKG_CONFIG_PATH /usr/lib/x86_64-linux-gnu/pkgconfig:/usr/share/pkgconfig

# 3. Copy your requirements file and install Python packages
#    This line (previously #28) will now run AFTER the ENV
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# 4. Copy the rest of your application code
COPY . .

# 5. Set the command to run your app
CMD ["streamlit", "run", "app.py", "--server.port", "10000"]
