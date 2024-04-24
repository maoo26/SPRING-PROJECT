import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os
import follow
import template


GPIO.setwarnings(False)

# Initialize the Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(0.1)


# Line following parameters
y_top = 100
y_bottom = 480

    
# Main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    
    follow.linefollow(img, y_top, y_bottom)

    # Template matching
    #template.shapedetection(img)

    #cv2.imshow('roi',adjusted_gray_roi)
    #cv2.imshow('template',templates[4])
    cv2.imshow('Line Following and Template Matching', img)
    # Clear the stream for the next frame
    rawCapture.truncate(0)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release GPIO resources
GPIO.cleanup()
cv2.destroyAllWindows()
