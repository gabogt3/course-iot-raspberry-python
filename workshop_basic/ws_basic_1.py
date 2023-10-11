#Librerias​
from gpiozero import Button, LED
from time import sleep
import random
#definir entredas y salidas indice BCM
led = LED(18) #GPIO18, PIN en J8 = 12
boton = Button(24) #GPIO24, PIN en J8 = 18
#encendido inicial para probar el led
led.on()
print("encendido inicial")
sleep(3)
led.off()
#encender el leb cuando se presione el boton
while True:
    if boton.is_pressed:
        print("boton presionado")
        led.on() #encender el led
        time = random.uniform(2, 5)
        sleep(time) #encendido por tiempo aleatorio entre 2 y 5 segundos
        led.off() #apagar el led
