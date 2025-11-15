import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration
import av
import numpy as np

# --- Page Configuration ---
# Use a wide layout and set the page title
st.set_page_config(page_title="TDMAU Pro", layout="wide", page_icon="🎓")

# --- Target UI Header ---
# This section mimics the header from the tdmau.netlify.app site

# 1. Main Title
st.title("TDMAU Pro")

# 2. Subtitle
st.subheader("Termiz davlat muhandislik va agrotexnologiyalar universiteti")

# 3. Banner Image (This is the URL from the site)
st.image("https://3cn91n41op.ucarecd.net/e88745d3-4a99-45ab-8d6a-274e6fccdd4d/IMG_20251014_180951_896.png")

# --- Your Application ---
# This is your video detector, now placed below the new header
st.header("🎓 Teacher Presence Detector (Demo)")
st.write("Click 'Start' to enable the webcam and begin detecting.")

# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        # Convert frame to OpenCV format
        img = frame.to_ndarray(format="bgr24")

        # Convert to grayscale for detection
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Detect Faces
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        # Draw rectangles
        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Teacher Present", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        # Return the processed frame back to the browser
        return av.VideoFrame.from_ndarray(img, format="bgr24")

# WEBRTC Configuration
rtc_configuration = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

# The Web Component
webrtc_streamer(
    key="classroom-feed",
    mode=1, # Send and Receive mode (This is the corrected line)
    rtc_configuration=rtc_configuration,
    video_processor_factory=VideoProcessor,
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
    # Make the video component wider to fit the new layout
    video_container_style={"border": "1px solid #e0e0e0", "border-radius": "8px", "overflow": "hidden"},
)

# --- Footer ---
# This is the updated footer with your text and hyperlink
st.markdown("---")
st.caption("Copyright © Termez State University of Engineering and Agrotechnology / [IT Department](https://instagram.com/iamumarsatti/#)")
