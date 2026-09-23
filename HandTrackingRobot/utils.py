# utils.py
import numpy as np

class AngleCalculator:
    """Calcula los ángulos de flexión 3D para los 5 dedos."""

    def __init__(self):
        # Índices de la mano en MediaPipe: (Base/Muñeca, Nudillo, Articulación, Punta)
        self.finger_indices = {
            'pulgar':  (1, 2, 4),
            'indice':  (0, 5, 8),
            'medio':   (0, 9, 12),
            'anular':  (0, 13, 16),
            'meñique': (0, 17, 20)
        }

    def _calculate_angle_3d(self, p1, p2, p3):
        v1 = np.array([p1.x - p2.x, p1.y - p2.y, p1.z - p2.z])
        v2 = np.array([p3.x - p2.x, p3.y - p2.y, p3.z - p2.z])

        norm_v1 = np.linalg.norm(v1)
        norm_v2 = np.linalg.norm(v2)

        if norm_v1 == 0 or norm_v2 == 0:
            return 180.0

        v1_u = v1 / norm_v1
        v2_u = v2 / norm_v2

        cosine_angle = np.clip(np.dot(v1_u, v2_u), -1.0, 1.0)
        angle_rad = np.arccos(cosine_angle)
        return float(np.degrees(angle_rad))

    def get_finger_angles(self, landmarks):
        angles = {}
        for finger_name, (idx1, idx2, idx3) in self.finger_indices.items():
            p1 = landmarks[idx1]
            p2 = landmarks[idx2]
            p3 = landmarks[idx3]
            raw_angle = self._calculate_angle_3d(p1, p2, p3)
            angles[finger_name] = raw_angle
        return angles


class SignalSmoother:
    """Filtro Exponencial (EMA) para eliminar temblores en los servos."""

    def __init__(self, alpha=0.3):
        self.alpha = alpha
        self.smoothed_values = {}

    def smooth(self, current_values):
        for key, val in current_values.items():
            if key not in self.smoothed_values:
                self.smoothed_values[key] = val
            else:
                self.smoothed_values[key] = (self.alpha * val) + ((1.0 - self.alpha) * self.smoothed_values[key])
        return self.smoothed_values