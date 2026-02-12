import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration
import cv2
from detector_sono import processar_frame # Importa sua lógica

RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.title("🚗 Monitor de Fadiga do Lincoln")

def video_frame_callback(frame):
    img = frame.to_ndarray(format="bgr24")
    # Chama a função que você criou no outro arquivo
    img_processada = processar_frame(img) 
    return av.VideoFrame.from_ndarray(img_processada, format="bgr24")

webrtc_streamer(
    key="detector",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_frame_callback=video_frame_callback, # Aqui a mágica acontece
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)