import cv2
import streamlit as st
from streamlit_webrtc import webrtc_streamer, VideoProcessorBase, RTCConfiguration, WebRtcMode
import av
import numpy as np

# --- Page Configuration ---
st.set_page_config(page_title="TDMAU Pro", layout="wide", page_icon="🎓")

# --- Centered Header ---
st.markdown("<h1 style='text-align: center;'>TDMAU Pro</h1>", unsafe_allow_html=True)
st.markdown("<h3 style='text-align: center;'>Termiz davlat muhandislik va agrotexnologiyalar universiteti</h3>", unsafe_allow_html=True)

# --- Centered Logo (HTML Method) ---
image_url = "https://3cn91n41op.ucarecd.net/e88745d3-4a99-45ab-8d6a-274e6fccdd4d/IMG_20251014_180951_896.png"
st.markdown(f"""
<div style="display: flex; justify-content: center;">
    <img src="{image_url}" alt="University Logo" style="max-width: 100%; width: 70%;">
</div>
""", unsafe_allow_html=True)

# --- Centered Application ---
st.markdown("<h2 style='text-align: center;'>🎓 Teacher Presence Detector (Demo)</h2>", unsafe_allow_html=True)
st.markdown("<p style='text-align: center;'>Click 'Start' to enable the webcam and begin detecting.</p>", unsafe_allow_html=True)


# Load the face detector
face_cascade = cv2.CascadeClassifier(cv2.data.haarcascades + 'haarcascade_frontalface_default.xml')

class VideoProcessor(VideoProcessorBase):
    def recv(self, frame):
        img = frame.to_ndarray(format="bgr24")
        gray = cv2.cvtColor(img, cv2.COLOR_BGR_GRAY)
        faces = face_cascade.detectMultiScale(gray, 1.1, 4)

        for (x, y, w, h) in faces:
            cv2.rectangle(img, (x, y), (x+w, y+h), (0, 255, 0), 2)
            cv2.putText(img, "Teacher Present", (x, y-10), 
                        cv2.FONT_HERSHEY_SIMPLEX, 0.9, (0, 255, 0), 2)

        return av.VideoFrame.from_ndarray(img, format="bgr24")

# WEBRTC Configuration (with multiple STUN servers)
rtc_configuration = RTCConfiguration(
    {"iceServers": [
        {"urls": ["stun:stun.l.google.com:19302"]},
        {"urls": ["stun:stun1.l.google.com:19302"]},
        {"urls": ["stun:stun.services.mozilla.com"]}
    ]}
)

# --- Centered Web Component ---
col1, col2, col3 = st.columns([1, 5, 1])
with col2:
    webrtc_streamer(
        key="classroom-feed",
        mode=WebRtcMode.SENDRECV,
        rtc_configuration=rtc_configuration,
        video_processor_factory=VideoProcessor,
        media_stream_constraints={"video": True, "audio": False},
        async_processing=False  # Keep this as False for stability
    )

# --- Centered Footer (FIXED) ---
st.markdown("---")
# We must use pure HTML to get a centered link
footer_html = """
<p style='text-align: center;'>
    Copyright © Termez State University of Engineering and Agrotechnology / 
    <a href='https://instagram.com/iamumarsatti/' target='_blank'>IT Department</a>
</p>
"""
st.markdown(footer_html, unsafe_allow_html=True)
