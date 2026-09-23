# serial_controller.py
import serial
import serial.tools.list_ports
import time

class SerialController:
    def __init__(self, port=None, baudrate=115200, enabled=True):
        self.enabled = enabled
        self.ser = None
        self.baudrate = baudrate
        self.port = port or self.find_arduino_port()

        if self.enabled and self.port:
            self.connect()

    def find_arduino_port(self):
        ports = serial.tools.list_ports.comports()
        for p in ports:
            if any(keyword in p.description.upper() for keyword in ["ARDUINO", "CH340", "FTDI", "USB-SERIAL", "CP210"]):
                return p.device
        return ports[0].device if ports else None

    def connect(self):
        try:
            self.ser = serial.Serial(self.port, self.baudrate, timeout=1)
            self.ser.dtr = False
            time.sleep(0.1)
            self.ser.dtr = True
            time.sleep(2)
            print(f"🔌 Conectado exitosamente al Arduino en {self.port} ({self.baudrate} baudios).\n")
        except Exception as e:
            print(f"⚠️ No se pudo abrir {self.port}: {e}")
            self.ser = None

    def send_angles(self, angles_dict):
        if not self.ser or not self.ser.is_open:
            return

        pulgar  = int(angles_dict.get('pulgar', 180))
        indice  = int(angles_dict.get('indice', 180))
        medio   = int(angles_dict.get('medio', 180))
        anular  = int(angles_dict.get('anular', 180))
        meñique = int(angles_dict.get('meñique', 180))

        # Formato de Trama: S,pulgar,indice,medio,anular,meñique\n
        packet = f"S,{pulgar},{indice},{medio},{anular},{meñique}\n"

        try:
            self.ser.write(packet.encode('utf-8'))
            print(f"📤 Enviando -> P:{pulgar}° | I:{indice}° | M:{medio}° | A:{anular}° | m:{meñique}°")
        except Exception as e:
            print(f"⚠️ Error en la comunicación USB: {e}")

    def close(self):
        if self.ser and self.ser.is_open:
            self.ser.close()
            print("🔌 Puerto serie cerrado.")