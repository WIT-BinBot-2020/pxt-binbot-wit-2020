from gpiozero import MCP3008
from time import sleep
import spidev

# IR Distance Sensor (Sharp 2Y0A02)
# Script used to read in voltage to get distance/level of object
# Threshold in this script is for test purposes only, I imagine they'd definetly differ with BinBot

voltage = [0, 0, 0, 0, 0, 0, 0, 0]
vref = 3.3


adc = MCP3008(channel=0)
volts = 0.0
for y in range (20):
    volts = volts + (vref * adc.value)
volts = volts /20.0
voltsStr = '{:.3f}'.format(volts)
voltage[0] = volts
    
# Setting a threshold of 0.4, when voltage goes above that - counted as object in line of sensor (level of rubbish)
# If it's less than 0.4 - counted as nothing reflecting off the IR 
    
if (volts > 0.4):
    i = (volts/3.0) * 100
    print('Level of rubbish: %s %%' % i)
    print('Voltage: %s' % voltsStr)
else:
    print('I\'m a little bit hungry...')
    print('Voltage: %s' % voltsStr) 


