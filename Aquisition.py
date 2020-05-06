import numpy as np
import cv2 as cv
import os

cap = cv.VideoCapture(0)

if not cap.isOpened():
    print("camera not found")
    exit()

PATH = os.path.dirname(os.path.abspath(__file__))
print("current dir: ", PATH)

CLIENT_NAME = input("type name: ")
CLIENT_PATH = PATH + f"/{CLIENT_NAME}_images"

if not os.path.exists(CLIENT_PATH):
    os.mkdir(PATH + f"/{CLIENT_NAME}_images")
else:
    "USER ALREADY EXIST"


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
