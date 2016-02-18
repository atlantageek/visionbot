import pyfirmata
from flask import Flask, render_template, Response
from camera_pi import Camera

board = pyfirmata.Arduino('/dev/ttyACM0')
turret = board.get_pin('d:5:s')
tilter = board.get_pin('d:6:s')
left = board.get_pin('d:11:s')
right = board.get_pin('d:10:s')
turret.write(int(90))
tilter.write(int(20))
steerval = 0
left.write(90  )
right.write(90 )

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    while True:
        frame = camera.get_frame()
        yield(b'--frame\r\n'
              b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    return Response(gen(Camera()),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

@app.route('/rotate/<angle>')
def rotate(angle):
    print(angle)
    turret.write(int(angle))
    return ""

@app.route('/tilt/<angle>')
def tilt(angle):
    print("TILTER", angle)
    tilter.write(int(angle))
    return ""

@app.route('/steer/<angle>')
def steer(angle):
    steerval=int(angle)
    print("Steer", steerval)
    left.write(90 - steerval )
    right.write(90 + steerval )
    return ""

@app.route('/turnleft')
def turnleft():
    print("left",steerval )
    left.write(90  )
    right.write(60 )
    return ""

@app.route('/straight')
def straight():
    left.write(120  )
    right.write(60 )
    print("straight",steerval )
    return ""

@app.route('/turnright')
def turnright():
    print("right",steerval )
    left.write(120  )
    right.write(90 )
    return ""


@app.route('/stop')
def stop():
    left.write(90  )
    right.write(90 )
    print("Stop")
    return ""

@app.route("/hello")
def hello():
    return "Hello World!"

if __name__ == "__main__":
    app.run(host='0.0.0.0', debug=True, threaded=True)
