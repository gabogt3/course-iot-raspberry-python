#Librerias​
from gpiozero import Button, PWMLED
from time import sleep
import random
#definir entredas y salidas indice BCM
led = PWMLED(18) #GPIO18, PIN en J8 = 12
boton = Button(24) #GPIO24, PIN en J8 = 18
#encendido inicial para probar el led
led.value = 1.0
print("encendido inicial")
sleep(2)
led.value = 0.5
sleep(2)
led.value = 0.0
#contador de boton
contador = 0
#encender el leb cuando se presione el boton
while True:
    if boton.is_pressed:
        print("boton presionado")
        contador+=1 #aumenta el contador en uno
        if contador == 4:
            contador = 0 #regresamos el contador a 0 para apagar el led
        led.value = contador * 0.33 #asignar el valor de brillo al led
        sleep(0.5) #tiempo de espera para evitar doble pulso
