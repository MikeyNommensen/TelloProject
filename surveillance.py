from djitellopy import tello
import keyPressModule as kp
from time import sleep
import cv2
import time



kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())
global img

drone.streamon()

def getKeyboardInput():
    lr, fb, ud, yv = 0, 0, 0, 0
    speed = 50

    if kp.getKey("LEFT"): lr = -speed
    if kp.getKey("RIGHT"): lr = speed

    if kp.getKey("UP"): fb = speed
    if kp.getKey("DOWN"): fb = -speed

    if kp.getKey("w"): ud = speed
    if kp.getKey("s"): ud = -speed

    if kp.getKey("a"): yv = -speed
    if kp.getKey("d"): yv = speed

    #if kp.getKey("q"): yv = drone.land(); time.sleep(3)
    #if kp.getKey("e"): yv = drone.takeoff() # tombol e dikeyboard adalah langkah awal setelah drone terkonek

    if kp.getKey("q"):
        drone.land()
        time.sleep(3)
    
    if kp.getKey("e"):
        drone.takeoff()

    if kp.getKey('z'):
        cv2.imwrite(f'Resources/Images/{time.time()}.jpg', img)
        time.sleep(0.3)

    

    return [lr, fb, ud, yv]
# masih bgr
# harus rgb



#drone.takeoff()


frame_read = drone.get_frame_read()

while True:
    values = getKeyboardInput()
    drone.send_rc_control(values[0], values[1], values[2], values[3])

    img = frame_read.frame
    img = cv2.resize(img, (360, 240))

    cv2.imshow("Image", img)

    key = cv2.waitKey(1) & 0xFF
    if key == 27:  # ESC
        drone.land()
        break

    sleep(0.05)