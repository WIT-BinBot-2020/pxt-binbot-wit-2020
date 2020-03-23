
import ears
import time

print("TEST >> Starting EARS DOA Thread")
ears.start_direction_of_arrival_thread()
print("TEST >> Starting EARS Keyword Thread")
ears.start_keyword_recognition_thread()

print("TEST >> Sleeping...")
time.sleep(5)

print("TEST >> RESET VAD...")
ears.set_vad_threshold(150)


print("TEST >> Add New Keyword...")
ears.add_user_keyword("hello")


# print("TEST >> Stop Threads")
# ears.stop_direction_of_arrival_thread()
# ears.stop_keyword_recognition_thread()


while True:
    time.sleep(2)
    print("TEST >> keeping main thread alive...")

# print("TEST >> Set new VAD Threshold")
# ears.set_vad_threshold(255)

# print("TEST >> Sleeping...")
# time.sleep(5)

# print("TEST >> Set new VAD Threshold")
# ears.set_vad_threshold(0)

# print("TEST >> Sleeping...")
# time.sleep(5)