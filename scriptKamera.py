from djitellopy import tello
import cv2

drone = tello.Tello()
drone.connect()
drone.streamon()

frame_read = drone.get_frame_read()

while True:
    img = frame_read.frame
    cv2.imshow("Drone Camera", img)

    if cv2.waitKey(1) & 0xFF == ord('q'):
        break