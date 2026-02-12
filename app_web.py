import streamlit as st
from streamlit_webrtc import webrtc_streamer

st.title("🚗 Monitor de Fadiga do Lincoln")
st.write("Se a imagem não aparecer, recarregue a página.")

# Versão ultra-simples para evitar o erro de 'AttributeError'
webrtc_streamer(
    key="monitor-lincoln", # Mudei a chave para forçar um novo início
    media_stream_constraints={"video": True, "audio": False},
)