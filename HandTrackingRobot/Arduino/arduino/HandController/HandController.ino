#include <Servo.h>

// Objetos Servo para cada dedo
Servo servoPulgar;  // Pin 3
Servo servoIndice;  // Pin 5
Servo servoMayor;   // Pin 6
Servo servoAnular;  // Pin 9
Servo servoMenique; // Pin 10

// Asignación de Pines PWM
const int PIN_PULGAR  = 3;
const int PIN_INDICE  = 5;
const int PIN_MAYOR   = 6;
const int PIN_ANULAR  = 9;
const int PIN_MENIQUE = 10;

// Limites de seguridad angular (Software Clamping)
const int ANG_MIN = 0;
const int ANG_MAX = 180;

void setup() {
  // Configuración del puerto serie a 115200 baudios (para sincronización con Python)
  Serial.begin(115200);

  // Vincular servos a los pines PWM
  servoPulgar.attach(PIN_PULGAR);
  servoIndice.attach(PIN_INDICE);
  servoMayor.attach(PIN_MAYOR);
  servoAnular.attach(PIN_ANULAR);
  servoMenique.attach(PIN_MENIQUE);

  // =====================================================
  // RUTINA DE AUTO-TEST Y PRUEBA DE POTENCIA (AL ENCHUFAR)
  // =====================================================
  
  // 1. Posición inicial: Mano totalmente abierta
  moverMano(0, 0, 0, 0, 0);
  delay(1200);

  // 2. Cierre completo de la mano (Prueba de consumo conjunto)
  moverMano(180, 180, 180, 180, 180);
  delay(1500);

  // 3. Regreso a posición de reposo (Mano abierta)
  moverMano(0, 0, 0, 0, 0);
  delay(1000);
}

void loop() {
  // =====================================================
  // MODO TELEOPERACIÓN EN TIEMPO REAL (RECEPCIÓN DESDE PYTHON)
  // =====================================================
  
  // Escuchar si hay tramas de datos provenientes de la cámara / Python
  if (Serial.available() > 0) {
    String trama = Serial.readStringUntil('\n'); // Leer línea completa
    trama.trim();

    // Comprobar formato de cabecera válido ("S,θ_pul,θ_ind,θ_may,θ_anu,θ_meñ")
    if (trama.startsWith("S,")) {
      trama = trama.substring(2); // Remover la cabecera 'S,'

      // Parsear los 5 ángulos individuales
      int angPulgar  = extraerSiguienteAngulo(trama);
      int angIndice  = extraerSiguienteAngulo(trama);
      int angMayor   = extraerSiguienteAngulo(trama);
      int angAnular  = extraerSiguienteAngulo(trama);
      int angMenique = extraerSiguienteAngulo(trama);

      // Aplicar movimiento físico a los servomotores
      moverMano(angPulgar, angIndice, angMayor, angAnular, angMenique);
    }
  }
}

// Función auxiliar para mover todos los servos aplicando restricciones de seguridad
void moverMano(int p, int i, int m, int a, int me) {
  servoPulgar.write(constrain(p, ANG_MIN, ANG_MAX));
  servoIndice.write(constrain(i, ANG_MIN, ANG_MAX));
  servoMayor.write(constrain(m, ANG_MIN, ANG_MAX));
  servoAnular.write(constrain(a, ANG_MIN, ANG_MAX));
  servoMenique.write(constrain(me, ANG_MIN, ANG_MAX));
}

// Función auxiliar para extraer números enteros de la cadena CSV
int extraerSiguienteAngulo(String &datos) {
  int indiceComa = datos.indexOf(',');
  if (indiceComa == -1) {
    int valor = datos.toInt();
    datos = "";
    return valor;
  }
  int valor = datos.substring(0, indiceComa).toInt();
  datos = datos.substring(indiceComa + 1);
  return valor;
}
