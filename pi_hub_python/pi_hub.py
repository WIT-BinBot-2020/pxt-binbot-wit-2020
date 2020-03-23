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
    "CMD_REQUESTDOAANGLE",
    "CMD_SENDMICTHRESHHOLD",
    "CMD_GETMICTHRESHOLD",
    "CMD_SENDKEYWORD",
    "CMD_GETKEYWORDS",
    "CMD_BINMOUTH",
]


# Serial connection to Microbit Gateway for R/W messages
microbitGatewaySerial = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = 1
)


# # # # # # # # # # # #
# Start Up
# # # # # # # # # # # #

# - - - EARS - - -
# Starts the main Ears threads. (Can be used to start a stopped thread too)
ears.start_direction_of_arrival_thread()
ears.start_keyword_recognition_thread()
# You can stop the threads with the below at any time.
# ears.stop_direction_of_arrival_thread()
# ears.stop_keyword_recognition_thread()



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
    elif cmd == "CMD_REQUESTDOAANGLE":
        print("Request direction of arrival angle data from the Mic Array..")
        doa_angle = ears.get_scaled_voice_detectoin_angle()
        # microbitGatewaySerial.write(packet_encoding.CreateNumberPacket(_cmd, doa_angle, 0, 0))

    elif cmd == "CMD_SENDMICTHRESHHOLD":
        print("Setting mic voice detection threshold value of the Mic Array..")
        ears.set_vad_threshold(make_code_requested_vad_threshold=) # TODO Add incoming variable to parameter

    elif cmd == "CMD_GETMICTHRESHOLD":
        print("Retrieving mic voice detection threshold value of the Mic Array..")
        voice_detection_threshold = ears.get_vad_threshold()
        # microbitGatewaySerial.write(packet_encoding.CreateNumberPacket(_cmd, voice_detection_threshold, 0, 0))

    elif cmd == "CMD_SENDKEYWORD":
        print("Setting keyword for Mic Array voice recognition..")
        ears.add_user_keyword(keyword=)  # TODO Add incoming variable to parameter

    elif cmd == "CMD_GETKEYWORDS":
        print("Retreive keywords for Mic Array voice recognition..")
        keywords_list = ears.get_user_keywords()
        # microbitGatewaySerial.write(packet_encoding.CreateStringPacket(_cmd, keywords_list, 0,0))
        
    # - - - MOUTH - - -
    elif cmd == "CMD_BINMOUTH":
        print("Sending action to BinBot's ServoMouth..")
        servo.mouth(rcv_msg.num1)

    else:
        print("Command not defined in module, invalid.")

    # time.sleep(1)
