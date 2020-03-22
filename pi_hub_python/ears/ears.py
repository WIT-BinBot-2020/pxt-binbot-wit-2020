# ReSpeaker Microphone Array v2.0 Code for BinBot
# Author: Jon Gillespie | References at Base
# Waterford Institute of Technology
# IOT Applications in the Robotics Lab


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# NOTE: FOR USE WITHIN THE RPI HUB
# Two seperate threads are created:
#   1. Thread One: Angle of Voice Detection
#           > Access this variable by reading the global : "ears.scaled_voice_detection_angle"
#       A. VAD Threshold Set
#           > Sets the above thread's voice detection threshold, higher for crowded spaces is best.
#   2. Thread Two: Speech Recognition
#       A. TODO
#
# MAKECODE
# - Must scale up the voice detection angle to 0-360 from 0-255
#
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import speech_recognition as sr
import threading
import logging
import time
import usb.util
import usb.core
from tuning import Tuning
print("EARS | Loading Ears.py Script")


""" User's Keywords for Speech Recognition """
# Format: ("word", threshold) ... threshold is between 0 and 1. Closer to 0 is more false positives.
user_keywords_default = [("binbot", 1.0), ("rubbish", 1.0)]

""" Global Variables used by the Mic Array """
vad_threshold = 300

""" Public Global Variables set by the Mic Array thread and available to reference publicly """
# Referenced by Controller (pi_hub.py) >> Ensure used within a polling loop or framework
voice_detection_angle_to_360 = 0
scaled_voice_detection_angle_to_255 = 0

""" Private Global Variables """
vad_range_max = 1000  # Limit Set by MicArray Tuning
_is_stop_thread_flag = False

""" Initialisation of the Mic Array """
# Find the ReSpeaker in the list of devices connected.
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
# Loop until ReSpeaker is found - unlikely but for insurance.
while not dev:
    print("EARS | Setting Up         | Looking for Mic Array")
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
if dev:
    print("EARS | Setting Up         | Found Mic Array")
    Mic_tuning = Tuning(dev)
    # Mic_tuning.set_HPFONOFF(3) I think this has to run on the CLI as param


def _run_voice_detection_angle():
    """ Private: create a thread to poll the Mic Array and set the DOA Global Variable """
    print("EARS | Voice Detection    | Voice Detection Loop Starting")
    # Mic_tuning.set_vad_threshold(vad_threshold)
    while True:
        global _is_stop_thread_flag
        global voice_detection_angle_to_360
        global Mic_tuning
        try:
            is_voice_detected = Mic_tuning.is_voice()
            if is_voice_detected:
                voice_detection_angle_to_360 = Mic_tuning.direction
                print("EARS | Voice Detection    | Direction of Arrival: ",
                      voice_detection_angle_to_360)
                global scaled_voice_detection_angle_to_255
                scaled_voice_detection_angle_to_255 = voice_detection_angle_to_360 / 360 * 255
            time.sleep(0.5)
        except KeyboardInterrupt:
            break
        if _is_stop_thread_flag:
            break


def set_vad_threshold(make_code_requested_vad_threshold):
    # TODO THIS GETS THE VAD
    # print("" + Mic_tuning.get_VAD())
    """ Public: re-set the VAD threshold """
    # Confirm parameter is an int
    if isinstance(make_code_requested_vad_threshold, int):
        # Ensure parameter is within range
        # TODO find out what the range is.
        if 0 <= make_code_requested_vad_threshold <= 255:
            # Set scaled threshold
            global vad_threshold
            vad_threshold = int(make_code_requested_vad_threshold / 255 * 1000)
        else:
            print("EARS | Voice Detection    | ERROR: make_code_requested_vad_threshold - parameter is not within range")
    else:
        print("EARS | Voice Detection    | ERROR: make_code_requested_vad_threshold - parameter is not an Int")



""" Set the target for the DOA Thread """
doa_thread = threading.Thread(
    target=_run_voice_detection_angle, daemon=True)

def start_doa_thread():
    # Public: start the main DOA thread
    # Ensure the stop flag is off before starting a new thread
    global _is_stop_thread_flag
    _is_stop_thread_flag = False
    print("EARS | Voice Detection    | Starting DOA Loop Thread")
    # Create a new thread without any parameters (args)
    # global doa_thread
    doa_thread.start()


def _stop_doa_thread():
    # Private: stop the currently running thread and reset the flag
    print("EARS | Voice Detection    | Stopping DOA Loop Thread")
    global _is_stop_thread_flag
    # Set the stop flag to true, so that once the thread re-joins the main process, it will know to die.
    _is_stop_thread_flag = True

    # global doa_thread
    #
    # if doa_thread.is_alive():
    #     print("IS ALIVE")
    #
    # doa_thread.join()
    #
    # time.sleep(5)
    # if doa_thread.is_alive():
    #     print("IS ALIVE STILL")


def speech_recognition(user_keyword=user_keywords_default):

    r = sr.Recognizer()
    m = sr.Microphone()

    while True:

        try:
            print("EARS | Speech Recognition | Starting Up...")
            with m as source:
                r.adjust_for_ambient_noise(source)
            print("EARS | Speech Recognition | Set minimum energy threshold to {}".format(
                r.energy_threshold))
            while True:
                print("EARS | Speech Recognition | Ready and Listening...")
                with m as source:
                    audio = r.listen(source)
                print(
                    "EARS | Speech Recognition | Voices detected >>> processing for keywords...")
                try:
                    sphinx_value = r.recognize_sphinx(
                        audio, keyword_entries=user_keyword)
                    print(
                        "EARS | Speech Recognition | * * KEYWORD RECOGNISED * * Sphinx Found:  \" {}\"".format(sphinx_value))
                    # Google Speech Recognition
                    # google_value = r.recognize_google(audio, keyword_entries=user_keyword)
                    # print("EARS | Speech Recognition | * * KEYWORD RECOGNISED * * Google Found:  {}".format(sphinx_value))
                except sr.UnknownValueError:
                    print(
                        "EARS | Speech Recognition | *EXCEPTION* Unknown Value Heard...")
                except sr.RequestError as e:
                    print(
                        "EARS | Speech Recognition | *EXCEPTION* Couldn't request results from Google Speech Recognition service; {0}".format(e))

        except Exception:
            pass


keyword_recognition_thread = threading.Thread(
    target=speech_recognition, daemon=True)

start_doa_thread()


# REFERENCES
# Threading: https://realpython.com/intro-to-python-threading/#starting-a-thread
