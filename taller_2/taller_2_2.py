#Librerias​
from gpiozero import Button, LED
from time import sleep
import random
from smbus2 import SMBus
from sgp30 import SGP30
import time
import logging
#descargar la carpeta arduino_iot_cloud
#copiado desde https://github.com/arduino/arduino-iot-cloud-py
#la dependencia senml requerió una corrección tomado de https://github.com/kpn-iot/senml-micropython-library
from arduino_iot_cloud.ucloud import ArduinoCloudClient  # noqa
from arduino_iot_cloud.ucloud import ArduinoCloudObject
from arduino_iot_cloud.ucloud import timestamp
try:
    import asyncio
except ImportError:
    import uasyncio as asyncio

import sys
sys.path.append("lib")
sys.path.append("./")

#definir entredas y salidas indice BCM
salida = LED(14, active_high=False) #GPIO18, PIN en J8 = 12
#encender el leb cuando se presione el boton
bus_i2c = SMBus(1) #usar el puerto I2C 1
sgp = SGP30(bus_i2c) #instanciar el sensor
sgp.init_sgp() #inicializar el sensor
#encendido inicial para probar el ventilador
salida.on()
print("encendido inicial de prueba")
sleep(5)
salida.off()

#from arduino_iot_cloud import ArduinoCloudClient
#obtenido en la creación de la cosa en Arduino Cloud
DEVICE_ID =                                         b"bb65d7a2-8328-4cff-9a45-a4e534e4380b"
SECRET_KEY =                                        b"WTE9BJ4YBRXZ7EJE0DOX"

def logging_func():
    logging.basicConfig(
        datefmt="%H:%M:%S",
        format="%(asctime)s.%(msecs)03d %(message)s",
        level=logging.INFO,
    )   

class Task(ArduinoCloudObject):
    def __init__(self, name, **kwargs):
        kwargs.update({("runnable", True)})  # Force task creation.
        self.on_run = kwargs.pop("on_run", None)
        if not callable(self.on_run):
            raise TypeError("Expected a callable object")
        super().__init__(name, **kwargs)

    async def run(self, aiot):
        while True:
            self.on_run(aiot)
            await asyncio.sleep(self.interval)

# This function is executed each time the "test_switch" variable changes 
def on_switch_changed(client, value):
    print("Switch Pressed! Status is: ", value)

#función del usuario que se llamara repetidamente
    #client es el cliente conectado al Arduino Cloud
def user_task(client):
    lectura = sgp.read_measurements()
    #print(client.contador_promedio_vco2)
    if lectura.data[0] > 700:#este valor depende de las necesidades de la aplicación
        client.contador_encendido_ventilador = 20 #esta función se llama cada segundo, así que este valor es más o menos el tiempo en segundo que permanece encendido el ventilar
    if client.contador_encendido_ventilador > 0:
        if client.contador_encendido_ventilador == 20:
            #envia el valor a la nube cada vez que supera el umbral
            client["vco2"] = lectura.data[0] #actualiza el valor en la nube
            print("enceder ventilador")
            client["ventilador"] = True #actualiza el valor en la nube
        if client.contador_encendido_ventilador == 1:
            client["ventilador"] = False #actualiza el valor en la nube
        
        client.contador_encendido_ventilador -= 1
        salida.on()
    else:
        salida.off()
    #caa 20 segundos envia el promedio a la nube
    if client.contador_promedio_vco2 > 0:
        client.contador_promedio_vco2 -= 1
        client.vco2_20[client.contador_promedio_vco2-1] = lectura.data[0]
    else:
        if client.contador_promedio_vco2 == 0:
            client.contador_promedio_vco2 = 21
            promedio = 0.0
            for valor in client.vco2_20:
                promedio += valor
            promedio /= 20
            print(promedio)
            client["vco2"] = promedio

logging_func()
#crea y conecta a la nube de Arduino Cloud
client = ArduinoCloudClient(device_id=DEVICE_ID, username=DEVICE_ID, password=SECRET_KEY)

client.register("vco2") #registra el valor tal como se definió en Arduino Cloud 
client["vco2"] = 0.0 #registrar un valor inicial en la nube
client.contador_encendido_ventilador = 0
client.contador_promedio_vco2 = 0
client.vco2_20 = [0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0,0.0]
client.register("ventilador", value=None, on_write=on_switch_changed)
client["ventilador"] = False
#registrar la función loop que se mantendrá en ejecución
client.register(Task("user_task", on_run=user_task, interval=1.0)) 
client.start()