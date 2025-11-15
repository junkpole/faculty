import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration, WebRtcMode # <-- Import WebRtcMode
import av
import numpy as np

# --- Page Configuration ---
# Use a wide layout and set the page title
st.set_page_config(page_title="TDMAU Pro", layout="wide", page_icon="🎓")

# --- Centered Header ---
# We use st.markdown with unsafe_allow_html=True to center the text
st.markdown("<h1 style='text-align: center;'>TDMAU Pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Termiz davlat muhandislik va agrotexnologiyalar universiteti</h3>", unsafe_allow_html=True)

# We use columns to center the image. [1, 5, 1] means the middle column is 5x wider
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    st.image("https://3cn91n41op.ucarecd.net/e88745d3-4a99-45ab-8d6a-274e6fccdd4d/IMG_20251014_180951_896.png")

# --- Centered Application ---
st.markdown("<h2 style='text-align: center;'>🎓 Teacher Presence Detector (Demo)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Click 'Start' to enable the webcam and begin detecting.</p>", unsafe_allow_html=True)


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

# --- Centered Web Component ---
# We put the video streamer inside the middle column
with col2:
    webrtc_streamer(
        key="classroom-feed",
        mode=WebRtcMode.SENDRECV, # <-- This line is corrected
        rtc_configuration=rtc_configuration,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=True
    )

# --- Footer ---
st.markdown("---")
st.caption("Copyright © Termez State University of Engineering and Agrotechnology / [IT Department](https://instagram.com/iamumarsatti/#)")
