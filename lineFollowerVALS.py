"""
Pastikan posisi Drone harus selalu berada di tengah-tengah garis
"""

import cv2
import numpy as np

cap = cv2.VideoCapture(0)
hsvVals = [0, 0, 100, 179, 255, 255]
sensors = 3
threshold = 0.2


# Find a PATH
def thressholding(img):
    hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
    lower = np.array([hsvVals[0], hsvVals[1], hsvVals[2]])
    upper = np.array([hsvVals[3], hsvVals[4], hsvVals[5]])
    mask = cv2.inRange(hsv, lower, upper)   
    return mask



def getContours(imgThres, img):
    contours, hieracrhy = cv2.findContours(imgThres, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)
    biggest = max(contours, key = cv2.contourArea)
    x, y, w, h = cv2.boundingRect(biggest)
    cx = x + w // 2
    cy = y + h // 2
    cv2.drawContours(img, biggest, -1, (255, 0, 255), 7)
    cv2.circle(img, (cx, cy), 10, (0, 255, 0), cv2.FILLED)

    return cx

def getSensorOutput(imgThres, sensors):
    imgs = np.hsplit(imgThres, sensors)
    totalPixels = img.shape[1] // sensors * img.shape[0]
    senOut = []
    for x, im in enumerate(imgs):
        pixelCount = cv2.countNonZero(im)
        if pixelCount > threshold * totalPixels:
            senOut.append(1)
        else:
            senOut.append(0)
        cv2.imshow(str(x), im)
    
    print(senOut)
    return senOut

while True:
    _, img = cap.read()
    img = cv2.resize(img, (480, 360))
    #img = cv2.flip(img, 0)

    imgThres = thressholding(img)
    cx = getContours(imgThres, img)  # Translation
    senOut = getSensorOutput(imgThres, sensors)

    getSensorOutput(imgThres, sensors)

    cv2.imshow("Output", img)
    cv2.imshow("Path", imgThres)
    cv2.waitKey(1)