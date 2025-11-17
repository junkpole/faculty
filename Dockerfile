# Start from Debian Bookworm, which has newer ffmpeg libraries
FROM python:3.10-slim-bookworm

# Set a working directory
WORKDIR /app

# 1. Update apt and install all the system dependencies
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

# 3. (THIS IS THE FIX)
#    Upgrade pip to the latest version
RUN pip install --no-cache-dir --upgrade pip
RUN pip cache purge

# 4. Copy requirements file
COPY requirements.txt .

# 5. Install Python packages
#    The new pip will be able to resolve the dependencies correctly
RUN pip install --no-cache-dir -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Set the command to run your app
CMD ["streamlit", "run", "app.py", "--server.port", "10000"]
