#!/usr/bin/python
import time
import eyes

# Starts the main Eyes threads. (Can be used to start a stopped thread too)
eyes.start_object_detection_thread()

# Constantly print out the most recently detected object's coordinates
while True:
   coordinates = eyes.get_recently_found_object_coordinates()
   print("eyes-test.py | Object Coordinates Found X%s Y%s" % (coordinates[0], coordinates[1]))