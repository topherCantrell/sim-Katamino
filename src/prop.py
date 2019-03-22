import time
import serial

bus = serial.Serial('COM15', 115200)

# Tell the first node what it's chip number is. The
# chips then increment/ripple their numbers down
# the line
bus.write(b'{"to":"@1"}')

for _ in range(5):
    # Chip 1, Nodes A and B ... set your lights
    bus.write(b'{"to":"1A","led":true"}')
    bus.write(b'{"to":"1B","led":false"}')
    time.sleep(1)

    # Chip 1, Nodes A and B ... flip them
    bus.write(b'{"to":"1B","led":true"}')
    bus.write(b'{"to":"1A","led":false"}')
    time.sleep(1)
