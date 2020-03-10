""" Imports & Initial OpenMV Cam Setup """
#==========================================#
import sensor, image, time, math, pyb

usb = pyb.USB_VCP()

threshold_index = 0 # Index of array below:

# Color Tracking Thresholds (L Min, L Max, A Min, A Max, B Min, B Max)
thresholds = [(30, 100, 15, 127, 15, 127),   # generic_red_thresholds
              (40, 100, -100, -50, 30, 60),  # green_ball_thresholds
              (0, 50, -20, 40, -128, -60)]   # blue_threshold

sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 2000)
sensor.set_auto_gain(False) # must be turned off for color tracking
sensor.set_auto_whitebal(False) # must be turned off for color tracking
clock = time.clock()

# Only blobs that with more pixels than "pixel_threshold" and more area than "area_threshold" are
# returned by "find_blobs" below. Change "pixels_threshold" and "area_threshold" if you change the
# camera resolution. "merge=True" merges all overlapping blobs in the image.

while(True):
    clock.tick()
    img = sensor.snapshot()
    for blob in img.find_blobs([thresholds[threshold_index]], pixels_threshold=200, area_threshold=200):
        # These values depend oan the blob not being circular - otherwise they will be shaky.
        if blob.elongation() > 0.5:
            img.draw_edges(blob.min_corners(), color=(255,0,0))
            img.draw_line(blob.major_axis_line(), color=(0,255,0))
            img.draw_line(blob.minor_axis_line(), color=(0,0,255))
        # These values are stable all the time.
        img.draw_rectangle(blob.rect())
        img.draw_cross(blob.cx(), blob.cy())
        # Note - the blob rotation is unique to 0-180 only.
        img.draw_keypoints([(blob.cx(), blob.cy(), int(math.degrees(blob.rotation())))], size=20)
        #print("Test Object_X: ", blob.cx(), "Test Object_Y: ",blob.cy())
        usb.send("Object_X: %d | Object_Y: %d \n" % (blob.cx(), blob.cy()), timeout=100)
    #print(clock.fpTest s())
