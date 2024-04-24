import cv2
import numpy as np
import RPi.GPIO as GPIO
from picamera.array import PiRGBArray
from picamera import PiCamera
import time
import os

GPIO.setwarnings(False)

# Initialize the Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(0.1)

# Define GPIO pins for motor control
ENA = 13
IN1 = 16
IN2 = 20
IN3 = 21
IN4 = 26
ENB = 19

# Initialize GPIO settings
GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)    
GPIO.setup(IN2, GPIO.OUT)    
GPIO.setup(IN3, GPIO.OUT)    
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)


pwmA = GPIO.PWM(ENA, 100) # PWM frequency is set to 100Hz
pwmB = GPIO.PWM(ENB, 100)
pwmA.start(0) # Start with 0% duty cycle
pwmB.start(0)

# Initial state for motor control
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

# Template matching parameters

text = ['rectangle', 'triangle', 'partial circle', 'hexagon', 'circle', 'pentagon',
        'left', 'right', 'up', 'down']
threshold = [0.5, 0.75, 0.7, 0.77, 0.7, 0.88,
             0.7, 0.7, 0.7, 0.7]
#threshold = [0.31, 0.22, 0.36, 0.25, 0.25, 0.17, 0.15, 0.50, 0.35, 0.20, 0.25]
template_folder = '/home/pi/Desktop/template fast/shape merged'
#threshold = [0.7, 0.75, 0.55, 0.6, 0.57, 0.55, 1]
#template_folder = '/home/pi/Desktop/template fast/attachments (6)'
"""
text = ['left','right','up','down']
#threshold = [0.73,0.73,0.76,0.85] #arrow
threshold = [0.7,0.7,0.7,0.8]
template_folder = '/home/pi/Desktop/template fast/arrow zoom'
"""
template_files = sorted([f for f in os.listdir(template_folder) if f.endswith('.png')])
templates = []
for filename in template_files:
    if filename.endswith('.jpg') or filename.endswith('.png'):
        template_path = os.path.join(template_folder, filename)
        template = cv2.imread(template_path,0)
        templates.append(template)

"""
text = ["a","b"]
threshold = [0.7,0.5]
template_paths = ['/home/pi/Desktop/template fast/resized/a. pentagon.png',
                  '/home/pi/Desktop/template fast/resized/c partial circle 2.png']
# Load templates
templates = [cv2.imread(path, cv2.IMREAD_GRAYSCALE) for path in template_paths]
"""
# Line following parameters
y_top = 200
y_bottom = 480

roi_x, roi_y, roi_width, roi_height = 0, 90, 420, 300

# Motor control functions
def forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(29.5) #47
    pwmB.ChangeDutyCycle(19.5) #37

def backward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(32) #32
    pwmB.ChangeDutyCycle(42) #42

def stop():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)

def turnleft(a, b):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(a)
    pwmB.ChangeDutyCycle(b)

def turnright(a, b):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(a)
    pwmB.ChangeDutyCycle(b)

def movement(contours):
    C = max(contours, key=cv2.contourArea)
    M = cv2.moments(C)
    if M["m00"] !=0 :
        cx = int(M['m10']/M['m00'])
        cy = int(M['m01']/M['m00'])
        cy_adjusted = cy + y_top
        if cx <= 260 : 
            turnleft(46,41) #51,46 #48,43
            
        if cx < 415 and cx > 260 :
            forward()
            
        if cx >= 415 : 
            turnright(47,46) #52,51 #49,48
            
        if cy_adjusted >= 350 and cx <= 140: #160
            turnleft(58,48)
            
        if cy_adjusted >= 350 and cx >= 520: #500
            turnright(51,56)

def linefollow(img):
    # Crop the frame to the specified ROI
    cropped_frame = img[y_top:y_bottom, :]

    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)

    # Define the range for red color in HSV format
    low_c1 = np.array([40, 100, 72])
    high_c1 = np.array([80, 255, 255])
    
    # Create a mask to isolate red color
    c1_mask = cv2.inRange(hsv_frame, low_c1, high_c1)
    
    # Find contours in the red mask
    c1_contours, _ = cv2.findContours(c1_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
    
    # Define the range for red color in HSV format
    low_c2 = np.array([100, 100, 40])
    high_c2 = np.array([140, 255, 255])
    
    # Create a mask to isolate red color
    c2_mask = cv2.inRange(hsv_frame, low_c2, high_c2)

    # Find contours in the red mask
    c2_contours, _ = cv2.findContours(c2_mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

    # For black line
    low_black = np.uint8([0,0,0]) 
    high_black = np.uint8([48,48,48]) #rgb
    mask = cv2.inRange(cropped_frame, low_black, high_black)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)

    # Line following
    if len(c1_contours) > 0:
        movement(c1_contours)
        #cv2.imshow("c1Mask", c1_mask)
        #cv2.circle(frame, (c1_cx,c1_cy_adjusted), 5, (255,255,255), -1)
    elif len(c2_contours) > 0:
        movement(c2_contours)
        #cv2.imshow("c2Mask", c2_mask)
        #cv2.circle(frame, (c2_cx,c2_cy_adjusted), 5, (255,255,255), -1)
    elif len(contours) > 0 :
        movement(contours)
        #cv2.imshow("Mask", mask)
        #cv2.circle(frame, (cx,cy_adjusted), 5, (255,255,255), -1)
        else :
            #print("I don't see the line")
            backward()
    #cv2.imshow("cropped", cropped_frame)

def templatematching(img):
    roi = img[roi_y:roi_y + roi_height, roi_x:roi_x + roi_width]
    gray_roi = cv2.cvtColor(roi, cv2.COLOR_BGR2GRAY)

    alpha = 1.5  # Contrast control (1.0-3.0)
    beta = 60  # Brightness control (0-100)

    # Apply contrast and brightness adjustment
    adjusted_gray_roi = cv2.convertScaleAbs(gray_roi, alpha=alpha, beta=beta)
    
    for i in range(len(templates)):
        template = templates[i]
        shape_name = text[i]
        result = cv2.matchTemplate(adjusted_gray_roi, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if max_val > threshold[i]:
            location = (max_loc[0], max_loc[1])
            h, w = template.shape
            bottom_right = (location[0] + template.shape[1], location[1] + template.shape[0])
            cv2.rectangle(adjusted_gray_roi, location, bottom_right, 100, 5)
            cv2.putText(adjusted_gray_roi, shape_name, (location[0], location[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(shape_name, ":", max_val)
            
        #else:
            #print(shape_name,"not detected")
    if i == len(templates) - 1:
        i = -1  # Reset index to -1 so that it becomes 0 in the next iteration
    #cv2.imshow('template',templates[6])
    cv2.imshow('roi',adjusted_gray_roi)

# Main loop
for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    img = frame.array
    # Line following
    linefollow(img)
    # Template matching
    templatematching(img)

    #cv2.imshow('template',templates[4])
    #cv2.imshow('Line Following and Template Matching', img)
    # Clear the stream for the next frame
    rawCapture.truncate(0)

    # Exit the loop if 'q' is pressed
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Release GPIO resources
GPIO.cleanup()
cv2.destroyAllWindows()
