# main.py
import cv2
import time
import config
from vision import HandDetector
from utils import AngleCalculator, SignalSmoother
from calibration import HandCalibrator
from serial_controller import SerialController

def draw_text_with_outline(img, text, pos, font, scale, color_fg, thickness):
    x, y = pos
    cv2.putText(img, text, (x, y), font, scale, (255, 255, 255), thickness + 2, cv2.LINE_AA)
    cv2.putText(img, text, (x, y), font, scale, color_fg, thickness, cv2.LINE_AA)

def main():
    cap = cv2.VideoCapture(config.CAM_INDEX)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, config.CAM_WIDTH)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, config.CAM_HEIGHT)

    detector = HandDetector()
    calc = AngleCalculator()
    smoother = SignalSmoother(alpha=0.3)
    calibrator = HandCalibrator()
    arduino = SerialController(baudrate=115200, enabled=True)

    p_time = 0
    last_send_time = 0

    print("\n🚀 Sistema de Control Robótico Activo. Presiona 'q' o 'ESC' para salir.")

    while cap.isOpened():
        success, frame = cap.read()
        if not success:
            break

        frame = cv2.flip(frame, 1)
        timestamp_ms = int(time.time() * 1000)

        result = detector.detect(frame, timestamp_ms)
        frame = detector.draw_landmarks(frame, result)

        c_time = time.time()
        fps = 1 / (c_time - p_time) if (c_time - p_time) > 0 else 0
        p_time = c_time

        draw_text_with_outline(frame, f'FPS: {int(fps)}', (20, 40),
                               cv2.FONT_HERSHEY_SIMPLEX, 0.8, (0, 0, 0), 2)

        if result.hand_landmarks:
            hand_lms = result.hand_landmarks[0]

            # 1. Ángulos calculados
            raw_angles = calc.get_finger_angles(hand_lms)

            # 2. Suavizado
            angles = smoother.smooth(raw_angles)

            # 3. Mapeo a Servos
            servo_angles = {}
            for finger, angle in angles.items():
                servo_angles[finger] = calibrator.map_angle_to_servo(finger, angle)

            # 4. Transmisión a Arduino (~30 lecturas por segundo)
            if (c_time - last_send_time) > 0.03:
                arduino.send_angles(servo_angles)
                last_send_time = c_time

            # OSD - Dibujar valores en pantalla
            y_offset = 80
            draw_text_with_outline(frame, "MANO (REAL)  -->  SERVO", (20, y_offset),
                                   cv2.FONT_HERSHEY_SIMPLEX, 0.6, (0, 0, 0), 2)

            for finger_name, angle in angles.items():
                s_angle = servo_angles[finger_name]
                y_offset += 25
                text = f"{finger_name.capitalize()}: {angle:.1f} deg  -->  {s_angle} deg"
                draw_text_with_outline(frame, text, (20, y_offset),
                                       cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0, 0, 0), 1)

        cv2.imshow("Hand Tracking Robot - Control Principal", frame)

        if cv2.waitKey(1) & 0xFF in (ord('q'), 27):
            break

    arduino.close()
    cap.release()
    cv2.destroyAllWindows()

if __name__ == "__main__":
    main()