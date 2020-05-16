# ReSpeaker Microphone Array v2.0 Code for BinBot
# Author: Jon Gillespie
# Waterford Institute of Technology
# IOT Applications in the Robotics Lab

# EARS : Manages all listening capabilities of the BinBot, which, can determine the angle of arrival of 
#        a human's voice and recognise keywords.
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# Two seperate threads are created:
#   1. Thread One: Angle of Voice Detection
#      > Access this variable by reading the global : "ears.scaled_voice_detection_angle"
#      > Publishes the angle to the mqtt cloud feed every 6th cycle
#      - VAD Threshold Set : set_vad_threshold(make_code_requested_vad_threshold)
#        > Sets the above thread's voice detection threshold, higher for crowded spaces is best.
#        > Expects an Int (0-255) and will scale it up to 0-1000 for the Mic array. 
#      - VAG Get Threshold : ears.get_scaled_vad_threshold()
#        > Returns the scaled version of the threshold (0-255)
#   2. Thread Two: Keyword Recognition
#      > Set a new Keyword : ears.add_user_keyword(keyword)
#      > Get all the Keywords : ears.get_user_keywords()
#      > Determines if any Keywords have been said : "has_recognised_keyword"
#      > Sends the Keyword to the Cloud via MQTT upon recognition
#
# MAKECODE Note
# > Must scale up the voice detection angle to 0-360 from 0-255 to present the user with accurate angles
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

import speech_recognition as sr
import threading
import logging
import time
import usb.util
import usb.core
from .tuning import Tuning
from pi_monitoring_scripts.pub_data import publish
print("EARS | Loading Ears.py Script")

""" User's Keywords for Keyword Recognition """
# Format: ("word", threshold) ... threshold is between 0 and 1. Closer to 0 is more false positives.
user_keywords = [("binbot", 1.0), ("rubbish", 1.0)]
has_recognised_keyword = False

""" Global Variables used by the Mic Array """
vad_threshold = 300

""" Public Global Variables set by the Mic Array thread and available to reference publicly """
# Referenced by Controller (pi_hub.py) >> Ensure used within a polling loop or framework
voice_detection_angle_to_360 = 0
scaled_voice_detection_angle_to_255 = 0
scaled_vad_threshold_to_255 = vad_threshold / 1000 * 255

""" Private Global Variables """
vad_range_max = 1000  # Limit Set by MicArray Tuning
mqtt_topic_mic_angle = "micAngleArrival"
mqtt_topic_keyword = "micKeyword"  

""" Initialisation of the Mic Array """
# Find the ReSpeaker in the list of devices connected.
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
# Loop until ReSpeaker is found - unlikely but for insurance.
while not dev:
    print("EARS | Setting Up          | Looking for Mic Array")
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
if dev:
    print("EARS | Setting Up          | Found Mic Array")
    Mic_tuning = Tuning(dev)
    # Mic_tuning.set_HPFONOFF(3) # For the CLI as param


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# VOICE DETECTION ANGLE
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_scaled_voice_detection_angle():
    """ Public: Returns the angle of voice detection scaled down to fit in a byte length.
        Must be scaled back 'up' to 360 max to represent correct angles """
    return scaled_voice_detection_angle_to_255


def _run_voice_detection_angle():
    """ Private: create a thread to poll the Mic Array and set the DOA Global Variable """
    print("EARS | Voice Detection     | Voice Detection Loop Starting")
    print("EARS | Voice Detection     | VAD: ", vad_threshold)
    # Counter to implement simple trigger for publishing to mqtt 
    mqtt_trigger_counter = 0
    # Mic_tuning.set_vad_threshold(vad_threshold)
    # Continue this block until the flag is raised to stop the thread - or the user interrupts
    while True:
        global _is_direction_of_arrival_stop_thread_flag
        global voice_detection_angle_to_360
        global Mic_tuning
        try:
            # Read the voice detected bool from the Mic tuninig script / hardware
            is_voice_detected = Mic_tuning.is_voice()
            if is_voice_detected:
                # Set the 0-360 degree var for direction of arrival
                voice_detection_angle_to_360 = Mic_tuning.direction
                print("EARS | Voice Detection     | Direction of Arrival: ",
                      voice_detection_angle_to_360)
                # Convert the angle to the byte size scale (0-360 to 0-255)
                global scaled_voice_detection_angle_to_255
                scaled_voice_detection_angle_to_255 = voice_detection_angle_to_360 / 360 * 255
            # Briefly sleep to prevent unecessary runaway
            time.sleep(0.3)
            # Simple Trigger to Publish the DOA every 6th loop (0.3 * 6) ~1.8 seconds
            mqtt_trigger_counter += 1
            if mqtt_trigger_counter == 6:
                # Publish the angle of arrival to the cloud via mqtt
                publish(mqtt_topic_mic_angle, {
                    "mic_direction_of_arrival": voice_detection_angle_to_360
                })
                # Once published, reset the trigger
                mqtt_trigger_counter = 0
        except KeyboardInterrupt:
            break
        if _is_direction_of_arrival_stop_thread_flag:
            print("Direction of Arrival Thread told to stop.")
            break


def get_vad_threshold():
    """ Public: Returns the voice detection threshold value (to 1000)"""
    return vad_threshold


def get_scaled_vad_threshold():
    """ Public: Returns the scaled voice detection threshold value (to 255) """
    return scaled_vad_threshold_to_255


