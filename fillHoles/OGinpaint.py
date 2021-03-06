import sys

from PIL import Image, ImageDraw
import os
import glob
import numpy as np
import cv2
from natsort import natsorted, ns 
import code


if len(sys.argv) < 3:
	print 'inpaint.py -- a mask inpainter for EM images'
	print 'written by Michael Morehead'
	print 'May 2015'
	print 'WVU Center for Neuroscience'
	print 'usage: python inpaint.py EMimageDirectory maskDirectory'
	sys.exit()

imgDir = sys.argv[1]
maskDir = sys.argv[2]
texture = Image.open('./nucleTexture.png')
imgGlob = natsorted(glob.glob(imgDir+'*'), alg=ns.IGNORECASE)
maskGlob = list(reversed(natsorted(glob.glob(maskDir+'*'))))
text = np.asarray(texture)
text = text.flatten()
print len(text)
print len(imgGlob)
print len(maskGlob)
if not os.path.exists('temp'):
	os.makedirs('temp')

for ww, img in enumerate(imgGlob):
	img = Image.open(imgGlob[ww])
	imgA = np.asarray(img)
	imgA.setflags(write=True)
	im1 = Image.open(maskGlob[ww])
	im = cv2.imread(maskGlob[ww])
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,0,1,0)
	
	t = np.where(thresh == 1)
	d = zip(t[0],t[1])
	count = 0
	#code.interact(local=locals())
	for each in d:
		count =count+ 1
		x, y = each
		#print count
		imgA[x,y] = text[count]
		if count == len(text)-1:
			count = 0
	img = Image.fromarray(imgA)
	print 'Writing ' + str(ww) + ' of ' + str(len(imgGlob)) 
	img.save('./temp/'+str(ww)+'.tiff')		
	
	
	
	#imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	#ret,thresh = cv2.threshold(imgray,0,1,0)
	#contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)


	#for xx,jj in enumerate(contours):
		##print xx
		#this = contours[xx][0][0]
		##print this
		#if len(contours[xx]) < 2:
			#continue
		#xs = [contours[xx][y][0][0] for y in range(0,len(contours[xx]))]

		#ys = [contours[xx][y][0][1] for y in range(0,len(contours[xx]))]
		##print xs
		##print ys
		#c = zip(xs,ys)
		##print c

		#ImageDraw.Draw(im1).polygon(c, outline=255, fill=255)
		
	##im1.show()	
	#kernel = np.ones((5,5),np.uint8)
	#dilation = cv2.dilate(np.asarray(im1),kernel,iterations = 1)

	##cv2.imshow('image',dilation)
	##cv2.waitKey()

	##imgray = cv2.cvtColor(dilation,cv2.COLOR_BGR2GRAY)
	#ret,thresh = cv2.threshold(dilation,0,1,0)
	#contours, hierarchy = cv2.findContours(thresh,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	#for xx,jj in enumerate(contours):
		##print xx
		#this = contours[xx][0][0]
		##print this
		#if len(contours[xx]) < 2:
			#continue
		#xs = [contours[xx][y][0][0] for y in range(0,len(contours[xx]))]

		#ys = [contours[xx][y][0][1] for y in range(0,len(contours[xx]))]
		##print xs
		##print ys
		#c = zip(xs,ys)
		
		##print c
		#gg = np.asarray(img)
		#imgX, imgY = gg.shape
		##print imgX, imgY
		#s = 0
		

		#for tt in c:
			#x,y = tt
			##print x, y
			#if x >= imgX or y >= imgY:
				#continue
			
			#s += gg[tt]
			
		#s = s/len(c)
		#ImageDraw.Draw(img).polygon(c, outline=s, fill=s)
	#img.show()	
	#print 'Writing ' + str(ww) + ' of ' + str(len(imgGlob)) 
	#img.save('./temp/'+str(ww)+'.tiff')

