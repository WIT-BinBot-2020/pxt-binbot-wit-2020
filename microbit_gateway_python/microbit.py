# Add your Python code here. E.g.
from microbit import *

import radio
import micropython

radio.config(group = 187)
radio.on()

micropython.kbd_intr(-1)


PAYLOAD_LENGTH = 16
PAYLOAD_START = 3

while True:
    msg = radio.receive_bytes()
    if msg != None :

        packet = msg[PAYLOAD_START:(PAYLOAD_START+PAYLOAD_LENGTH)]
        checksum = 0

        for i in range(PAYLOAD_LENGTH):
            checksum ^= packet[i]

        if ( checksum == 0 and packet[0] == 0xbb) :
            uart.write(packet)

    msg2 = uart.read(PAYLOAD_LENGTH)
    if msg2 != None :
        radio.send(msg2)
    