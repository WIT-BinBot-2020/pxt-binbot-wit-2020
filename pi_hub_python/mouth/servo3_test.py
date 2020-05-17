import threading
import time
from adafruit_servokit import ServoKit

# IN TEST PI HUB - SCRIPTNAME.start_FUNCTION_NAME_thread()
# '' - SCRIPTNAME.stop_YOUR_FUNCTION_thread()

# Initialise variables

kit = ServoKit(channels=16)

# Setting it do nothing while waiting for command
current_action = 5
_is_MOUTH_stop_thread_flag = False

def _run_MOUTH():
    while True:
        global _is_MOUTH_stop_thread_flag
        global current_action
        try:
            if current_action == 0:
                try:
                    print("Open: " + str(current_action))
                    # Set angle to 'open' state
                    kit.servo[0].angle = 40
                    # Calling option number 5 to 'do nothing' while waiting for new request
                    MOUTH(5)
                except Exception:
                    print("Error")
                    break
            if current_action == 1:
                try:
                    print("Close: " + str(current_action))
                    # Set angle to 'close' state
                    kit.servo[0].angle = 180
                    MOUTH(5)
                except Exception:
                    print("Error")
                    break
            if current_action == 2:
                try:
                    
                    print("Talk: " + str(current_action))
                    # Setting motor to varius angles to give talking effect
                    kit.servo[0].angle = 140
                    time.sleep(0.5)
                    kit.servo[0].angle = 100
                    time.sleep(1)
                    kit.servo[0].angle = 180
                    time.sleep(0.75)
                    kit.servo[0].angle = 120
                    
                    time.sleep(0.5)
                except Exception:
                    print("Error")
                    break
            if current_action == 3:
                try:
                    print("Munch: " + str(current_action))
                    # Fully opening and closing motor to give eating effect
                    #kit.continuous_servo[0].throttle = 1
                    #time.sleep(1.25)
                    #kit.continuous_servo[0].throttle = -1
                    #kit.continuous_servo[0].throttle = 0
                    #time.sleep(1.25)
                    
                    # Above commented out code threw errors for 360 degree motor - using following code for that
                    kit.servo[0].angle = 40
                    time.sleep(0.5)
                    kit.servo[0].angle = 100
                    time.sleep(1)
                    kit.servo[0].angle = 180
                    time.sleep(0.75)
                    
                except Exception:
                    print("Error 3")
                    break
            if current_action == 4:
                try:
                    print("Stopping: " + str(current_action))
                    # Stopping thread
                    _is_MOUTH_stop_thread_flag = True
                    #break
                except Exception:
                    print("Error 4")
                    break
            elif current_action == 5:
                try:
                    # Waiting for something to do
                    print("Nothing to do")
                    time.sleep(0.5)
                except Exception:
                    print("Error")
        except Exception:
            print("Error")       
        
        # if 'stop the thread' == true then stop program
        if _is_MOUTH_stop_thread_flag:
            print("Function told to stop")
            break
        
# Setting thread target (the function that controls the motor)
_MOUTH_thread = threading.Thread(target=_run_MOUTH, daemon = True)

def start_MOUTH_thread():
    global _is_MOUTH_stop_thread_flag
    is_MOUTH_stop_thread_flag = False
    _MOUTH_thread.start()
    
def stop_MOUTH_thread():
    global _is_MOUTH_stop_thread_flag
    _is_MOUTH_stop_thread_flag = True
    global __MOUTH_thread
    _MOUTH_thread.join()
    
start_MOUTH_thread()

# To recieve a value from the makecode blocks and pass it through to the motor function.
# It's originally set as 'Nothing to do'/ option 5
def MOUTH(action):
    global current_action
    global new_thr_request
    global __MOUTH_thread
    # Setting value from passed parameter, i.e 0, 1, 2, 3, 5
    current_action = action
    
    #if _MOUTH_thread.is_alive():
    