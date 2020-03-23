
import ears
import time

print("TEST >> Starting EARS Thread")
ears.start_doa_thread()

print("TEST >> Sleeping...")
time.sleep(5)

print("TEST >> Stop Thread")
time.sleep(5)


while True:
    time.sleep(2)
    print("TEST >> loop...")








print("TEST >> ")


# print("TEST >> Set new VAD Threshold")
# ears.set_vad_threshold(255)

# print("TEST >> Sleeping...")
# time.sleep(5)

# print("TEST >> Set new VAD Threshold")
# ears.set_vad_threshold(0)

# print("TEST >> Sleeping...")
# time.sleep(5)