# ReSpeaker Microphone Array v2.0 Code for BinBot


# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

# FOR USE WITHIN THE RPI HUB
# 1. ANGLE OF VOICE DETECTION USE within a loop : "ears.scaled_voice_detection_angle"

# - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - - -

print("ears.py | Loading Ears.py Script")

from tuning import Tuning
import usb.core
import usb.util
import time
import logging
import threading

""" Global Variables used by the Mic Array """
vad_threshold = 300

""" Public Global Variables set by the Mic Array thread and available to reference publicly """
# Referenced by Controller (pi_hub.py) >> Ensure used within a polling loop or framework
voice_detection_angle = 0
scaled_voice_detection_angle = 0

""" Private Global Variables """
vad_range_max = 1000  # Limit Set by MicArray Tuning
_is_stop_thread_flag = False

""" Initialisation of the Mic Array """
# Find the ReSpeaker in the list of devices connected.
dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
# Loop until ReSpeaker is found - unlikely but for insurance.
while not dev:
    print("ears.py | Looking for Mic Array")
    dev = usb.core.find(idVendor=0x2886, idProduct=0x0018)
if dev:
    print("ears.py | Found Mic Array")
    Mic_tuning = Tuning(dev)
    # Mic_tuning.set_HPFONOFF(3) I think this has to run on the CLI as param


def _run_voice_detection_loop_thread():
    """ Private: create a thread to poll the Mic Array and set the DOA Global Variable """
    print("ears.py | THREAD: Voice Detection Loop Starting")
    # Mic_tuning.set_vad_threshold(vad_threshold)
    while True:
        global voice_detection_angle
        global Mic_tuning
        try:
            is_voice_detected = Mic_tuning.is_voice()
            if is_voice_detected:
                voice_detection_angle = Mic_tuning.direction
                print("ears.py | THREAD: Voice Direction of Arrival: ", voice_detection_angle)
                global scaled_voice_detection_angle
                scaled_voice_detection_angle = voice_detection_angle / 360 * 255

            time.sleep(0.5)
        except KeyboardInterrupt:
            break
        if _is_stop_thread_flag:
            break


""" Set the target for the DOA Thread """
doa_thread = threading.Thread(target=_run_voice_detection_loop_thread, daemon=True)


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

            # Restart Thread as the VAD has changed (instead of 'setting' the VAD within the thread infinite loop.)
            # _stop_doa_thread()
            # start_doa_thread()

        else:
            print("ears.py | ERROR: make_code_requested_vad_threshold - parameter is not within range")
    else:
        print("ears.py | ERROR: make_code_requested_vad_threshold - parameter is not an Int")


def start_doa_thread():
    # Public: start the main DOA thread
    # Ensure the stop flag is off before starting a new thread
    global _is_stop_thread_flag
    _is_stop_thread_flag = False
    print("ears.py | Starting DOA Loop Thread")
    # Create a new thread without any parameters (args)
    # global doa_thread
    doa_thread.start()


def _stop_doa_thread():
    # Private: stop the currently running thread and reset the flag
    print("ears.py | Stopping DOA Loop Thread")
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


start_doa_thread()

# REFERENCES
# Threading: https://realpython.com/intro-to-python-threading/#starting-a-thread