def set_vad_threshold(make_code_requested_vad_threshold):
    """ Public: Re-set the VAD threshold """
    # NOTE: The VAD is accesible via custom function Jon wrote within tuning.py
    # print("" + Mic_tuning.get_VAD())
    # Confirm parameter is an int
    if isinstance(make_code_requested_vad_threshold, int):
        # Ensure parameter is within range
        # TODO find out what the range is.
        if 0 <= make_code_requested_vad_threshold <= 255:
            # Set scaled threshold
            global vad_threshold
            vad_threshold = int(make_code_requested_vad_threshold / 255 * 1000)
            global scaled_vad_threshold_to_255
            scaled_vad_threshold_to_255 = make_code_requested_vad_threshold
            print("EARS | Voice Detection     | VAD: ", vad_threshold)
        else:
            print("EARS | Voice Detection     | ERROR: make_code_requested_vad_threshold - parameter is not within range")
    else:
        print("EARS | Voice Detection     | ERROR: make_code_requested_vad_threshold - parameter is not an Int")


""" Private: Set the target for the direction_of_arrival Thread """
_direction_of_arrival_thread = threading.Thread(
    target=_run_voice_detection_angle, daemon=True)


def start_direction_of_arrival_thread():
    """ Public: Start the Direction of Arrival Thread """
    global _is_direction_of_arrival_stop_thread_flag
    _is_direction_of_arrival_stop_thread_flag = False
    print("EARS | Voice Detection     | Starting Direction of Arrival Thread")
    # Create a new thread without any parameters (args)
    # global doa_thread
    _direction_of_arrival_thread.start()


def stop_direction_of_arrival_thread():
    """ Public: Stop the Direction of Arrival Thread """
    print("EARS | Voice Detection     | Stopping Direction of Arrival Thread")
    global _is_direction_of_arrival_stop_thread_flag
    _is_direction_of_arrival_stop_thread_flag = True
    global _direction_of_arrival_thread
    _direction_of_arrival_thread.join()


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -
# KEYWORD RECOGNITION
# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

def get_user_keywords():
    """ Public: Returns all of the Keywords that the Bot is listening for """
    return user_keywords


def add_user_keyword(keyword):
    """ Public: Permits user to add a new word to the keywords list.
        Saved only during runtime - ephemeral """
    # Confirms the keyword is a string
    if isinstance(keyword, str):
        # Creates the keyword tuple and appends it to the list
        pair = (keyword, 1.0)
        user_keywords.append(pair)
        print("EARS | Keyword Recognition | New Keyword Added: ", keyword)
        print("EARS | Keyword Recognition | All User Keywords are: ", user_keywords)


def _keyword_recognition():
    """ Private: Main Keyword Recognition Thread Logic """
    r = sr.Recognizer()
    m = sr.Microphone()
    # Continue this block until the flag is raised to stop the thread
    while True:
        global _is_keyword_recognition_stop_thread_flag
        try:
            print("EARS | Keyword Recognition | Starting Up...")
            # Speech Recognition - ambient noise filter (send mic into it)
            with m as source:
                r.adjust_for_ambient_noise(source)
            print("EARS | Keyword Recognition | Set minimum energy threshold to {}".format(
                r.energy_threshold))
            # Main thread loop - listens for voices, checks against keywords and provides result...
            while True:
                print("EARS | Keyword Recognition | Ready and Listening...")
                with m as source:
                    audio = r.listen(source)
                print(
                    "EARS | Keyword Recognition | Voices detected >>> processing for keywords...")
                try:
                    global user_keywords
                    # Sphinx Keyword Recognition (on-board)
                    sphinx_value = r.recognize_sphinx(
                        audio, keyword_entries=user_keywords)
                    print(
                        "EARS | Keyword Recognition | * * KEYWORD RECOGNISED * * Sphinx Found:  \" {}\"".format(sphinx_value))
                    # Google Keyword Recognition
                    # google_value = r.recognize_google(audio, keyword_entries=user_keywords)
                    # print("EARS | Keyword Recognition | * * KEYWORD RECOGNISED * * Google Found:  {}".format(sphinx_value))
                    global has_recognised_keyword
                    has_recognised_keyword = True
                    # In the case of multi match: "BinBot, BinBot, BinBot" we only want to send the first instance of the sentence
                    single_keyword_method = sphinx_value.split()
                    # Publish the Keyword to the MQTT Broker (event based)
                    publish(mqtt_topic_keyword, { "mic_keyword": single_keyword_method[0] })
                except sr.UnknownValueError:
                    print(
                        "EARS | Keyword Recognition | *EXCEPTION* Unknown Value Heard...")
                except sr.RequestError as e:
                    print(
                        "EARS | Keyword Recognition | *EXCEPTION* Couldn't request results from Google Keyword Recognition service; {0}".format(e))
                if _is_keyword_recognition_stop_thread_flag:
                    print("Keyword Recognition Thread told to stop.(1)")
                    break
        except Exception:
            pass
        if _is_keyword_recognition_stop_thread_flag:
            print("Keyword Recognition Thread told to stop.(2)")
            break


""" Private: Set the target for the Keyword Recognition Thread """
_keyword_recognition_thread = threading.Thread(
    target=_keyword_recognition, daemon=True)


def start_keyword_recognition_thread():
    """ Public: Start up the Keyword Recognition Thread """
    print("EARS | Keyword Recognition | Starting Keyword Recognition Thread")
    global _is_keyword_recognition_stop_thread_flag
    _is_keyword_recognition_stop_thread_flag = False
    # Create a new thread without any parameters (args)
    # global _keyword_recognition
    _keyword_recognition_thread.start()


def stop_keyword_recognition_thread():
    """ Public: Stop the Keyword Recognition Thread """
    print("EARS | Keyword Recognition | Stopping Keyword Recognition Thread")
    global has_recognised_keyword
    has_recognised_keyword = False
    global _is_keyword_recognition_stop_thread_flag
    _is_keyword_recognition_stop_thread_flag = True
    global _keyword_recognition_thread
    _keyword_recognition_thread.join()
