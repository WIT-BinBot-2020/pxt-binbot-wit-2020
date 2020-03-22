# Main Raspberry Pi Hub file for handling interaction
# between Microbit Gateway, Robotino and other BinBot
# functionalities

# Made by Wei Kit Wong
# # # # # # # # # # # #

import serial
import packet_encoding
from ears import ears
from mouth import servo
from sounds import sounds
import time

# # # # # # # # # # # #
# Variables
# # # # # # # # # # # #

# Mapping of command numbers and their associated system functionality
COMMANDS = [
    "CMD_TEST",
    "CMD_SENDSTRING",
    "CMD_SENDNUMBERS",
    "CMD_CTRLOMNIDRIVE",
    "CMD_REQUESTDISTANCESENSOR",
    "CMD_SENDDISTANCESENSORVALUE",
    "CMD_REQUESTSOUND",
    "CMD_SENDNAME",
    "CMD_SENDMICTHRESHHOLD",
    "CMD_BINMOUTH",
    "CMD_REQUESTMICANGLE"
]

# Serial connection to Microbit Gateway for R/W messages
microbitGatewaySerial = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = 1
)

# # # # # # # # # # # #
# Main block of code
# # # # # # # # # # # #
while True:
    
    # Continuously read in message from the Microbit Gateway
    fromMicrobitGateway = microbitGatewaySerial.readline()

    if len(fromMicrobitGateway) != packet_encoding.PAYLOAD_LENGTH:
        print("Invalid payload length, message __not__ from the Microbit Gateway detected.")
        continue

    _cmd = fromMicrobitGateway[2]
    cmd = COMMANDS[_cmd]
    rcv_msg = packet_encoding.ReceivedPacket(fromMicrobitGateway[3:12], fromMicrobitGateway[3], fromMicrobitGateway[7], fromMicrobitGateway[11])

    # Switch case -> perform y functionality if x
    # - - - MOVEMENT - - -
    if cmd == "CMD_TEST":
        print("Writing data to Robotino..")

    elif cmd == "CMD_SENDSTRING":
        print("Sending a string to Robotino..")

    elif cmd == "CMD_SENDNUMBERS":
        print("Sending numbers to Robotino..")

    elif cmd == "CMD_CTRLOMNIDRIVE":
        print("Requesting to control Robotino movement..")

    # - - - EYES ? - - -
    elif cmd == "CMD_REQUESTDISTANCESENSOR":
        print("Request distance sensor data from the Robotino..")

    elif cmd == "CMD_SENDDISTANCESENSORVALUE":
        print("Sending a distance sensor value to the Robotino..")

    # - - - SOUND - - -
    elif cmd == "CMD_REQUESTSOUND":
        print("Playing sound..")
        sounds.play_sound(rcv_msg.num1)
        
    # - - - EARS - - -
    elif cmd == "CMD_SENDKEYWORD":
        print("Setting keyword for Mic Array voice recognition..")
        
    elif cmd == "CMD_SENDMICTHRESHHOLD":
        print("Setting mic voice detection threshold value to the Mic Array..")

    elif cmd == "CMD_"
        
    # - - - MOUTH - - -
    elif cmd == "CMD_BINMOUTH":
        print("Sending action to BinBot's ServoMouth..")
        servo.mouth(rcv_msg.num1)
        
    elif cmd == "CMD_REQUESTMICANGLE":
        print("Request mic angle data from the Mic Array..")
        # microbitGatewaySerial.write(packet_encoding.CreateNumberPacket(_cmd, ears.scaled_voice_detection_angle, 0, 0))

    else:
        print("Command not defined in module, invalid.")

    # time.sleep(1)
