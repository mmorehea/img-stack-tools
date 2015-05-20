import sys
import xml.etree.ElementTree as ET
from pprint import pprint
import numpy as np
from skimage.io._plugins import freeimage_plugin as fi

from PIL import Image
import code


bigDict = {}

e = ET.parse('annotation.xml').getroot()
l = []
for elem in e.iter():
	if elem.tag == 'node':
		l.append(elem.attrib)

Zs = []
Ys = []
Xs = []
for each in l:
	tempX=int(each.get('x'))
	tempY=int(each.get('y'))
	tempZ=int(each.get('z'))
	Zs.append(tempZ)
	Xs.append(tempX)
	Ys.append(tempY)
	if bigDict.get(str(tempZ)) == None:
		bigDict[str(tempZ)] = [(tempX, tempY)]
	else:
		li = bigDict.get(str(tempZ)) 
		li.append((tempX, tempY))
		

minZ = min(Zs)
maxZ = max(Zs)
minX = min(Xs)
minY = min(Ys)
maxX = max(Xs)
maxY = max(Ys)
diffX = maxX - minX
diffY = maxY - minY
diffZ = maxZ - minZ




for ii in range(int(minZ), int(maxZ)):
	image = np.zeros((diffX, diffY), 'uint8')
	if bigDict.get(str(ii)) != None:
		li = bigDict.get(str(ii))
		for each in li:
			x,y = each
			image[x-minX-1,y-minY-1] = 255
			
			 
	image = Image.fromarray(image)
	image.save(str(ii)+'.tiff', "TIFF")
print 'Z-offset: ' + str(minZ)
print 'X-offset: ' + str(minX)	
print 'Y-offset: ' + str(minY)
	
	
		
  
#fi.write_multipage(image, 'multipage.tif')
