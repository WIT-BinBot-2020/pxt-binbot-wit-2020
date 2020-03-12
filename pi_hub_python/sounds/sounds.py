import pyaudio
import wave


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


def close_stream():
    print("Checking Stream")
    global stream
    if stream is not None:
        stream.close()


def play_sound(sound_number):
    global stream
    close_stream()
    sound = sounds.get(sound_number)
    if sound:
        sound_file = wave.open(sound, 'rb')
        stream = p.open(format=p.get_format_from_width(sound_file.getsampwidth()),
                        channels=sound_file.getnchannels(),
                        rate=sound_file.getframerate(),
                        output=True)

        # Read data in chunks
        data = sound_file.readframes(chunk)

        stream.write(data)

        while data:
            stream.write(data)
            data = sound_file.readframes(chunk)
        stream.close()
    else:
        print("No Sound Associated")
