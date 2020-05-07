import numpy as np
import cv2 as cv
import os


cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("camera not found")
    exit()


## setting up path
PATH = os.path.dirname(os.path.abspath(__file__))
print("current dir: ", PATH)


#client name ask
CLIENT_NAME = input("type name: ")
CLIENT_PATH = PATH + f"/{CLIENT_NAME}_images"


## checking same folder already exist?
if os.path.exists(os.path.abspath(CLIENT_PATH)):
    print("USER ALREADY EXIST!")   
else:
    os.mkdir(PATH + f"/{CLIENT_NAME}_images")


## start capturing
while True:
    ret, frame = cap.read()

    if not ret:
        print("frames not found!")
        break

    frame = cv.flip(frame, 1) # fliped
    gray = cv.cvtColor(frame, cv.COLOR_BGR2GRAY) #to gray

    cv.imshow("ready to capture", gray)

    if cv.waitKey(1) == ord('c'): # start capturing images
        cv.imwrite(PATH, gray)


##-------------------------EXIT
    if cv.waitKey(1) == 27: # 27 for ESC, ord(q)
        break

cv.destroyAllWindows()
