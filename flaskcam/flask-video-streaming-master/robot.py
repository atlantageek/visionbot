import io
from camera_pi import Camera
while True:
    frame = Camera().get_frame()
