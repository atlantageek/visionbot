import numpy as np
import cv2
import glob

criteria = (cv2.TERM_CRITERIA_EPS + cv2.TERM_CRITERIA_MAX_ITER, 30, 0.001)
img = cv2.imread("workspace/checkerboard135.jpg")
gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
found, corners = cv2.findChessboardCorners(gray, (8,7),None)
# If found, add object points, image points (after refining them)

	# Draw and display the corners
cv2.drawChessboardCorners(img, (8,7), corners,found)

print(len(corners))
if (found):
   cv2.cornerSubPix(gray,corners,(11,11),(-1,-1),criteria)

   q = np.zeros((4,2), dtype=np.float32)
   q[0] = corners[0][0]
   q[1] = corners[7][0]
   q[2] = corners[55][0]
   q[3] = corners[48][0]
   dst = np.zeros((4,2), dtype=np.float32)
   dst[0] = (200,100)
   dst[1] = (200,200)
   dst[2] = (100,200)
   dst[3] = (100,100)
   imgagain = cv2.imread("workspace/checkerboard135.jpg")
   print(corners[0][0])
   imagain = cv2.circle(imgagain, (corners[7][0][0],corners[7][0][1]), 10,(100,0,0), -1)
   imagain = cv2.circle(imgagain, (corners[48][0][0],corners[48][0][1]), 10,(100,0,0), -1)
   imagain = cv2.circle(imgagain, (corners[55][0][0],corners[55][0][1]), 10,(100,0,0), -1)
   cv2.imwrite('workspace/imgx.jpg',imgagain)

   retvalHomography, mask = cv2.findHomography(q, dst, cv2.RANSAC)
   print(retvalHomography)
   result = cv2.warpPerspective(imgagain, retvalHomography, (400, 500))
   cv2.imwrite("workspace/img.jpg", result)
   cv2.waitKey(0)

