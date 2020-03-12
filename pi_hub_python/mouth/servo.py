import time
from adafruit_servokit import ServoKit

kit = ServoKit(channels=16)

def mouth(action):
    if(action == 0):
        print("openMouth")
        kit.servo[0].angle = 40
    if(action == 1):
        print("close")
        kit.servo[0].angle = 180
    if(action == 2):
        print("talk")
        #kit.servo[0].angle = 180
        while True:
            kit.servo[0].angle = 140
            time.sleep(0.5)
            kit.servo[0].angle = 100
            time.sleep(1)
            kit.servo[0].angle = 180
            time.sleep(0.75)
            kit.servo[0].angle = 120
            time.sleep(0.5)
    if(action == 3):
        print("munch")
        while True:
            #kit.servo[0].angle = 180
            kit.continuous_servo[0].throttle = 1
            time.sleep(1.25)
            kit.continuous_servo[0].throttle = -1
            #time.sleep(1)
            #kit.servo[0].angle = 0
            kit.continuous_servo[0].throttle = 0
            time.sleep(1.25)
    elif((action < 0) or (action > 4)):
        print("No action.")