import streamlit as st
from streamlit_webrtc import webrtc_streamer, RTCConfiguration

# Configuração para garantir que o vídeo chegue no celular
RTC_CONFIG = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.title("🚗 Monitor de Fadiga do Lincoln")
st.write("Se a imagem não aparecer, clique em START e aceite a câmera.")

# Versão simplificada que evita o erro de 'import cv2'
webrtc_streamer(
    key="monitor",
    rtc_configuration=RTC_CONFIG,
    media_stream_constraints={"video": True, "audio": False},
)