from djitellopy import tello
import keyPressModule as kp
from time import sleep


kp.init()
drone = tello.Tello()
drone.connect()
print(drone.get_battery())

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

    if kp.getKey("q"): yv = drone.land()
    if kp.getKey("e"): yv = drone.takeoff() # tombol e dikeyboard adalah langkah awal setelah drone terkonek
    

    return [lr, fb, ud, yv]


#drone.takeoff()


while True:
    values = getKeyboardInput()
    drone.send_rc_control(values[0], values[1], values[2], values[3])
    sleep(0.05)