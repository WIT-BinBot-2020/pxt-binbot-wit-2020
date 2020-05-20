# Ears - 'BinBot's ability to hear and recognise its own name.'

This single script implements two python threads to:
* Determine Direction of Arrival of Voices
* Recognize Keywords

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.
### Prerequisites

SEEED ReSpeaker MicArray v2.0
http://wiki.seeedstudio.com/ReSpeaker_Mic_Array_v2.0/#version


In order to run on an RPi, the following commands should get you up to speed...

```
pip3 install pyusb
```
```
sudo apt-get install flac
```



PocketSphinx requirements:

```
sudo apt-get install -qq python python-dev python-pip build-essential swig git libpulse-dev libasound2-dev
```
```
pip install pocketsphinx
```
SpeechRecognition requirements:
```
sudo apt-get install python3-pyaudio
```
```
pip3 install SpeechRecognition
```

## Common Error Resolution

If you get this error:   

**"usb.core.USBError: [Errno 13] Access denied (insufficient permissions)"**

https://www.raspberrypi.org/forums/viewtopic.php?t=186839

1. Locate or create this file: **… /etc/udev/rules.d/50-usb-perms.rules**

2. Add this line to the above file and save:
```
SUBSYSTEM==“usb”, ATTRS{idVendor}==“2886", ATTRS{idProduct}==“0018”, GROUP=“plugdev”, MODE=“0660”
```
3. Run this command in terminal:
```
sudo udevadm control --reload; sudo udevadm trigger
```


## Special / Unique Sounding Keywords

The PocketSphinx 'pronounciation-dictionary.dict' within the 'speech_recognition' module, contains a huge list of english words. However, if you are hoping to have your own unique word, such as "BinBot" recognised, you'll need to add it to the dictionary. The easiest way to do this is by finding existing words that partially represent your word's sounds - copying them to assemble your own.
For this project: "BinBot" must be added to 'pronounciation-dictionary.dict'
As there are a few ways to pronounce the word, multiple can be added as shown below with (#).
```
binbot B IH N B AH T
binbot(2) B IH N B AA T
binbot(3) B IH N B AH
```
Your dictionary location may be different - but try here first:
**/home/pi/.local/lib/python3.5/site-packages/speech_recognition/pocketsphinx-data/en-US**


## Optional Resources
If you want to manipulate the LED lights of the SEEED Mic Array v2.0: https://github.com/respeaker/pixel_ring/blob/master/pixel_ring/usb_pixel_ring_v2.py


### Threading
https://realpython.com/intro-to-python-threading/#starting-a-thread

### CMUSphinx
"CMU Sphinx speech recognition engines"

https://cmusphinx.github.io/

### SpeechRecognition
"Library for performing speech recognition, with support for several engines and APIs, online and offline."

https://github.com/Uberi/speech_recognition

https://pypi.org/project/SpeechRecognition/

### PyAudio
"PyAudio provides Python bindings for PortAudio, the cross-platform audio I/O library"

http://people.csail.mit.edu/hubert/pyaudio/docs/
