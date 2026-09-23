# calibration.py
class HandCalibrator:
    def __init__(self):
        # Rangos de ángulos anatómicos de la mano humana: (Mano abierta/extendida, Mano flexionada/puño)
        self.ranges = {
            'pulgar':  (30, 160),
            'indice':  (20, 170),
            'medio':   (20, 170),
            'anular':  (20, 170),
            'meñique': (20, 170)
        }

    def map_angle_to_servo(self, finger_name, angle):
        min_deg, max_deg = self.ranges.get(finger_name, (20, 170))
        
        # Limitar el ángulo capturado dentro del rango esperado
        angle = max(min_deg, min(max_deg, angle))
        
        # Mapear proporcionalmente de (min_deg -> max_deg) a (180 -> 0)
        # 180° = Dedo extendido / 0° = Dedo doblado
        if max_deg == min_deg:
            return 180
            
        servo_val = int((angle - min_deg) * (180 - 0) / (max_deg - min_deg))
        return max(0, min(180, servo_val))