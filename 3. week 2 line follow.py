import cv2
import numpy as np
import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False)

# define a video capture object
vid = cv2.VideoCapture(0)
  
ENA = 13
IN1 = 16
IN2 = 20
IN3 = 21
IN4 = 26
ENB = 19
LRE = 5
RRE = 6

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)    
GPIO.setup(IN2, GPIO.OUT)    
GPIO.setup(IN3, GPIO.OUT)    
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
pwmA = GPIO.PWM(ENA,100) #PWM frequency is set to 100Hz
pwmB = GPIO.PWM(ENB,100)
pwmA.start(0) #start with 0% duty cycle
pwmB.start(0)

# Initial state
GPIO.output(IN1, GPIO.LOW)
GPIO.output(IN2, GPIO.LOW)
GPIO.output(IN3, GPIO.LOW)
GPIO.output(IN4, GPIO.LOW)

def forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(47)#30 #36
    pwmB.ChangeDutyCycle(37)#20 #36
    
def backward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(32)
    pwmB.ChangeDutyCycle(42)
    
def stop():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    
def turnleft(a,b):
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(a) #40 #42 #39
    pwmB.ChangeDutyCycle(b) #30 #39 #36

    
def turnright(a,b):
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(a) #37 #35 #42 #36
    pwmB.ChangeDutyCycle(b) #40 #38 #44 #39



while(True):
    
    # Capture the video frame by frameq
    ret, frame = vid.read()
    
    # Rotate the frame by 180 degrees
    #frame = cv2.rotate(frame, cv2.ROTATE_180)
    
    # Define the y-coordinate range for the ROI
    y_top = 100  # Example top y-coordinate
    y_bottom = 480  # Example bottom y-coordinate
    
    # Crop the frame to the specified ROI
    cropped_frame = frame[y_top:y_bottom, :]
    
    # differentiate black lines from rest of the frames
    low_black = np.uint8([60,60,60]) 
    high_black = np.uint8([0,0,0]) #hsv
    mask = cv2.inRange(cropped_frame, high_black, low_black)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        C = max(contours, key=cv2.contourArea)
        M = cv2.moments(C)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            # Adjusting centroid coordinates for cropping offset
            cy_adjusted = cy + y_top
            print("CX : "+str(cx)+"  CY : "+str(cy_adjusted))
            if cx <= 260 : 
                print("Turn Left")
                turnleft(51,46)
                
            if cx < 415 and cx > 260 :
                print("On Track!")
                forward()
                
            if cx >= 415 :
                print("Turn Right")
                turnright(52,51)
                
            if cy_adjusted >= 350 and cx <= 140: #160
                turnleft(58,48)
                print("Turn Left -----------------------")
                
            if cy_adjusted >= 350 and cx >= 520: #500
                print("Turn Right -----------------------")
                turnright(51,56)
            cv2.circle(frame, (cx,cy_adjusted), 5, (255,255,255), -1)
    else :
        print("I don't see the line")
        backward()
        
    cv2.drawContours(cropped_frame, contours, -1, (0,255,0), 1)
    #lower_black = np.uint8([50,50,50])w
          
    cv2.imshow("Mask", mask)
    cv2.imshow('frame', cropped_frame)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
