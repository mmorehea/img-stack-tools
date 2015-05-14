import glob
from PIL import Image, ImageDraw
import os
import sys
import subprocess
import numpy as np
import math
import cv2

class Model:
	def __init__(self, name):
		self.name = name
		self.cont = []
		self.allCont = []
		self.contourDict = None
	def __getitem__(self,b):
		return self.allCont[b]
	def __len__(self):
		return len(self.cont)
	def addContour(self, contour):
		self.cont.append(contour)
	def collectCont(self):
		self.allCont.append(self.cont)
		self.cont = []
	def finishCont(self):
		self.allCont.append(self.cont)
		self.cont = []
		print self.name + ' ' + str(len(self.allCont))
		


def main(path):
	l = path
	try:
		os.mkdir('temp')
	except:
		print 'Making dir'	
	ss = 'imodinfo -a -f '+ l +'.txt ' + l
	#subprocess.call(ss, shell=True)
	
	
	models = []
	names = []
	modelCount = 0
	objectTrigger = 0
	contourTrigger = 0
	with open(l+'.txt') as f:
		for lines in f:
			jj = lines.strip()
			jj = jj.split(' ')
			#print jj
			if jj[0] == 'object':
				objectTrigger = 1
				contourTrigger = 0
				continue
			if jj[0] == 'mesh':
				c.collectCont()
				objectTrigger = 0
				contourTrigger = 0
				continue
			if objectTrigger == 1:
				if jj[0] == 'name':
					try:
						c.finishCont()
					except:
						print 'building models'	
					c = Model(str(modelCount) + '. ' +  '_'.join(jj[1:]))
					modelCount += 1
					models.append(c)
					names.append(jj[1])
					continue
				if jj[0] == 'contour' and contourTrigger == 0:
					contourTrigger = 1
					continue
				if jj[0] == 'contour' and contourTrigger == 1:
					
					c.collectCont()
					
					continue
				
					
				if contourTrigger == 1:				
					#print jj
					try:
						numStr = [int(math.floor(float(i))) for i in jj]
					except:
						print jj
					
					
					c.addContour(numStr)
					continue
	c.finishCont()
	thingsToPaint = raw_input('Which items would you like to paint? (seperated by space) \n')
	thingsToPaint = thingsToPaint.split(' ')
	#thingsToPaint = ['0', '1', '2']
	superContours = []
	for each in thingsToPaint:
		superContours = superContours + models[int(each)].allCont
	maxP = [0] * 3
	minP = [sys.maxint] * 3
	for each in superContours:
		for ndx, sample in enumerate(each):
			x, y, z = each[ndx]
			if x > maxP[0]:
				maxP[0] = x
			if x < minP[0]:
				minP[0] = x
			if y > maxP[1]:
				maxP[1] = y
			if y < minP[1]:
				minP[1] = y
			if z > maxP[2]:
				maxP[2] = z
			if z < minP[2]:
				minP[2] = z
	
		
	
	
	print 'X dimensions: ' + str(minP[0]) + ', '+ str(maxP[0])
	print 'Y dimensions: ' + str(minP[1]) + ', '+ str(maxP[1])
	print 'Z dimensions: ' + str(minP[2]) + ', '+ str(maxP[2])
	
	
	
	xTotal = maxP[0] - minP[0]
	yTotal = maxP[1] - minP[1]
	zSlices = []
	allPoints = []
	for ii,each in enumerate(superContours):
		if len(each) == 0:
			
			continue
		allPoints.append(each)	
		zSlices.append(each[0][2])
	
	#print len(superContours)
	#print len(allPoints)
	#print zSlices
	zSlices = np.asarray(zSlices)
	rrr = np.asarray(allPoints)
	bigStr = ''
	for ii in range(minP[2],maxP[2]):
		print 'Painting slice %s' %str(ii)
		f = np.where(zSlices == ii)
		if np.size(f) == 0:
			continue
		img = Image.new('L', (maxP[0], maxP[1]), 0)
		for each in np.nditer(f):
			just = np.asarray(rrr[each])
			xx = just[:,0]
			yy = just[:,1]
			c = zip(xx,yy)
			if len(c) < 2:
				continue
			ImageDraw.Draw(img).polygon(c, outline=255, fill=255)
		name = 'temp/img%s.tiff' %str(ii)
		bigStr += name + ' '
		img.save(name)
		#allZs = np.where(rrr[:,2] == ii)
		#print allZs[0]
		#if len(allZs[0]) == 0:
			#print 'HELLOOOOOOOOOOOOO'
			#continue
		#xx = rrr[allZs,0]
		#yy = rrr[allZs,1]
		##print xx[0]
		#c = zip(xx[0],yy[0])
		##print c
		#img = Image.new('L', (xLocalMax, yLocalMax), 0)
		#ImageDraw.Draw(img).polygon(c, outline=255, fill=255)
		#name = 'temp/%s.tiff' %str(ii)
		#img.save(name)
	ss = 'tiffcp '+ bigStr + ' '+  l+'.tif'
	subprocess.call(ss, shell=True)

	


if __name__ == "__main__":	
	path = sys.argv[1] 
	main(path)
	

		
	
      


				
				
				
				
			
		
