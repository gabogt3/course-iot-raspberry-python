#!/usr/bin/env python

import pigpio

pigpio.exceptions = False # handle errors

pi = pigpio.pi()

for bus in range(2):
    for x in range(0x08, 0x79):
        try:
            h = pi.i2c_open(bus, x)
            if h >= 0:
                s = pi.i2c_read_byte(h)
                if s >= 0:
                    print("dispositivo encontrado con address {} en el bus {}".format(x, bus))
                pi.i2c_close(h)
        except:
            print("Error al probar con address: "+hex(x))
pi.stop()
