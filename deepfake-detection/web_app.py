import streamlit as st
import tempfile
import cv2
import numpy as np
import matplotlib.pyplot as plt
from detector import DeepfakeDetector
from utils.audio_processor import analyze_voice
from utils.video_processor import temporal_scores, frequency_score

st.set_page_config(
    page_title="Advanced Deepfake Detection",
    layout="wide"
)

# ---------------- INIT ----------------
if "mode" not in st.session_state:
    st.session_state.mode = None

detector = DeepfakeDetector({
    "detection_threshold": 0.7,
    "selected_model": "mesonet",
    "enable_ensemble": True
})

st.markdown("## 🔍 Advanced Deepfake Detection System")

# ---------------- MODE SELECTION ----------------
col1, col2, col3 = st.columns(3)

with col1:
    if st.button("🎥 VIDEO", use_container_width=True):
        st.session_state.mode = "video"

with col2:
    if st.button("🖼 IMAGE", use_container_width=True):
        st.session_state.mode = "image"

with col3:
    if st.button("🎙 VOICE", use_container_width=True):
        st.session_state.mode = "voice"

st.divider()

# ================= VIDEO =================
if st.session_state.mode == "video":
    st.subheader("🎥 Video Deepfake Detection")

    video = st.file_uploader(
        "Upload video",
        type=["mp4", "avi", "mov"]
    )

    if video:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(video.read())
            path = f.name

        st.video(video)

        if st.button("Analyze Video"):
            with st.spinner("Analyzing video..."):
                result = detector.analyze_video(path)

            if result["success"]:
                st.success(f"Verdict: {result['verdict']}")
                st.metric("Confidence", f"{result['confidence']:.2f}")

                # Temporal graph
                temp = temporal_scores(path)
                st.subheader("📊 Temporal Consistency")
                st.line_chart(temp)

            else:
                st.error(result["error"])

# ================= IMAGE =================
elif st.session_state.mode == "image":
    st.subheader("🖼 Image Deepfake Detection")

    image = st.file_uploader(
        "Upload image",
        type=["jpg", "png", "jpeg"]
    )

    if image:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(image.read())
            path = f.name

        img = cv2.imread(path)
        st.image(img, channels="BGR")

        if st.button("Analyze Image"):
            with st.spinner("Analyzing image..."):
                result = detector.analyze_image(path)

            if result["success"]:
                st.success(f"Verdict: {result['verdict']}")
                st.metric("Confidence", f"{result['confidence']:.2f}")

                freq = frequency_score(img)
                st.subheader("📊 Frequency Artifacts")
                st.bar_chart(freq)

            else:
                st.error(result["error"])

# ================= VOICE =================
elif st.session_state.mode == "voice":
    st.subheader("🎙 Voice Deepfake Detection")

    audio = st.file_uploader(
        "Upload audio",
        type=["wav", "mp3"]
    )

    if audio:
        with tempfile.NamedTemporaryFile(delete=False) as f:
            f.write(audio.read())
            path = f.name

        st.audio(audio)

        if st.button("Analyze Voice"):
            with st.spinner("Analyzing voice..."):
                result = analyze_voice(path)

            st.success(f"Verdict: {result['verdict']}")
            st.metric("Confidence", f"{result['confidence']:.2f}")

            st.subheader("📊 Spectral Features")
            st.line_chart(result["spectral"])
