from gpiozero import MCP3008
from time import sleep
import spidev

# IR Distance Sensor (Sharp 2Y0A02)
# Script used to read in voltages and count spike in voltage
# Threshold in this script is for test purposes only, I imagine they'd would definetly differ with BinBot

voltage = [0, 0, 0, 0, 0, 0, 0, 0]
vref = 3.3
# Counter
i = 1

while True:
    adc = MCP3008(channel=0)
    volts = 0.0
    for y in range (20):
        volts = volts + (vref * adc.value)
    volts = volts /20.0
    voltsStr = '{:.3f}'.format(volts)
    voltage[0] = volts
        
    # Setting a threshold of 0.6, when voltage goes above that - counted as something passing by
    if (volts > 0.6):
        print('Count of rubbish: %s' % i)
        print('Voltage: %s' % voltsStr)
        # 	Increment counter
        i = i+1
    sleep(0.2)
    