import streamlit as st
from streamlit_webrtc import webrtc_streamer
import cv2
import mediapipe as mp

st.title("🚗 Monitor de Fadiga do Lincoln")
st.write("Abra este link no celular para testar!")

def transform(frame):
    img = frame.to_ndarray(format="bgr24")
    
    # Aqui vai a lógica que você já criou (MediaPipe)
    # Por enquanto, vamos apenas mostrar que a câmera funciona
    img = cv2.flip(img, 1)
    
    return img

webrtc_streamer(key="sample", video_frame_callback=transform)