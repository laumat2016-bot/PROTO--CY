# config.py
import os

# Obtiene la ruta de la carpeta donde se encuentra este mismo archivo
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
MODEL_PATH = os.path.join(BASE_DIR, "hand_landmarker.task")

# Configuración de Cámara
CAM_INDEX = 0
CAM_WIDTH = 640
CAM_HEIGHT = 480

# Parámetros de detección
MAX_HANDS = 1
MIN_HAND_DETECTION_CONFIDENCE = 0.5
MIN_HAND_PRESENCE_CONFIDENCE = 0.5
MIN_TRACKING_CONFIDENCE = 0.5