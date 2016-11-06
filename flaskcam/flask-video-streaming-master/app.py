#!/usr/bin/env python

from PIL import Image
from flask import Flask, render_template, Response

#install redis
import redis

r=redis.StrictRedis(host='localhost', port=6379, db=0)

# emulated camera
from camera_pi import Camera

# Raspberry Pi camera module (requires picamera package)
# from camera_pi import Camera

global finding_ball 

r.set('finding_ball', False)

app = Flask(__name__, static_url_path='')



@app.route('/')
def index():
    """Video streaming home page."""
    return render_template('index.html')

@app.route('/capture')
def capture(data):
    camera.set_range(data)
    return "OK"

    

@app.route('/find_ball') 
def find_ball():
    r.set('finding_ball', True)
    finding_ball = True
    return "OK"



@app.route('/no_ball') 
def no_ball():
    r.set('finding_ball', False)
    finding_ball = False
    return "OK"


def gen(camera):
    """Video streaming generator function."""
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n')


@app.route('/video_feed')
def video_feed():
    """Video streaming route. Put this in the src attribute of an img tag."""
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')


if __name__ == '__main__':
    app.run(host='0.0.0.0', debug=True, threaded=True)
