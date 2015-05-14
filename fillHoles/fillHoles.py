import sys

from PIL import Image, ImageDraw

import glob
import numpy as np
import cv2
from natsort import natsorted, ns 

imgDir = sys.argv[1]
maskDir = sys.argv[2]

imgGlob = natsorted(glob.glob(imgDir+'*'), alg=ns.IGNORECASE)
maskGlob = list(reversed(natsorted(glob.glob(maskDir+'*'))))

print imgGlob
print maskGlob

for ww, img in enumerate(imgGlob):
	img = Image.open(imgGlob[ww])

	im1 = Image.open(maskGlob[ww])
	im = cv2.imread(maskGlob[ww])
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,0,1,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


	for xx,jj in enumerate(contours):
		#print xx
		this = contours[xx][0][0]
		#print this
		if len(contours[xx]) < 2:
			continue
		xs = [contours[xx][y][0][0] for y in range(0,len(contours[xx]))]

		ys = [contours[xx][y][0][1] for y in range(0,len(contours[xx]))]
		#print xs
		#print ys
		c = zip(xs,ys)
		#print c

		ImageDraw.Draw(im1).polygon(c, outline=255, fill=255)
		
	#im1.show()	
	kernel = np.ones((5,5),np.uint8)
	dilation = cv2.dilate(np.asarray(im1),kernel,iterations = 1)

	#cv2.imshow('image',dilation)
	#cv2.waitKey()

	#imgray = cv2.cvtColor(dilation,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(dilation,0,1,0)
	contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	for xx,jj in enumerate(contours):
		#print xx
		this = contours[xx][0][0]
		#print this
		if len(contours[xx]) < 2:
			continue
		xs = [contours[xx][y][0][0] for y in range(0,len(contours[xx]))]

		ys = [contours[xx][y][0][1] for y in range(0,len(contours[xx]))]
		#print xs
		#print ys
		c = zip(xs,ys)
		#print c
		gg = np.asarray(img)
		s = 0
		for tt in c:
			s += gg[tt]
			
		s = s/len(c)+100	
		ImageDraw.Draw(img).polygon(c, outline=s, fill=s)
	#img.show()	
	img.save(str(ww)+'.tiff')

