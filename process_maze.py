#!/usr/bin/python

import cv2
import numpy as np

def findLongest(contours):
	maxsize = 0
	count = 0
	best = 0
	for cnt in contours:
		if cv2.arcLength(cnt, False) > maxsize:
			maxsize = cv2.arcLength(cnt,False)
			best = count
			print(best)
		count = count + 1
	return best

def findLargest(contours):
	maxsize = 0
	count = 0
	best = 0
	for cnt in contours:
		if cv2.contourArea(cnt) > maxsize:
			maxsize = cv2.contourArea(cnt)
			best = count
			print(best)
		count = count + 1
	return best

imgray = cv2.imread("workspace/result.jpg", cv2.CV_LOAD_IMAGE_GRAYSCALE)
img = cv2.imread("workspace/result.jpg")
(thresh, im_bw) = cv2.threshold(imgray, 128, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)
mask = np.zeros(im_bw.shape, np.uint8)
mask2 = np.zeros(im_bw.shape, np.uint8)
contours, hierarchy = cv2.findContours(im_bw,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
cv2.imwrite("workspace/bw.jpg", imgray)

largest = findLargest(contours)
for pnt in list(largest):
	print pnt
cnt = contours[largest]
epsilon = 0.020 * cv2.arcLength(cnt, True)
approx = cv2.approxPolyDP(cnt, epsilon, True)
cv2.drawContours(img, contours, largest,(255,0,0),3)
cv2.drawContours(img, [approx], 0,(0,0,255),3)

cv2.imwrite("workspace/BANG.jpg", img)


#x,y,w,h = cv2.boundingRect(contours[largest])
#crop = imgray[y:y+h,x:x+w]
#contours, hierarchy = cv2.findContours(crop,cv2.RETR_LIST,cv2.CHAIN_APPROX_SIMPLE)
#longest = findLongest(contours)
#
#
#cv2.imwrite("workspace/BANG.jpg", orig)
