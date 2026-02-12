import streamlit as st
from streamlit_webrtc import webrtc_streamer, WebRtcMode, RTCConfiguration

# 1. Configuração para furar o bloqueio de conexão do celular (STUN)
# Agora usando o nome correto que o Streamlit espera
RTC_CONFIGURATION = RTCConfiguration(
    {"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]}
)

st.title("🚗 Monitor de Fadiga do Lincoln")
st.write("Abra este link no celular para testar!")

# 2. O comando que abre a câmera
webrtc_streamer(
    key="detector",
    mode=WebRtcMode.SENDRECV,
    rtc_configuration=RTC_CONFIGURATION, # Nome corrigido aqui
    video_frame_callback=None, 
    media_stream_constraints={"video": True, "audio": False},
    async_processing=True,
)