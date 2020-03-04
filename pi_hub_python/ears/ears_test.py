
import ears
import time

print("Starting EARS Thread")
ears.start_doa_thread()

print("Sleeping...")
time.sleep(5)

print("Set new VAD Threshold")
ears.set_vad_threshold(255)

print("Sleeping...")
time.sleep(5)

print("Set new VAD Threshold")
ears.set_vad_threshold(0)

print("Sleeping...")
time.sleep(5)