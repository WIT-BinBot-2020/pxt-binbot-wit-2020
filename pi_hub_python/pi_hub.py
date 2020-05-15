# Raspberry Pi Hub Code for BinBot
# Author: Wei Kit Wong
# Waterford Institute of Technology
# IOT Applications in the Robotics Lab

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Main Raspberry Pi Hub file for handling interaction
# between Microbit Gateway, Robotino and providing other
# functionalities
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import serial
import time

print("RPi Hub | Loading All Dependencies")

import packet_encoding
from eyes import eyes
from ears import ears
from mouth import servo
from sounds import sounds
from pi_monitoring_scripts.pub_data import publish

""" Global Variables used by the RPi Hub """
# Mapping of command numbers and their associated system functionality
COMMANDS = [
    "CMD_TEST", #= 0,
    "CMD_SENDSTRING", #= 1,
    "CMD_SENDNUMBERS", #= 2,
    "CMD_CTRLOMNIDRIVE", #= 3,
    "CMD_REQUESTDISTANCESENSOR", #= 4,
    "CMD_SENDDISTANCESENSORVALUE", #= 5,
    "CMD_REQUESTSOUND", #= 6,
    "CMD_SENDNAME", #= 7,
    "CMD_SENDMICTHRESHOLD", #= 8,
    "CMD_BINMOUTH", #= 9,
    "CMD_REQUESTMICANGLE", #= 10,
    "CMD_REQUESTOBJCOORDS", #= 11,
    "CMD_REQUESTNAMECALLED", #= 12
    "",
    "CMD_SENDMESSAGE", #= 14
]

# Outdated command numbers mapping, to be discussed
"""
COMMANDS = [
    "CMD_TEST",
    "CMD_SENDSTRING",
    "CMD_SENDNUMBERS",
    "CMD_CTRLOMNIDRIVE",
    "CMD_REQUESTDISTANCESENSOR",
    "CMD_SENDDISTANCESENSORVALUE",
    "CMD_REQUESTSOUND",
    "CMD_REQUESTDOAANGLE",
    "CMD_SENDMICTHRESHOLD",
    "CMD_GETMICTHRESHOLD",
    "CMD_SENDKEYWORD",
    "CMD_GETKEYWORDS",
    "CMD_BINMOUTH",
]
"""

""" Establishing serial connection to Microbit Gateway for R/W messages  """
microbitGatewaySerial = False
while not microbitGatewaySerial:
    try:
        microbitGatewaySerial = serial.Serial(
            port='/dev/ttyACM0',
            baudrate=115200,
            timeout=0
        )
    except Exception as ex:
        print("RPi Hub | Looking for Microbit Gateway")
        time.sleep(1)

if microbitGatewaySerial:
    print("RPi Hub | Found Microbit Gateway")

""" RPi Hub Operations """    
# # # # # # # # # # # # #
# Start Up
# # # # # # # # # # # # #

# - - - EYES - - -
# Starts the main Eyes threads. (Can be used to start a stopped thread too)
eyes.start_object_detection_thread()
# You can stop the threads with the below at any time.
# eyes.stop_object_detection_thread()

# - - - EARS - - -
# Starts the main Ears threads. (Can be used to start a stopped thread too)
ears.start_direction_of_arrival_thread()
ears.start_keyword_recognition_thread()
# You can stop the threads with the below at any time.
# ears.stop_direction_of_arrival_thread()
# ears.stop_keyword_recognition_thread()
is_keyword_event_sent_to_make_code = False


