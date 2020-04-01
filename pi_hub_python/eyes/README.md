### OpenMV Cam setup using the OpenMVE IDE and the Raspberry Pi. 
---- 
Requirements:
1. You will need **OpenMV IDE**.
2. The **eyes.py** script runs on the Raspberry Pi & reads in data from the OpenMV Cam.
3. The **object-detection.py** script (for OpenMV Cam).
----
#### OpenMV IDE (object-detection.py)
* Open the IDE and load in the object-detection.py script - file > open file.
* Once opened, you can go ahead and connect your OpenMV Cam to your laptop via usb. Wait for light flicker to become stable and then click [white-connect-cable-icon] bottom left.
* To see the loaded script in action just hit the [green-play-btn] bottom left & check the visual display (top-right corner).
* Expand serial terminal at the bottom to view (Object X,Y) readings.
----
#### Saving Script to **OpenMV Cam**
- **[Tools > Save open script to your OpenMV Cam]** command saves whatever script you’re currently looking at to your OpenMV Cam.
- Will save your script as **main.py** on your OpenMV Cam.
- **[Tools > Reset CAM]** after script is saved.
----
#### Raspberry Pi (eyes.py)
- You will need to edit only one line in this script which is the following:
``` 
serial.Serial("/dev/serial/by-id/usb-Silicon_Labs_CP2102_USB_to_UART_Bridge_Controller_0001-if00-port0", baudrate=115200, timeout=1.0)
```
- Run this command first to check the serial port id for the OpenMV Cam connected to your Pi:
```
ls /dev/serial/by-id/
```
- Replace the path after **/by-id/<here>**

