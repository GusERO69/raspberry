import time
import board
import busio
import adafruit_ads1x15.ads1115 as ADS
from adafruit_ads1x15.analog_in import AnalogIn
import mysql.connector

# Configuración del I2C y ADS1115
i2c = busio.I2C(board.SCL, board.SDA)
ads = ADS.ADS1115(i2c)
chan = AnalogIn(ads, ADS.P0)

# Configuración de la conexión a la base de datos
conn = mysql.connector.connect(
    host="34.151.233.27",
    user="CEG4",
    password="'sFk)z/lm1l7nD2;",
    database="Grupo4"
)
cursor = conn.cursor()

while True:
    # Leer el valor del sensor
    voltage = chan.voltage
    
    # Calcular corriente (depende del factor de conversión del SCT-013-000)
    current = (voltage / 2) / 0.050  # Ajusta según el circuito utilizado
    
    # Insertar datos en la base de datos
    cursor.execute("INSERT INTO energy_measurements (timestamp, voltage, current) VALUES (NOW(), %s, %s)", (voltage, current))
    conn.commit()
    
    # Esperar antes de la siguiente lectura
    time.sleep(1)

# Cerrar la conexión a la base de datos al finalizar (si es necesario)
conn.close()