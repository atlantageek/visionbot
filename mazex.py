# import the necessary packages
import numpy as np
import cv2
from skimage import morphology
from skimage import img_as_ubyte
import matplotlib.pyplot as plt

todopoints=[]

def proc_neighbors(point):
    print "Neighbor for point {0} {1}".format(point[0],point[1])
    curr_val = path[point[0],point[1]] + 1
    for a in range(-1,2):
        for b in range(-1,2):
            x = point[0] + a
            y = point[1] + b

            if thinmaze[x,y] == True:
                if path[x,y] > curr_val:
                    print "point {0} {1} {2}".format(x,y, curr_val)
                    path[x,y] = curr_val
                    todopoints.append((x,y))

def smallest_neighbor(point):
    curr_val = path[point[0],point[1]] 
    for a in range(-1,2):
        for b in range(-1,2):
            x = point[0] + a
            y = point[1] + b
            if path[x,y] < curr_val:
                return(x,y)
    return (-1,-1)

points = []
# load the games image
cv2.namedWindow('image')
im = cv2.imread("workspace/maze.jpg")
#cv2.imshow("im", im)
imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
imgray = cv2.medianBlur(imgray,5)
ret,thresh = cv2.threshold(imgray,127,25,0)
thresh2 = cv2.adaptiveThreshold(imgray,255,cv2.ADAPTIVE_THRESH_GAUSSIAN_C,cv2.THRESH_BINARY,11,2)
#Find the contours
contours, hierarchy = cv2.findContours(thresh2, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
maxArclen = 0
maxcontour = contours[0]
#Find the longest contour
for contour in contours:
    arclen =cv2.arcLength(contour,False)
    if (arclen > maxArclen):
       maxArclen = arclen
       maxcontour = contour

cv2.drawContours(im, [maxcontour], 0, 255,-1)
#Store contour in its own image
height,width, channels = im.shape
thickmaze = np.zeros((height,width,3), np.uint8)
path = np.full((height,width),65535, np.uint16);
route = np.full((height,width),0, np.uint8);
cv2.drawContours(thickmaze, [maxcontour], 0, 255,-1)
#Skeletonize
thickmaze = cv2.bitwise_not(thickmaze)
thickmaze = cv2.cvtColor(thickmaze, cv2.COLOR_BGR2GRAY)
thickmaze = cv2.threshold(thickmaze,0,255,cv2.THRESH_OTSU)[1]
thinmaze = morphology.skeletonize(thickmaze == 0)
dst = (69,148)
start = (379,279)
todopoints.append(start)
path[379,279] = 0
while(len(todopoints) > 0):
    print  len(todopoints)
    currpoint = todopoints.pop()
    proc_neighbors(currpoint)

x,y = smallest_neighbor(dst)
print "---------------------------------------------"
print "route point {0} {1}".format(x,y)
while (x != -1):
    route[x,y]=200
    print "route point {0} {1}".format(x,y)

    x,y = smallest_neighbor((x,y))
ret,routex = cv2.threshold(route,128,255,cv2.THRESH_BINARY)
cv2.imshow("image", img_as_ubyte(routex))
cv2.imshow("image2", img_as_ubyte(thinmaze))
#cv2.imwrite("dst.png", img_as_ubyte(thinmaze))
cv2.waitKey(0)
