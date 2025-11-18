# We use Python 3.9 on Debian Bullseye
# This specific version allows us to download pre-built binaries
# instead of trying (and failing) to build them ourselves.
FROM python:3.9-slim-bullseye

WORKDIR /app

# We only need the basic libraries for OpenCV now
# No need for ffmpeg-dev or compilers because we will use binary wheels
RUN apt-get update && apt-get install -y \
    libgl1-mesa-glx \
    libglib2.0-0 \
    && rm -rf /var/lib/apt/lists/*

COPY requirements.txt .

# Upgrade pip to ensure we can download the binary wheels
RUN pip install --no-cache-dir --upgrade pip

# Install the packages
RUN pip install --no-cache-dir -r requirements.txt

COPY . .

CMD ["streamlit", "run", "app.py", "--server.port", "10000"]
