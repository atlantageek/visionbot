# import the necessary packages
from picamera.array import PiRGBArray
from picamera import PiCamera
from subprocess import call
import time
import cv2
import serial
import struct
import pyfirmata

board = pyfirmata.Arduino('/dev/ttyACM0')
iter8 = pyfirmata.util.Iterator(board)
iter8.start()
turret = board.get_pin('d:5:s')
camera = PiCamera()
rawCapture = PiRGBArray(camera)

def rotate(angle):
  turret.write(angle)

def capture_image(filename):
  time.sleep(0.1)
  rawCapture.truncate(0)
  camera.capture(rawCapture, format="bgr")
  image = rawCapture.array
  cv2.imwrite(filename, image)

# initialize the camera and grab a reference to the raw camera capture
 
# allow the camera to warmup
 

rotate(50)
time.sleep(1)
capture_image("workspace/r45.jpg")


rotate(90)
time.sleep(1)
capture_image("workspace/r90.jpg")

rotate(130)
time.sleep(1)
capture_image("workspace/r135.jpg")



camera.close()
rotate(90)
call(["./build_panorama"])
board.exit()
