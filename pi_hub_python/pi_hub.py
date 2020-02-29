# Main Raspberry Pi Hub file for handling interaction
# between Microbit Gateway, Robotino and other BinBot
# functionalities

# Made by Wei Kit Wong
# # # # # # # # # # # #

import time
import serial

microbitGatewaySerial = serial.Serial(
    port = 'dev/ACM0',
    baudrate = 115200,
    timeout = 3.0
)

while True:
    fromMicrobitGateway = microbitGatewaySerial.readline()
    print(fromMicrobitGateway)