import serial
import time

bus = serial.Serial('COM15',115200)

bus.write(b'{"to":"@1"}')

bus.write(b'{"to":"1A"}')

time.sleep(10)