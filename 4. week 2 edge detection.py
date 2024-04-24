import cv2
import numpy as np
import RPi.GPIO as GPIO
GPIO.setwarnings(False)

# define a video capture object
vid = cv2.VideoCapture(0)

while(True):
# Capture the video frame by frameq
    ret, frame = vid.read()

# Convert BGR to HSV
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    low_w = np.array([0,0,170]) 
    high_w = np.array([180,25,255]) #hsv
    mask = cv2.inRange(hsv, low_w, high_w)
# Load and preprocess an Image
    #image = cv2.imread('image.png')
    #gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    blur = cv2.GaussianBlur(frame, (5, 5), 0)

# Perform edge detection
    edges = cv2.Canny(blur, 30, 150)

# Find contours
    contours, _ = cv2.findContours(edges.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)

# Classifying shapes
    for contour in contours:
        epsilon = 0.04 * cv2.arcLength(contour, True)
        approx = cv2.approxPolyDP(contour, epsilon, True)
        vertices = len(approx)
        if vertices == 7:
            shape = "Arrow"
        elif vertices == 5:
            shape = "Pentagon"
        elif vertices == 4:
            (x, y, w, h) = cv2.boundingRect(approx)
            ar = w / float(h)
            shape = "square" if ar >= 0.95 and ar <= 1.05 else "rectangle"
        elif vertices == 3:
            shape = "Triangle"
        else :
            shape = "Circle"
    
        cv2.drawContours(frame, [approx], 0, (0, 255, 0), 2)
        cv2.putText(frame, shape, (approx[0][0][0], approx[0][0][1]+5), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)

# Save Results
    cv2.imshow('frame', frame)
    #cv2.imshow('mask', mask)
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# After the loop release the cap object
vid.release()
# Destroy all the windows
cv2.destroyAllWindows()
