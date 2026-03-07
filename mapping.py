from djitellopy import tello
import keyPressModule as kp
import numpy as np
from time import sleep
import cv2
import math

# PARAMETERS 
forwardSpeed = 117/10   # Forward Speed (cm/s)    117/10       (15cm/s)
angularSpeed = 360/10   # Angular speed (Degrees/s)   360/10   (50d/s)
interval = 0.25

distanceInterval = forwardSpeed*interval
angularInterval = angularSpeed*interval

x, y = 500, 500
a = 0  #angle
yaw = 0

isFlying = False



kp.init()
drone = tello.Tello()
drone.connect()
sleep(3)
print(drone.get_battery())
points = [(0, 0), (0, 0)]


def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 15
    angularSpeed = 50
    global x, y, yaw, a
    d = 0 # distance

    if kp.getKey("LEFT"): 
        lr = -speed
        d = distanceInterval
        a = -180
    if kp.getKey("RIGHT"): 
        lr = speed
        d = -distanceInterval
        a = 180

    if kp.getKey("UP"): 
        fb = speed
        d = distanceInterval
        a = 270
    if kp.getKey("DOWN"): 
        fb = -speed
        d = -distanceInterval
        a = -90

    if kp.getKey("w"): 
        ud = speed

    if kp.getKey("s"): 
        ud = -speed

    if kp.getKey("a"): 
        yv = -angularSpeed
        yaw -= angularInterval

    if kp.getKey("d"): 
        yv = angularSpeed
        yaw += angularInterval

    global isFlying

    if kp.getKey("e") and not isFlying: 
        drone.takeoff()
        isFlying = True
    if kp.getKey("q") and isFlying:
        drone.land() # tombol e dikeyboard adalah langkah awal setelah drone terkonek
        isFlying = False

    sleep(interval)
    a += yaw
    x += int(d*math.cos(math.radians(a)))
    y += int(d*math.sin(math.radians(a)))
    

    return [lr, fb, ud, yv, x, y]

def drawPoints(img, points):
    for point in points:
        cv2.circle(img, point, 5, (0, 0, 255), cv2.FILLED)
    cv2.circle(img, points[-1], 8, (0, 255, 0), cv2.FILLED)
    cv2.putText(img, f'({(points[-1][0]- 500) / 100}, {(points[-1][1]-500) / 100})m', 
                (points[-1][0] + 10, points[-1][1] + 30), cv2.FONT_HERSHEY_PLAIN, 1,
                (255, 0, 255), 1)


while True:
    values = getKeyboardInput()
    drone.send_rc_control(values[0], values[1], values[2], values[3])
    
    img = np.zeros((1000, 1000, 3), np.uint8)
    if (points[-1][0] != values[4] or points[-1][1] != values[5]):
        points.append((values[4], values[5]))
    drawPoints(img, points)
    cv2.imshow("Output", img)

    cv2.waitKey(1)
