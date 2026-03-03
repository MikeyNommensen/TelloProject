from djitellopy import tello
from time import sleep

me = tello.Tello()
me.connect()
print(me.get_battery())

me.takeoff()
me.send_rc_control(0, 20, 0, 0)
sleep(2)
# me.send_rc_control(0, -20, 0, 0)
# sleep(5)
me.send_rc_control(0, 0, 0, 30)
sleep(2)
me.land()


# # baterai = me.get_battery()
# # baterai_msg = f"Baterai tersisa {baterai}"

# from djitellopy import tello
# import time

# me = tello.Tello()
# me.connect()
# print(me.get_battery())

# me.takeoff()
# time.sleep(5) # kalibrasi imu dulu sebelum masuk ke program inti


# me.move_left(50)
# time.sleep(3)
# me.rotate_counter_clockwise(90)
# time.sleep(3)
# me.move_forward(50)
# time.sleep(3)
# me.land()

