#!/usr/bin/python
import os, sys
import serial

ser = serial.Serial('/dev/serial/by-id/usb-OpenMV_Virtual_Comm_Port_in_FS_Mode_000000000011-if00', 19200, timeout = 5)

# Listen for the input, exit if nothing received in timeout period. 
while True:
   eyes = ser.readline()
   if len(eyes) == 0:
      print("Sleeping.. No object detected. \n")
   print eyes
