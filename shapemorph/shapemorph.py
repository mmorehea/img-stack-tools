#Shapemorph by Hirsh Parikshak

"""

Description: Shapemorph for obtaining intermediate between two shapes 

Usage:
	$ python shapemorph.py firstShape.tiff secondShape.tiff .5 newShape.tiff

	-s .5 <- scaling factor for the shape, .5 indicates the shape 
			 halfway between the first and second shapes

"""

#from PIL import Image
# import code

import sys
import math
import numpy as np
import cv2
import matplotlib.pyplot as plt
import Image
from shapely.geometry import Polygon
from shapely.geometry import Point
from shapely.geometry import MultiPoint
import os

def minElucidianDistance(point, boundaries):
	x1,y1 = point[0]
	dist = {}
	for p2 in boundaries:
		x2,y2 = p2[0]
		dist[tuple(p2[0])] = math.sqrt((x2-x1)**2 + (y2-y1)**2)
	return [key for key,val in dist.iteritems() if val == min(dist.values())][0]

def checkContours(tiff_fileName, dest):
	im = cv2.imread(os.path.join(dest, tiff_fileName))
	check = np.max(im)
	if (check == 1):
		return True
	else:
		return False

def getContours(tiff_fileName, dest):
	im = cv2.imread(os.path.join(dest, tiff_fileName))
	imgray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
	ret,thresh = cv2.threshold(imgray,0,1,0)
	con, hierarchy = cv2.findContours(thresh, cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	return con[0]

def getCentroid(points):
	x = [p[0][0] for p in points]
	y = [p[0][1] for p in points]
	return (sum(x) / len(points), sum(y) / len(points))

def getDeltaXY(old, new):
	oldCenter = getCentroid(old)
	newCenter = getCentroid(new)
	delta_x = oldCenter[0]-newCenter[0]
	delta_y = oldCenter[1]-newCenter[1]
	return delta_x, delta_y

def superimpose(old, new):
	return new+[getDeltaXY(old,new)]

def getVector(p1, p2):
	'''
	Calculates vector between two points p1 and p2
	'''
	x1,y1 = p1
	x2,y2 = p2
	dist = [x2-x1, y2-y1]
	return dist

def scalePoint(originalPoint, vector, scaleFactor):
	'''
	Scale Factor should be between 0 and 1.0
	'''
	return [sum(point) for point in zip(originalPoint, map(lambda x: x*scaleFactor, vector))]

def translateToBetweenShapes(old, new, intermediate, scaleFactor):
	delta_x, delta_y = getDeltaXY(old, new)
	new_delta_x = delta_x * scaleFactor
	new_delta_y = delta_y * scaleFactor
	return intermediate - [new_delta_x, new_delta_y]

def getPixelDimensions(tiff_fileName, dest):
	im = Image.open(os.path.join(dest, tiff_fileName))
	#optional (just for visualization)
	#pixels = map(lambda x: x*2, im.size) 
	return im.size

def generateClosestPoints(oldShape, adjustedNewShape):
		closestPoints = {}
		for point in oldShape:
			closestPoints[tuple(point[0])] = minElucidianDistance(point, adjustedNewShape)
		return closestPoints

def generateVectors(closestPoints):
		pairVectors = {}
		for old_p,new_p in closestPoints.iteritems():
			#print '{0} -> {1}'.format(old_p, new_p)
			pairVectors[(old_p, new_p)] = getVector(old_p, new_p)
		return pairVectors

def createMorph(pairVectors, scaleFactor):
		intermediateMorph = []
		for pair, vector in pairVectors.iteritems():
			oldpoint = pair[0] #p2 = pair[1]
			intermediateMorph.append(scalePoint(oldpoint, vector, scaleFactor))
		return intermediateMorph

def createIntermediateImage(translated, intermediateShape, pixels):
		intermediate=()
		for x in translated.tolist()[0]:
			intermediate = intermediate + ((x[0],x[1]),)

		poly_unordered = MultiPoint(intermediate).convex_hull

		img_width, img_height = pixels

		intermediate_img = Image.new('1', (img_width, img_height))
		pixels = intermediate_img.load()
		white = 1 #(255,255,255)
		black = 0 #(0,0,0)

		for i in range(img_width):
			for j in range(img_height):
				point = Point(i,j)
				if poly_unordered.contains(point):
					pixels[i,j] = white #formerly grey
				else:
					pixels[i,j] = black

		for i in intermediate:
			pixels[i[0],i[1]] = white

		intermediate_img.save(intermediateShape)

def main(filename1, filename2, scale, newfile, dest):
	firstShape = filename1 #sys.argv[1]
	secondShape = filename2 #sys.argv[2]
	try:
		scaleFactor = scale #float(sys.argv[3])
	except ValueError:
		print 'Not a valid scale!!'

	intermediateShape = newfile #'Water.tiff'

	#read files in

	oldShape = getContours(firstShape, dest)
	newShape = getContours(secondShape, dest)

	#superimpose newShape on oldShape
	adjustedNewShape = superimpose(oldShape, newShape)

	#make a dictionary for old shape boundary points and their closest points on the new shape boundary
	closestPoints = generateClosestPoints(oldShape, adjustedNewShape)

	#get a vector for each pair of old->new points
	pairVectors = generateVectors(closestPoints)

	#create the morph
	intermediateMorph = createMorph(pairVectors, scaleFactor)

	#translate the morph between the two shapes with respect to the scaling factor
	intermediateMorph = np.array([intermediateMorph], dtype = np.int32)
	translatedIntermediateShape = translateToBetweenShapes(oldShape, newShape, intermediateMorph, scaleFactor)

	createIntermediateImage(translatedIntermediateShape, intermediateShape, getPixelDimensions(firstShape, dest))

if __name__ == "__main__":
	main(sys.argv[1], sys.argv[2], sys.argv[3], sys.argv[4], sys.argv[5])