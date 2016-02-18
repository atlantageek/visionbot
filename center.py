# import the necessary packages
from subprocess import call
import time
import cv2
import serial
import struct
import pyfirmata

board = pyfirmata.Arduino('/dev/ttyUSB0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
turret = board.get_pin('d:5:s')
 



rotate(90)
time.sleep(1)

board.exit()
