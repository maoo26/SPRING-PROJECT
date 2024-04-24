import RPi.GPIO as GPIO
import time
GPIO.setwarnings(False) #do not show any warnings

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
    pwmA.ChangeDutyCycle(50)
    pwmB.ChangeDutyCycle(30)
    #time.sleep(1)
    
def turnright():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(38)
    pwmB.ChangeDutyCycle(65)
    #time.sleep(1)

while 1: #execute forever
    command = input ('input:')
    if (command == 'r'):
        turnright()
        time.sleep(1)
        stop()
    if (command == 'l'):
        turnleft()
        time.sleep(1)
        stop()

GPIO.cleanup()
