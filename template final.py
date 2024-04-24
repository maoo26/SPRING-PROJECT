import cv2
import os
from picamera.array import PiRGBArray
from picamera import PiCamera
import time

# Initialize the Pi camera
camera = PiCamera()
camera.resolution = (640, 480)
camera.framerate = 30
rawCapture = PiRGBArray(camera, size=(640, 480))

# Allow the camera to warm up
time.sleep(0.1)

#text = ['rectangle', 'circle', 'square', 'hexagon', 'left arrow', 'partial circle', 'triangle', 'pentagon']
#text = ['pentagon', 'triangle', 'partial circle', 'left arrow', 'hexagon', 'square', 'circle', 'rectangle']
text = ['pentagon', 'triangle', 'partial circle', 'left arrow', 'hexagon', 'square', 'circle', 'rectangle',
        'right arrow', 'down arrow','up arrow']
fxfy = [
    [0.15,0.15],
    [0.17,0.17],
    [0.70,0.70],
    [0.55,0.55],
    [0.30,0.30],
    [0.55,0.55],
    [0.50,0.50],
    [0.55,0.55],
    [0.55,0.55],
    [0.55,0.55],
    [0.55,0.55]]
#threshold = [0.6, 0.55, 0.53, 0.5, 0.49, 0.46, 0.4, 0.37]
#threshold = [0.37, 0.4, 0.46, 0.49, 0.5, 0,52, 0.55, 0.6]
threshold = [0.15, 0.27, 0.16, 0.50, 0.25, 0.17, 0.17, 0.15, 0.35, 0.20, 0.25]
template_folder = '/home/pi/Desktop/template w bg'
template_files = sorted([f for f in os.listdir(template_folder) if f.endswith('.jpg') or f.endswith('.png')])
templates = []
for filename in template_files:
    if filename.endswith('.jpg') or filename.endswith('.png'):
        template_path = os.path.join(template_folder, filename)
        template = cv2.imread(template_path, 0)
        templates.append(template)
        
# Read the template image
#template = cv2.imread('/home/pi/Downloads/shapes/partial circle.png', 0)
        


# Template matching
methods = [cv2.TM_CCOEFF, cv2.TM_CCOEFF_NORMED, cv2.TM_CCORR,
            cv2.TM_CCORR_NORMED, cv2.TM_SQDIFF, cv2.TM_SQDIFF_NORMED]


for frame in camera.capture_continuous(rawCapture, format="bgr", use_video_port=True):
    # Grab the raw NumPy array representing the image
    img = frame.array

    # Convert the captured frame to grayscale
    gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

    #for method in methods:
    img2 = gray_img.copy()


    for i in range(len(templates)):
        fx, fy = fxfy[i]
        template = cv2.resize(templates[i], (0, 0), fx=fx, fy=fy)
        shape_name = text[i]
        result = cv2.matchTemplate(img2, template, cv2.TM_CCOEFF_NORMED)
        min_val, max_val, min_loc, max_loc = cv2.minMaxLoc(result)
        if (max_val > 1 - threshold[i]):
            location = max_loc
            h, w = template.shape
            bottom_right = (location[0] + template.shape[1], location[1] + template.shape[0])
            cv2.rectangle(img, location, bottom_right, 100, 5)
            cv2.putText(img, shape_name, (location[0], location[1] - 10), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 255, 0), 2)
            print(shape_name,":",max_val)
        else:
            print(shape_name,"not detected")
        cv2.imshow('Match1', templates[4])
    cv2.imshow('Match', img)

    # Clear the stream for the next frame
    rawCapture.truncate(0)
   
    # If 'q' is pressed, exit the loop
    if cv2.waitKey(1) & 0xFF == ord('q'):
        break

# Reset index variable if it reaches the end of the list
    if i == len(templates) - 1:
        i = -1  # Reset index to -1 so that it becomes 0 in the next iteration
        
# Close all OpenCV windows
cv2.destroyAllWindows()
