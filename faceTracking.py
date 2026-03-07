import cv2
import numpy as np
from djitellopy import Tello
import time

# Koneksikan Drone
drone = Tello()
drone.connect()

print("Battery:", drone.get_battery())

drone.streamon()
time.sleep(2)

frame_read = drone.get_frame_read()

# Setting Kamera Tello
w = 360
h = 240

# Face Detection
faceCascade = cv2.CascadeClassifier(
    "kamera/haarcascade_frontalface_default.xml"
)

# Parameter untuk kontrol 5000 dan 8000
fbRange = [6200, 6800]
pid = [0.7, 0.4, 0]
pError = 0

flying = False


# Cari face
def findFace(img):
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, 1.3, 5)

    center = [0, 0]
    area = 0

    for (x, y, w1, h1) in faces:
        cx = x + w1 // 2
        cy = y + h1 // 2

        area = w1 * h1

        center = [cx, cy]

        cv2.rectangle(img, (x, y), (x + w1, y + h1), (0, 0, 255), 2)

        cv2.circle(img, (cx, cy), 5, (0, 255, 0), cv2.FILLED)
    
    return img, center, area


# Track Muka
def trackFace(center, area, w, pid, pError):
    x, y = center
    fb = 0
    error = x - w // 2
    speed = pid[0] * error + pid[1] * (error - pError)
    speed = int(np.clip(speed, -60, 60))

    if area > fbRange[1]:
        fb = -20

    elif area < fbRange[0] and area != 0:
        fb = 20
    
    else:
        fb = 0

    if x == 0:
        drone.send_rc_control(0, 0, 0, 0)
        return 0
    
    drone.send_rc_control(0, fb, 0, speed)

    return error


# Main LooP

while True:

    frame = frame_read.frame

    if frame is None:
        continue

    img = frame.copy()  # fungsi ini dipakai karena sesaat tombol key diklik, kamera drone masih berada di kondisi yg sama saat di lantai
    
    img = cv2.resize(img, (w, h))

    img, center, area = findFace(img)

    if flying:
        pError = trackFace(center, area, w, pid, pError)
    
    cv2.imshow("Tello Face Tracking", img)

    key = cv2.waitKey(1) & 0xFF
    print(key)

    if key == ord('e'):
        drone.takeoff()
        time.sleep(2)
        #drone.move_up(80)
        flying = True
    
    if key == ord('q'):
        drone.land()
        break

    time.sleep(0.03)

cv2.destroyAllWindows()
