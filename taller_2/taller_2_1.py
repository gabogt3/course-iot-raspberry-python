#Librerias​
from gpiozero import Button, LED
from time import sleep
import random
from smbus2 import SMBus
from sgp30 import SGP30
#definir entredas y salidas indice BCM
salida = LED(14, active_high=False) #GPIO14, PIN en J8 = 8
#encender el leb cuando se presione el boton
bus_i2c = SMBus(1) #usar el puerto I2C 1
sgp = SGP30(bus_i2c) #instanciar el sensor
sgp.init_sgp() #inicializar el sensor
contador = 0
#encendido inicial para probar el ventilador
salida.on()
print("encendido inicial de prueba")
sleep(5)
salida.off()
sleep(10) #esperar por inicialización completa del sensor
for i in range(3000):
    lectura = sgp.read_measurements()
    print(lectura.data[0])
    if lectura.data[0] > 500:
        contador = 20
    if contador > 0:
        contador -= 1
        salida.on()
        print("enceder ventilador")
    else:
        salida.off()      
    sleep(0.5)
salida.off()
bus_i2c.close()