# Start from a stable Python 10 environment
FROM python:3.10-slim

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

# 3. (THIS IS THE FIX-PART-1)
#    Install the correct Cython version *before* installing requirements
RUN pip install --no-cache-dir Cython==0.29.37

# 4. Copy requirements file (which NO LONGER contains Cython)
COPY requirements.txt .

# 5. (THIS IS THE FIX-PART-2)
#    Install Python packages using --no-build-isolation
#    This forces pip to use the Cython we just installed
RUN pip install --no-cache-dir --no-build-isolation -r requirements.txt

# 6. Copy the rest of your application code
COPY . .

# 7. Set the command to run your app
CMD ["streamlit", "run", "app.py", "--server.port", "10000"]
