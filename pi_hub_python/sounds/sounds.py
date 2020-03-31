import pyaudio
import wave
import threading

print("sounds.py | Loading Sounds.py Script")

# All Sound files
sounds = [
    (0, '../assets/sound_files/mouthOpen.wav'),
    (1, '../assets/sound_files/mouthClose.wav'),
    (2, '../assets/sound_files/robotStop.wav'),
    (3, '../assets/sound_files/shutdown.wav'),
    (4, '../assets/sound_files/startup.wav')
]
sounds = dict(sounds)

# Set chunk size of 1024 samples per data frame
chunk = 1024
stream = None

# Create an interface to PortAudio
p = pyaudio.PyAudio()

# Globals
current_sound_number = -1
playing_new_sound = False
should_play_sound = False
_stop_play_sound_thread_flag = False


""" Thread function to constantly check if a sound needs to be played """
def _continuously_play_sound():
    while True:

        # Continuously check if a sound should be played
        global should_play_sound
        global stream
        if should_play_sound:
            # Playing a new sound

            # Ensure that it doesn't loop the first sound forever
            global playing_new_sound
            if playing_new_sound:
                playing_new_sound = False

            global current_sound_number
            sound = sounds.get(current_sound_number)
            if sound:
                sound_file = wave.open(sound, 'rb')
                stream = p.open(format=p.get_format_from_width(sound_file.getsampwidth()),
                                channels=sound_file.getnchannels(),
                                rate=sound_file.getframerate(),
                                output=True)

                # Read data in chunks
                data = sound_file.readframes(chunk)

                while data:
                    # Stop playing the sound if a new one is detected
                    if playing_new_sound:
                        break

                    stream.write(data)
                    data = sound_file.readframes(chunk)
                stream.close()
            else:
                print("No Sound Associated")

            # Play the next sound if a new sound is detected
            if not playing_new_sound:
                should_play_sound = False
                playing_new_sound = False

            # Stop the thread if told
            if _stop_play_sound_thread_flag:
                break


_play_sound_thread = threading.Thread(target=_continuously_play_sound, daemon=True)


def start_play_sound_thread():
    global _stop_play_sound_thread_flag
    _stop_play_sound_thread_flag = False
    # Create a new thread without any parameters (args)
    _play_sound_thread.start()


def stop_play_sound_thread():
    global _stop_play_sound_thread_flag
    _stop_play_sound_thread_flag = True
    global _play_sound_thread
    _play_sound_thread.join()


""" This line below must be kept! """
start_play_sound_thread()


""" Public function that a user calls in order to play a new sound """
def play_sound(sound_number):
    # Change globals to indicate that a new sound should be played
    global current_sound_number
    current_sound_number = sound_number
    global playing_new_sound
    playing_new_sound = True
    global should_play_sound
    should_play_sound = True
