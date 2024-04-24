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
diskslots = 40
counter1 = 0
counter2 = 0
initial1 = 0
initial2 = 0
distance = 0
distance1 = 0
distance2 = 0
circumference = 6.7*3.142

GPIO.setmode(GPIO.BCM)
GPIO.setup(ENA, GPIO.OUT)
GPIO.setup(IN1, GPIO.OUT)    
GPIO.setup(IN2, GPIO.OUT)    
GPIO.setup(IN3, GPIO.OUT)    
GPIO.setup(IN4, GPIO.OUT)
GPIO.setup(ENB, GPIO.OUT)
GPIO.setup(LRE, GPIO.IN)
GPIO.setup(RRE, GPIO.IN)
pwmA = GPIO.PWM(ENA,100) #PWM frequency is set to 100Hz
pwmB = GPIO.PWM(ENB,100)
pwmA.start(0) #start with 0% duty cycle
pwmB.start(0)

def count1():
    global initial1
    global counter1
    final1 = GPIO.input(LRE)
    if(final1 != initial1):
        counter1+=1
        initial1 = final1
        
def count2():
    global initial2
    global counter2
    final2 = GPIO.input(RRE)
    if(final2 != initial2):
        counter2+=1
        initial2 = final2
        
def calc_distance():
    distance1=counter1/diskslots*circumference*100
    distance2=counter2/diskslots*circumference*100
    distance=(distance1+distance2)/2
    print("distance:",distance)

def forward():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(60)
    pwmB.ChangeDutyCycle(50)
    count1()
    count2()
    calc_distance()
    #time.sleep(1)
    
def stop():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(0)
    pwmB.ChangeDutyCycle(0)
    #time.sleep(4)
    
def backward():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(60)
    pwmB.ChangeDutyCycle(50)
    count1()
    count2()
    #time.sleep(3)
    
def turnleft():
    GPIO.output(IN1, GPIO.LOW)
    GPIO.output(IN2, GPIO.HIGH)
    GPIO.output(IN3, GPIO.LOW)
    GPIO.output(IN4, GPIO.HIGH)
    pwmA.ChangeDutyCycle(70)
    pwmB.ChangeDutyCycle(40)
    count1()
    count2()
    #time.sleep(1)
    
def turnright():
    GPIO.output(IN1, GPIO.HIGH)
    GPIO.output(IN2, GPIO.LOW)
    GPIO.output(IN3, GPIO.HIGH)
    GPIO.output(IN4, GPIO.LOW)
    pwmA.ChangeDutyCycle(50)
    pwmB.ChangeDutyCycle(60)
    count1()
    count2()
    #time.sleep(1)
   
while 1: #execute forever
    
    command = input("input:")
    if (command == "forward"):
        forward()
    if (command == "backward"):
        backward()
        calc_distance()
    if (command == "stop"):
        stop()
    if (command == "left"):
        turnleft()
        calc_distance()
    if (command == "right"):
        turnright()
        calc_distance()
    if (command == 'distance'):
        calc_distance()
    
    
GPIO.cleanup()
