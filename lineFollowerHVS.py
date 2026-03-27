"""
Pastikan posisi Drone harus selalu berada di tengah-tengah garis
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
#hsvVals = [0, 0, 117, 179, 22, 219] Nilai HSV dari Website cvzone
hsvVals = [0, 0, 100, 179, 255, 255]


# Find a PATH
def thressholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)   
    return mask

while True:
    _, img = cap.read()
    img = cv2.resize(img, (480, 360))
    #img = cv2.flip(img, 0)

    imgThes = thressholding(img)

    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThes)
    cv2.waitKey(1)