import serial
import time

bus = serial.Serial('COM15',115200)

bus.write(b'{"to":"@1"}')

for _ in range(5):
    bus.write(b'{"to":"1A","led":true"}')
    bus.write(b'{"to":"1B","led":false"}')
    time.sleep(1)
    bus.write(b'{"to":"1B","led":true"}')
    bus.write(b'{"to":"1A","led":false"}')
    
    time.sleep(1)

time.sleep(10)