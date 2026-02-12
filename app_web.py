import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# Configuração para furar o bloqueio de conexão do celular
rtc_configuration = {
    "iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]
}

st.title("🚗 Monitor de Fadiga do Lincoln")

webrtc_streamer(
    key="detector",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION,
    video_frame_callback=None, # Por enquanto apenas para testar se a imagem abre
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)