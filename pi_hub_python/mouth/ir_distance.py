from gpiozero import MCP3008
from time import sleep
import spidev

# IR Distance Sensor (Sharp 2Y0A02)
# Script used to read in voltages as is

# Array list to add the different 8 voltage readings to, [0] being the sensor
voltage = [0, 0, 0, 0, 0, 0, 0, 0]
# Variable to multiply the voltage readings by
vref = 3.3

while True:    
    for x in range(8):
        # Reading in channel 0, channel sensor is on
        adc = MCP3008(channel=0)
        volts = 0.0
        # Converting the reading to a voltage
        for y in range (20):
            volts = volts + (vref * adc.value)
        volts = volts /20.0
        # Formatting a String
        voltsStr = '{:.3f}'.format(volts)
        
        print("channel " + str(0) + ":", voltsStr, "Volts")
        sleep(1)
        
########################
# Example output (random numbers)
# Nothing above sensor/ out of range
# channel 0: 0.345
# channel 0: 0.326
# channel 0: 0.209

# Something 10cm above sensor
# channel 0: 2.767

# Something above and continuously moving further than 10cm
# channel 0: 2.167
# channel 0: 1.984
# channel 0: 1.568
# channel 0: 1.230
# channel 0: 0.936

# Something above and continuously moving closer than 10cm
# channel 0: 1.542
# channel 0: 1.514
# channel 0: 1.468
# channel 0: 1.230
# channel 0: 1.136
