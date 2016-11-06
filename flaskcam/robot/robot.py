from time import sleep
from picamera import PiCamera

camera = PiCamera()
camera.resolution = (1024, 768)
camera.start_preview()
# Camera warm-up time
while True:
	camera.capture('/tmp/foo.jpg')
	sleep(1)
