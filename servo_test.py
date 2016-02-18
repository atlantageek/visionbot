# import the necessary packages
import time
import pyfirmata

board = pyfirmata.Arduino('/dev/ttyACM0')
turret = board.get_pin('d:5:s')
left = board.get_pin('d:11:s')
right = board.get_pin('d:10:s')

right.write(90)
left.write(60)
time.sleep(3)
left.write(90)
time.sleep(3)
right.write(120)
time.sleep(3)
right.write(90)
time.sleep(3)


