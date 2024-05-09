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

colour_ranges = {
    "r" : ([0,100,100],[10,255,255]),
    "y" : ([20,100,100],[40,255,255]),
    "g" : ([40,40,40],[80,255,255]),
    "b" : ([100,100,50],[140,255,255]),
}

colours = input("Enter colours:").split(',')
colour = [colour.strip() for colour in colours]
#print(colour[0]+colour[1])

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
    
    # Define the range for red color in HSV format
    
    # Convert the frame to HSV color space
    hsv_frame = cv2.cvtColor(cropped_frame, cv2.COLOR_BGR2HSV)
    
    colour_masks ={}
    for colour in colours:
        low_colour, high_colour = colour_ranges[colour]
        colour_masks[colour] = cv2.inRange(hsv_frame, np.array(low_colour), np.array(high_colour))
        #print(colour)
        colour_contours, _ = cv2.findContours(colour_masks[colour], cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
        if len(colour_contours) > 0:
            colour_contour = max(colour_contours, key=cv2.contourArea)
            colour_moments = cv2.moments(colour_contour)
            if colour_moments["m00"] != 0:
                colour_cx = int(colour_moments['m10'] / colour_moments['m00'])
                colour_cy = int(colour_moments['m01'] / colour_moments['m00'])
                colour_cy_adjusted = colour_cy + y_top
                #print(colour +" CX : "+str(colour_cx)+"  CY : "+str(colour_cy_adjusted))
                if colour_cx <= 260 : 
                    #print("Turn Left")
                    turnleft(51,46)
                    
                if colour_cx < 415 and colour_cx > 260 :
                    #print("On Track!")
                    forward()
                    
                if colour_cx >= 415 :
                    #print("Turn Right")
                    turnright(52,51)
                    
                if colour_cy_adjusted >= 350 and colour_cx <= 140: #160
                    turnleft(58,48)
                    #print("Turn Left -----------------------")
                    
                if colour_cy_adjusted >= 350 and colour_cx >= 520: #500
                    #print("Turn Right -----------------------")
                    turnright(51,56)
                #cv2.imshow("ColourMask", colour_mask)
                #cv2.circle(frame, (colour_cx,colour_cy_adjusted), 5, (255,255,255), -1)
        else:
            low_black = np.uint8([0,0,0]) 
            high_black = np.uint8([48,48,48]) #hsv
            mask = cv2.inRange(cropped_frame, low_black, high_black)
            contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
            if len(contours) > 0 :
                C = max(contours, key=cv2.contourArea)
                M = cv2.moments(C)
                if M["m00"] !=0 :
                    cx = int(M['m10']/M['m00'])
                    cy = int(M['m01']/M['m00'])
                    cy_adjusted = cy + y_top
                    #print("black CX : "+str(cx)+"  CY : "+str(cy_adjusted))
                    if cx <= 260 : 
                        #print("Turn Left")
                        turnleft(51,46)
                        
                    if cx < 415 and cx > 260 :
                        #print("On Track!")
                        forward()
                        
                    if cx >= 415 :
                        #print("Turn Right")
                        turnright(52,51)
                        
                    if cy_adjusted >= 350 and cx <= 140: #160
                        turnleft(58,48)
                        #print("Turn Left -----------------------")
                        
                    if cy_adjusted >= 350 and cx >= 520: #500
                        #print("Turn Right -----------------------")
                        turnright(51,56)
                #cv2.imshow("Mask", mask)
                #cv2.circle(frame, (cx,cy_adjusted), 5, (255,255,255), -1)
            else :
                #print("I don't see the line")
                backward()
            
            #cv2.drawContours(cropped_frame, contours, -1, (0,255,0), 1)
    
    #cv2.imshow('frame', cropped_frame)
    
    # the 'q' button is set as the
    # quitting button you may use any
    # desired button of your choice
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break
  
# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()


