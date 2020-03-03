# Raspberry Pi file for handling encoding of
# messages when sending data back from the RPi
# to the Microbit Gateway

# Made by Wei Kit Wong
# # # # # # # # # # # #

# # # # # # # # # # # #
# Variables
# # # # # # # # # # # #

# Maximum amount of data transferable between Microbit Gateway and RPi
PAYLOAD_LENGTH = 16
MESSAGE_LENGTH = 12

# # # # # # # # # # # #
# Classes
# # # # # # # # # # # #

# Wrapping the message to be received from the Microbit Gateway
class ReceivedPacket:
    def __init__(self, *args, **kwargs):
        self.str1 = args[0]
        self.num1 = args[1]
        self.num2 = args[2]
        self.num3 = args[3]

# # # # # # # # # # # #
# Packet Creation Helpers
# # # # # # # # # # # #

# Auto encoding string messages
def CreateStringPacket(cmd, str1):

    # String should adhere to message size of 12
    msg = bytearray(MESSAGE_LENGTH)

    # Fit string buffer to message
    str_buf = bytearray(str1, 'utf-16')
    
    if (len(str_buf) > MESSAGE_LENGTH):
        str_buf = str_buf[0 : MESSAGE_LENGTH]

    msg[0 : MESSAGE_LENGTH] = str_buf

    # Creating the final packet to be sent
    packet = bytearray(PAYLOAD_LENGTH)
    packet[0] = 0xbb
    packet[2] = cmd
    packet[3 : MESSAGE_LENGTH + 3] = msg

    # Generating checksum to indicate this is from the valid communication stack
    checksum = 0
    for i in range(PAYLOAD_LENGTH):
            checksum ^= packet[i]
    
    packet[5] = checksum

    return packet

# Auto encoding number messages
def CreateNumberPacket(cmd, num1, num2, num3):
    
    # Number data should adhere to message size of 12
    msg = bytearray(MESSAGE_LENGTH)

    # Put number bytes at specified indexes
    msg[0] = num1
    msg[4] = num2
    msg[8] = num3

    # Creating the final packet to be sent
    packet = bytearray(PAYLOAD_LENGTH)
    packet[0] = 0xbb
    packet[2] = cmd
    packet[3 : MESSAGE_LENGTH + 3] = msg

    # Generating checksum to indicate this is from the valid communication stack
    checksum = 0
    for i in range(PAYLOAD_LENGTH):
            checksum ^= packet[i]
    
    packet[5] = checksum

    return packet