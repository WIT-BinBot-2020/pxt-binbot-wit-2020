#!/usr/bin/python
import time
import eyes

# Starts the main Eyes threads. (Can be used to start a stopped thread too)
eyes.start_object_detection_thread()

# Constantly print out the most recently detected object's coordinates
while True:
   currently_detecting_object = eyes.get_is_currently_detecting_object()
   print("eyes-test.py | Object Detection Status: %s" % (currently_detecting_object and "True" or "False"))