#!/usr/bin/python
import time
import eyes

eyes.start_object_detection_thread()

# Listen for the input, exit if nothing received in timeout period. 
while True:
   coordinates = eyes.get_recently_found_object_coordinates()
   print("eyes-test.py | Object Coordinates Detected (Scaled Down to 255) X%s Y%s" % (coordinates[0], coordinates[1]))