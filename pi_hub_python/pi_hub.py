# Main Raspberry Pi Hub file for handling interaction
# between Microbit Gateway, Robotino and other BinBot
# functionalities

# Made by Wei Kit Wong
# # # # # # # # # # # #

import time
import serial

# Mapping of command numbers and their associated intended system functionality
# e.g. if cmd==1, isString=True, isRobotinoMessage=True, so route to Robotino to handle functionality
COMMANDS = [
    { "name": "CMD_TEST", "isString": False, "isRobotinoMessage": True, "sendDataBack": False }, # 0
    { "name": "CMD_SENDSTRING", "isString": True, "isRobotinoMessage": True, "sendDataBack": False }, # 1
    { "name": "CMD_SENDNUMBERS", "isString": False, "isRobotinoMessage": True, "sendDataBack": False }, # 2
    { "name": "CMD_CTRLOMNIDRIVE", "isString": False, "isRobotinoMessage": True, "sendDataBack": False }, # 3
    { "name": "CMD_REQUESTDISTANCESENSOR", "isString": False, "isRobotinoMessage": True, "sendDataBack": True }, # 4
    { "name": "CMD_SENDDISTANCESENSORVALUE", "isString": False, "isRobotinoMessage": True, "sendDataBack": False } # 5
]

# Serial connection to Microbit Gateway for R/W messages
microbitGatewaySerial = serial.Serial(
    port = '/dev/ttyACM0',
    baudrate = 115200,
    timeout = 1
)

# Wrapping the message to be received from the Microbit Gateway
class ReceiveMessage:
    
    def __init__(self, *args, **kwargs):
        self.cmd = args[0]
        
        self.isString = COMMANDS[self.cmd]["isString"]
        self.isRobotinoMessage = COMMANDS[self.cmd]["isRobotinoMessage"]
        self.sendDataBack = COMMANDS[self.cmd]["sendDataBack"]
        
        self.str1 = args[1]
        self.num1 = args[2]
        self.num2 = args[3]
        self.num3 = args[4]
            
    def printData(self):
        if self.isString:
            print("COMMAND NUMBER %s WITH STRING %s" % (self.cmd, self.str1))
        else:
            print("COMMAND NUMBER %s WITH NUMBERS %s, %s, %s" % (self.cmd, self.num1, self.num2, self.num3))

while True:
    
    # Reading in message from the Microbit Gateway
    fromMicrobitGateway = microbitGatewaySerial.readline()
    rcv_msg = ReceiveMessage(fromMicrobitGateway[2], fromMicrobitGateway[3:12], fromMicrobitGateway[3], fromMicrobitGateway[7], fromMicrobitGateway[11])
    rcv_msg.printData()
    
    if rcv_msg.isRobotinoMessage:
        print("")
        # Write data via serial to Robotino
        
    if rcv_msg.sendDataBack:
        print("")
        # Read data via serial from Robotino
        # Write data back via serial to Microbit Gateway
    
    time.sleep(1)