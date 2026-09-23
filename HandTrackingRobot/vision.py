# vision.py
import cv2
import numpy as np
import mediapipe as mp
from mediapipe.tasks import python
from mediapipe.tasks.python import vision

import config

class HandDetector:
    def __init__(self):
        base_options = python.BaseOptions(model_asset_path=config.MODEL_PATH)
        options = vision.HandLandmarkerOptions(
            base_options=base_options,
            running_mode=vision.RunningMode.VIDEO,
            num_hands=config.MAX_HANDS,
            min_hand_detection_confidence=config.MIN_HAND_DETECTION_CONFIDENCE,
            min_hand_presence_confidence=config.MIN_HAND_PRESENCE_CONFIDENCE,
            min_tracking_confidence=config.MIN_TRACKING_CONFIDENCE
        )
        self.detector = vision.HandLandmarker.create_from_options(options)
        
        self.HAND_CONNECTIONS = [
            (0, 1), (1, 2), (2, 3), (3, 4),        # Pulgar
            (0, 5), (5, 6), (6, 7), (7, 8),        # Índice
            (5, 9), (9, 10), (10, 11), (11, 12),   # Medio
            (9, 13), (13, 14), (14, 15), (15, 16), # Anular
            (13, 17), (0, 17), (17, 18), (18, 19), (19, 20) # Meñique
        ]

    def detect(self, frame, timestamp_ms):
        rgb_frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        # Empaquetamos la imagen especificando dimensiones exactas
        mp_image = mp.Image(image_format=mp.ImageFormat.SRGB, data=np.ascontiguousarray(rgb_frame))
        return self.detector.detect_for_video(mp_image, timestamp_ms)

    def draw_landmarks(self, frame, detection_result):
        if not detection_result.hand_landmarks:
            return frame

        h, w, _ = frame.shape

        for hand_landmarks in detection_result.hand_landmarks:
            for start_idx, end_idx in self.HAND_CONNECTIONS:
                pt1 = hand_landmarks[start_idx]
                pt2 = hand_landmarks[end_idx]
                x1, y1 = int(pt1.x * w), int(pt1.y * h)
                x2, y2 = int(pt2.x * w), int(pt2.y * h)
                cv2.line(frame, (x1, y1), (x2, y2), (0, 255, 0), 2)

            for lm in hand_landmarks:
                cx, cy = int(lm.x * w), int(lm.y * h)
                cv2.circle(frame, (cx, cy), 4, (0, 0, 255), -1)

        return frame