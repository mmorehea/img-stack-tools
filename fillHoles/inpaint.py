import sys

from PIL import Image, ImageDraw
import os
import glob
import numpy as np
import cv2
from natsort import natsorted, ns 
import code
import math
from scipy.spatial.distance import cdist

if len(sys.argv) < 3:
	print 'inpaint.py -- a mask inpainter for EM images'
	print 'written by Michael Morehead'
	print 'May 2015'
	print 'WVU Center for Neuroscience'
	print 'usage: python inpaint.py EMimageDirectory maskDirectory'
	sys.exit()

imgDir = sys.argv[1]
maskDir = sys.argv[2]
#texture = Image.open('./nucleTexture.png')
imgGlob = natsorted(glob.glob(imgDir+'*'), alg=ns.IGNORECASE)
maskGlob = list(reversed(natsorted(glob.glob(maskDir+'*'))))
#text = np.asarray(texture)
#text = text.flatten()
#print len(text)
print len(imgGlob)
print len(maskGlob)
if not os.path.exists('temp'):
	os.makedirs('temp')

#takes in a texture coordinate list and an x-y coordinate, and returns the x-y coordinate in the texture coordinate list nearest to that coordinate
#AAAdef findTexture(textlist, x, y):
#	p = [(x,y)]
#	distlist = cdist(p,textlist)
#	mindist=min(distlist[0])
#	closeX,closeY = textlist[distlist[0].tolist().index(mindist)]
#	return closeX, closeY

2 different ways to find a point outside the mitochondria to replace the point in the mitochondrai

#def findTexture(textlist, x, y):
	#jump = 2
	#posXlen=0
	#posYlen=0
	#negXlen=0
	#negYlen=0
	#while (x,y) in textlist == false:
		#x += jump 
		#posXlen += 1
	#x -= posXlen * jump 
	#while (x,y) in textlist == false:
		#x -= jump 
		#negXlen += 1
	#x += negXlen*jump 
	#while (x,y) in textlist == false:
		#y += jump 
		#posYlen += 1
	#y -= posYlen * jump 
	#while (x,y) in textlist == false:
		#y -= jump 
		#negYlen += 1
	#y += negYlen * jump 
	
	#if min(posXlen, posYlen, negXlen, negYlen) == posXlen:
		#newX, newY = x + posXlen * jump, y
	#elif min(posXlen, posYlen, negXlen, negYlen) == negXlen:
		#newX, newY = x - negXlen * jump, y
	#elif min(posXlen, posYlen, negXlen, negYlen) == posYlen:
		#newX, newY = x, y + posYlen * jump 
	#elif min(posXlen, posYlen, negXlen, negYlen) == negYlen:
		#newX, newY = x, y - negYlen * jump
	
	#return newX, newY 

for ww, img in enumerate(imgGlob):
	
	img = Image.open(imgGlob[ww])
	imgA = np.asarray(img)
	imgA.setflags(write=True)
	
	im1 = Image.open(maskGlob[ww])
	im = cv2.imread(maskGlob[ww])
	imgray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,0,1,0)
	
	kernel = np.ones((5,5),np.uint8)
	bigDil = cv2.dilate(thresh,kernel,iterations = 4)
	littleDil = cv2.dilate(thresh,kernel,iterations = 2)
	texture = bigDil-littleDil
	
	#for each in mtexture
	#text = np.asarray(texture)
	#text = text.flatten()
	
	t = np.where(thresh == 1)
	v = np.where(texture == 1)
	d = zip(t[0],t[1])
	c = zip(v[0],v[1])
	#BBBcount = 0
	for each in d:
		#BBBcount =count+ 1
		x, y = each
		#print count
		#AAA,CCC
		imgA[x,y] = imgA[findTexture(c, x, y)]
		#BBBimgA[x,y] = imgA[c[count]]
		#BBBif count == len(c)-1:
			#BBBcount = 0
	img = Image.fromarray(imgA)
	#code.interact(local=locals())
	print 'Writing ' + str(ww+1) + ' of ' + str(len(imgGlob)) 
	img.save('./temp/'+str(ww+1)+'.tiff')		
	
	
	
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

