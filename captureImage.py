from djitellopy import tello
import cv2
import time

drone = tello.Tello()
drone.connect()
print("Battery:", drone.get_battery())

drone.streamon()

#takeoff
drone.takeoff()
time.sleep(3)

frame_read = drone.get_frame_read()

while True:
    img = frame_read.frame
    cv2.imshow("Tello Camera", img)

    key = cv2.waitKey(1) & 0xFF
    if key == ord('q') or key == ord('Q'):
        break

drone.land()
cv2.destroyAllWindows()
drone.streamoff

# from djitellopy import tello
# import cv2

# drone = tello.Tello()
# drone.connect()
# print(drone.get_battery())

# drone.stream_on()
# while True:
#     img = drone.get_frame_read().frame
#     #img = cv2.resize(img, (360, 240))
#     cv2.imshow("Image", img)
#     cv2.waitKey(1)