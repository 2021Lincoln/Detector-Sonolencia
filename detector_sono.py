import cv2
import mediapipe as mp
import numpy as np
import winsound

# 1. Configurações MediaPipe
mp_drawing = mp.solutions.drawing_utils
mp_face_mesh = mp.solutions.face_mesh
face_mesh = mp_face_mesh.FaceMesh(refine_landmarks=True)

# --- PARÂMETROS DE AJUSTE REFINADOS ---
EAR_LIMIAR_SONOLENTO = 0.28  # Olho parcialmente fechado
EAR_LIMIAR_PERIGO = 0.21     # Olho completamente fechado
MAR_LIMIAR_BOCEJO = 0.50     # Boca aberta
LIMITE_FRAMES = 100          # Tamanho total da barra
CONTADOR_FRAMES = 0

OLHO_ESQ = [362, 385, 387, 263, 373, 380]
OLHO_DIR = [33, 160, 158, 133, 153, 144]
BOCA = [13, 14, 78, 308]

def calcular_ear(pontos, face_landmarks):
    coords = []
    for i in pontos:
        p = face_landmarks.landmark[i]
        coords.append(np.array([p.x, p.y]))
    d_v1 = np.linalg.norm(coords[1] - coords[5])
    d_v2 = np.linalg.norm(coords[2] - coords[4])
    d_h = np.linalg.norm(coords[0] - coords[3])
    return (d_v1 + d_v2) / (2.0 * d_h)

def calcular_mar(pontos, face_landmarks):
    p1, p2, p3, p4 = [face_landmarks.landmark[i] for i in pontos]
    dist_v = np.linalg.norm(np.array([p1.x, p1.y]) - np.array([p2.x, p2.y]))
    dist_h = np.linalg.norm(np.array([p3.x, p3.y]) - np.array([p4.x, p4.y]))
    return dist_v / dist_h

cap = cv2.VideoCapture(0)

while cap.isOpened():
    ret, frame = cap.read()
    if not ret: break

    frame = cv2.flip(frame, 1)
    h, w, _ = frame.shape
    rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
    results = face_mesh.process(rgb_frame)

    if results.multi_face_landmarks:
        for face_landmarks in results.multi_face_landmarks:
            # Malha Facial discreta
            mp_drawing.draw_landmarks(frame, face_landmarks, mp_face_mesh.FACEMESH_CONTOURS,
                None, mp_drawing.DrawingSpec(color=(255, 255, 0), thickness=1))

            ear = (calcular_ear(OLHO_ESQ, face_landmarks) + calcular_ear(OLHO_DIR, face_landmarks)) / 2.0
            mar = calcular_mar(BOCA, face_landmarks)

            # --- LÓGICA DE ESTADOS ---
            if ear < EAR_LIMIAR_PERIGO or mar > MAR_LIMIAR_BOCEJO:
                CONTADOR_FRAMES = min(CONTADOR_FRAMES + 2, LIMITE_FRAMES) # Sobe rápido
                status = "PERIGO: SONO DETECTADO!"
                cor_texto = (0, 0, 255) # Vermelho
            elif ear < EAR_LIMIAR_SONOLENTO:
                CONTADOR_FRAMES = min(CONTADOR_FRAMES + 0.8, LIMITE_FRAMES) # Sobe lento
                status = "ESTADO: SONOLENTO"
                cor_texto = (0, 255, 255) # Amarelo
            else:
                CONTADOR_FRAMES = max(CONTADOR_FRAMES - 1, 0) # Recupera
                status = "ESTADO: OK"
                cor_texto = (0, 255, 0) # Verde

            # --- BARRA COLORIDA DINÂMICA ---
            largura_max = 200
            perigo_pct = CONTADOR_FRAMES / LIMITE_FRAMES
            
            # Define cor da barra baseado na porcentagem
            if perigo_pct < 0.4:
                cor_barra = (0, 255, 0)   # Verde
            elif perigo_pct < 0.7:
                cor_barra = (0, 255, 255) # Amarelo
            else:
                cor_barra = (0, 0, 255)   # Vermelho

            cv2.rectangle(frame, (w-220, 40), (w-20, 65), (255, 255, 255), 1)
            cv2.rectangle(frame, (w-220, 40), (w-220 + int(perigo_pct * largura_max), 65), cor_barra, -1)
            cv2.putText(frame, "NIVEL DE FADIGA", (w-220, 35), cv2.FONT_HERSHEY_SIMPLEX, 0.4, (255,255,255), 1)
            cv2.putText(frame, status, (20, 50), cv2.FONT_HERSHEY_SIMPLEX, 0.8, cor_texto, 2)

            if CONTADOR_FRAMES >= LIMITE_FRAMES:
                winsound.Beep(1200, 150)

    cv2.imshow('Monitor de Fadiga Inteligente', frame)
    if cv2.waitKey(1) & 0xFF == ord('q'): break

cap.release()
cv2.destroyAllWindows()