#!/usr/bin/python

# OpenMV Camera Code for BinBot
# Author: Loti Ibrahimi
# Waterford Institute of Technology
# IOT Applications in the Robotics Lab

# Original code pre-Thread integration
"""
import os, sys
import serial

ser = serial.Serial('/dev/serial/by-id/usb-OpenMV_Virtual_Comm_Port_in_FS_Mode_000000000011-if00', 19200, timeout = 5)

# Listen for the input, exit if nothing received in timeout period. 
while True:
   eyes = ser.readline()
   if len(eyes) == 0:
      print("Sleeping.. No object detected. \n")
   print eyes
"""

# Post-Thread integration

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# NOTE: FOR USE WITHIN THE RPI HUB
# One thread is created:
#   1. Thread One: Object Detection
#           > Access coordinates of most recently found object by reading the global : "eyes_test.most_recent_object_coordinates"
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import os, sys
import serial
import time
import threading

print("EYES | Loading Eyes-Test.py Script")

""" Public Global Variables set by the Use Case #1 thread and available for reference publicly """
most_recent_object_coordinates = [ False, False ]

""" Private Global Variables """
OPENMV_SERIAL_PORT = "/dev/serial/by-id/usb-OpenMV_OpenMV_Virtual_Comm_Port_in_FS_Mode_000000000011-if00"

""" Initialisation of the OpenMV Camera """
# Ensure the serial connection is valid before proceeding
ser = False
while not ser:
   try:
      ser = serial.Serial(OPENMV_SERIAL_PORT, 19200, timeout = 5)
   except Exception as ex:
      print("Eyes | Setting Up          | Looking for OpenMV Camera")
      time.sleep(1)
if ser:
   print("Eyes | Setting Up          | Found OpenMV Camera")

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# TEMP USE CASE #1: OBJECT DETECTION
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_recently_found_object_coordinates():
   return most_recent_object_coordinates

def on_object_found(eyesStr):
   """ Private: set the most recently found object's coordinates to the global 'most_recent_object_coordinates' """
   print("Eyes | Object Detection    | Object detected with coordinates")

   # Parsing coordinates from string input
   coordinates_found = []
   for t in eyesStr.split():
    try:
        coordinates_found.append(int(t))
    except ValueError:
        pass
   # Set result to global variable - Note that the X and Y values are scaled to 0->255
   global most_recent_object_coordinates
   most_recent_object_coordinates = [
      int((coordinates_found[0] / 320) * 255),
      69    
      # int((coordinates_found[1] / 240) * 255)
   ]

def _run_object_detection():
   """ Private: create a thread to continuously set recently found object coordinates from the OpenMV Camera """
   print("Eyes | Object Detection    | Object Detection Loop Start")

   while True:
      global _object_detection_stop_thread_flag
      try:
         eyes = ser.readline()
         if len(eyes) == 0:
            print("Eyes | Object Detection    | Sleeping.. No object detected.")
         else:
            on_object_found(eyes)
      except KeyboardInterrupt:
            break
      if _object_detection_stop_thread_flag:
            print("Object Detection Thread told to stop.")
            break

""" Set the target for the object_detection Thread """
_object_detection_thread = threading.Thread(
   target=_run_object_detection, daemon=True)

def start_object_detection_thread():
   global _object_detection_stop_thread_flag
   _object_detection_stop_thread_flag = False
   print("Eyes | Object Detection    | Starting Object Detection Thread")
   # Create a new thread without any parameters (args)
   _object_detection_thread.start()

def stop_object_detection_thread():
   print("Eyes | Object Detection    | Stopping Object Detection Threaad")
   global _object_detection_stop_thread_flag
   _object_detection_stop_thread_flag = True
   global _object_detection_thread
   _object_detection_thread.join()
