import cv2
import numpy as np
import time
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

cap = cv2.VideoCapture(0)
cap.set(3, 160)
cap.set(4, 120)
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
pwmA.start(50) #start with 0% duty cycle
pwmB.start(50)

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
    pwmA.ChangeDutyCycle(60)
    pwmB.ChangeDutyCycle(50)
    time.sleep(4)
    
def stop():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    time.sleep(2)
    
def backward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(60)
    pwmB.ChangeDutyCycle(50)
    time.sleep(3)
    
def turnleft():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(40)
    #time.sleep(1)
    
def turnright():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(40)
    pwmB.ChangeDutyCycle(40)
    #time.sleep(1)
    
while True:
    ret, frame = cap.read()
    
    low_b = np.uint8([50,50,50])
    high_b = np.uint8([0,0,0])
    mask = cv2.inRange(frame, high_b, low_b)
    contours, hierarchy = cv2.findContours(mask, 1, cv2.CHAIN_APPROX_NONE)
    if len(contours) > 0 :
        C = max(contours, key=cv2.contourArea)
        M = cv2.moments(C)
        if M["m00"] !=0 :
            cx = int(M['m10']/M['m00'])
            cy = int(M['m01']/M['m00'])
            print("CX : "+str(cx)+"  CY : "+str(cy))
            if cx >= 120 :
                print("Turn Left")
                turnleft()
            if cx < 120 and cx > 40 :
                print("On Track!")
                forward()
            if cx <=40 :
                print("Turn Right")
                turnright()
            cv2.circle(frame, (cx,cy), 5, (255,255,255), -1)
    else :
        print("I don't see the line")
        stop()
        
    cv2.drawContours(frame, contours, -1, (0,255,0), 1)
    cv2.imshow("Mask",mask)
    cv2.imshow("Frame",frame)
    
    if cv2.waitKey(1) & 0xff == ord('q'):   # 1 is the time in ms
        stop()
        break
    
cap.release()
cv2.destroyAllWindows()
