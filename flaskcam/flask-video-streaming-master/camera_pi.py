import time
import io
import threading
import picamera
import cv2
import numpy as np
import colorsys

from cStringIO import StringIO
from PIL import Image

redLower = (0,205,60)
redUpper = (20,255,100)


class Camera(object):
    thread = None  # background thread that reads frames from camera
    frame = None  # current frame is stored here by background thread
    mask = None
    last_access = 0  # time of last client access to the camera

    def initialize(self):
        if Camera.thread is None:
            # start background frame thread
            Camera.thread = threading.Thread(target=self._thread)
            Camera.thread.start()

            # wait until frames start to be available
            while self.frame is None:
                time.sleep(0)
        self.mask = np.ones((320,240)).astype(np.bool)

    def set_range(capture):
        print("SET RANGE")
        pts = np.array(capture)
        mask = np.zeros((320,240))
        #cv2.fillConvexPoly(mask, pts, 1)
        #self.mask = mask.astype(np.bool)
        self.mask=1
  

    def get_frame(self):
        Camera.last_access = time.time()
        self.initialize()
        return self.frame

    @classmethod
    def _thread(cls):
        with picamera.PiCamera() as camera:
            # camera setup
            camera.resolution = (320, 240)
            camera.hflip = False
            camera.vflip = False

            # let camera warm up
            camera.start_preview()
            time.sleep(2)
            if cls.mask is not None:
              print(cls.mask)

            stream = io.BytesIO()
            for foo in camera.capture_continuous(stream, 'jpeg', use_video_port=True):
                # store frame
                stream.seek(0)
                frame = stream.read()
                data = np.fromstring(frame,dtype=np.uint8)
                image = cv2.imdecode(data,cv2.IMREAD_COLOR)
                hsv = cv2.cvtColor(image, cv2.COLOR_BGR2HSV)
                #print(hsv[160][120])
	        mask = cv2.inRange(hsv, redLower, redUpper)
	        mask = cv2.erode(mask, None, iterations=2)
	        mask = cv2.dilate(mask, None, iterations=2)
                mask = cv2.bitwise_and(mask, mask, mask=cls.mask)
                cnts = cv2.findContours(mask.copy(), cv2.RETR_EXTERNAL,
                   cv2.CHAIN_APPROX_SIMPLE)[-2]
                center = None
                
                if len(cnts) > 0:
                   c = max(cnts, key=cv2.contourArea)
                   ((x,y), radius) = cv2.minEnclosingCircle(c)
                   M = cv2.moments(c)
                   center = (int(M["m10"] / M["m00"]), int(M["m01"] / M["m00"]))
                   if radius > 10:
                      cv2.circle(image, (int(x), int(y)), int(radius),(0,255,255),2)
                      cv2.circle(image, center, 5, (0,0,255), -1)
                ret, frame = cv2.imencode('.jpg', image) #image)
                cls.frame = frame.tostring()

                # reset stream for next frame
                stream.seek(0)
                stream.truncate()

                # if there hasn't been any clients asking for frames in
                # the last 10 seconds stop the thread
                if time.time() - cls.last_access > 10:
                    break
        cls.thread = None