# # # # # # # # # # # # # #
# Main Message Controller
# # # # # # # # # # # # # #
while True:

    # Continuously read in message from the Microbit Gateway
    fromMicrobitGateway = microbitGatewaySerial.readline()

    if len(fromMicrobitGateway) != packet_encoding.PAYLOAD_LENGTH:
        # print("RPi Hub | Invalid incoming message")
        continue

    _cmd = fromMicrobitGateway[2]
    cmd = COMMANDS[_cmd]
    rcv_msg = packet_encoding.ReceivedPacket(
        fromMicrobitGateway[3:12], fromMicrobitGateway[3], fromMicrobitGateway[7], fromMicrobitGateway[11])

    # Switch case -> perform y functionality if x
    # - - - MOVEMENT - - -
    if cmd == "CMD_TEST":
        print("RPi Hub | Writing message to Robotino")

    elif cmd == "CMD_SENDSTRING":
        print("RPi Hub | Sending a string to Robotino")

    elif cmd == "CMD_SENDNUMBERS":
        print("RPi Hub | Sending numbers to Robotino")

    elif cmd == "CMD_CTRLOMNIDRIVE":
        print("RPi Hub | Requesting to control Robotino movement")

    # - - - EYES - - -
    elif cmd == "CMD_REQUESTDISTANCESENSOR":
        print("RPi Hub | Request distance sensor data from the Robotino")

    elif cmd == "CMD_SENDDISTANCESENSORVALUE":
        print("RPi Hub | Sending a distance sensor value to the Robotino")

    elif cmd == "CMD_REQUESTOBJCOORDS":
        print("RPi Hub | Request most recently detected object's coordinates")
        object_coordinates = eyes.get_recently_found_object_coordinates()
        microbitGatewaySerial.write(
            packet_encoding.CreateNumberPacket(_cmd, object_coordinates[0], object_coordinates[1], 0))

    # - - - SOUND - - -
    elif cmd == "CMD_REQUESTSOUND":
        print("RPi Hub | Playing sound..")
        sounds.play_sound(rcv_msg.num1)

    # - - - EARS - - -
    elif cmd == "CMD_REQUESTMICANGLE":
        print("RPi Hub | Request direction of arrival angle data from the Mic Array")
        doa_angle = ears.get_scaled_voice_detection_angle()
        microbitGatewaySerial.write(packet_encoding.CreateNumberPacket(_cmd, doa_angle, 0, 0))

    elif cmd == "CMD_SENDMICTHRESHOLD":
        print("RPi Hub | Setting mic voice detection threshold value of the Mic Array")
        ears.set_vad_threshold(make_code_requested_vad_threshold=rcv_msg.num1)

    elif cmd == "CMD_GETMICTHRESHOLD":
        print("RPi Hub | Retrieving mic voice detection threshold value of the Mic Array")
        voice_detection_threshold = ears.get_scaled_vad_threshold()
        microbitGatewaySerial.write(packet_encoding.CreateNumberPacket(_cmd, voice_detection_threshold, 0, 0))

    elif cmd == "CMD_SENDNAME":
        print("RPi Hub | Setting keyword for Mic Array voice recognition")
        ears.add_user_keyword(keyword=rcv_msg.str1)

    # NOTE: This may not be feasable given the list it will return is longer than a few characters...LIMIT>?
    elif cmd == "CMD_GETKEYWORDS":
        print("RPi Hub | Retreive keywords for Mic Array voice recognition")
        keywords_list = ears.get_user_keywords()
        # microbitGatewaySerial.write(packet_encoding.CreateStringPacket(_cmd, keywords_list, 0,0))

    elif cmd == "CMD_REQUESTNAMECALLED":
        print("RPi Hub | Checking whether keyword was called or not")
        recognised_keyword = ears.has_recognised_keyword and 1 or 0
        microbitGatewaySerial.write(packet_encoding.CreateNumberPacket(_cmd, recognised_keyword, 0, 0))
        is_keyword_event_sent_to_make_code = True
        ears.has_recognised_keyword = False
        

    # - - - MOUTH - - -
    elif cmd == "CMD_BINMOUTH":
        print("RPi Hub | Sending action to ServoMouth")
        # servo.mouth(rcv_msg.num1)

    # - - - CLOUD - - -
    elif cmd == "CMD_SENDMESSAGE":
        print("RPi Hub | Sending message to Slack Bot")
        messageFromMakeCode = rcv_msg.str1

        # Generate json data
        data = {
            "message": messageFromMakeCode,
        }
        # Define which measurement the data belongs to. Battery stats for example
        measurement = "messages" 
        publish(measurement, data)

    else:
        print("RPi Hub | Valid incoming message but invalid command")
