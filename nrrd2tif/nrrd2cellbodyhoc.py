import os
import sys
import re
import glob
from math import floor
from skimage import io, color, measure, draw
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt
print len(sys.argv)

def atoi(text):
    return int(text) if text.isdigit() else text

def natural_keys(text):
    '''
    alist.sort(key=natural_keys) sorts in human order
    http://nedbatchelder.com/blog/200712/human_sorting.html
    (See Toothy's implementation in the comments)
    '''
    return [ atoi(c) for c in re.split('(\d+)', text) ]

if len(sys.argv) < 6:
	print 'tiffs2cellbodyhoc builder!'
	print 'usage: python tiffs2cellbodyhoc [directory to tiffs] [x-dimension offset] [y-dimension offset] [z-dimension offset] [z-stack size] [number of cylinders]'
else:
	in1 = sys.argv[1]
	in2 = sys.argv[2]
	in3 = sys.argv[3]
	in4 = sys.argv[4]
	in5 = sys.argv[5]
	in6 = sys.argv[6]
	

	la = sorted(glob.glob(in1+'*.tiff'), key=natural_keys)

	ll = sorted(glob.glob(in1+'*.tif'), key=natural_keys)
	if len(la) > len(ll):
		ll = la
		
		
	print len(ll)
	f = open('testHOC.hoc','w')
	f. write('proc celldef() { \n')
	f.write('  topol() \n }\n')
	f.write('create soma[1] \n')
	f.write('proc topol() {\n }\n')
	f.write('soma[0] { \n')
	sizeList = len(ll)
	choices = np.linspace(40, sizeList-40, in6)
	print choices
	print ll
	for x in choices:
		zDepth = ll.index(ll[int(floor(x))])
		image = io.imread(ll[int(floor(x))])
		print ll[int(floor(x))]
		print zDepth
		print np.amax(image)
		regions = measure.regionprops(image)
		#print regions
		bubble = regions[0]

		y0, x0 = bubble.centroid
		r = bubble.major_axis_length / 2.

		def cost(params):
			x0, y0, r = params
			coords = draw.circle(y0, x0, r, shape=image.shape)
			template = np.zeros_like(image)
			template[coords] = 1
			return -np.sum(template == image)

		x0, y0, r = optimize.fmin(cost, (x0, y0, r))
		print r
		if r < 20:
			continue
		else:
		
			aa = float(in2)+x0
			bb = float(in3)+ y0
			cc = float(in4)+(zDepth)
			ss = 'pt3dadd('+str(aa)+', '+ str(bb) +', '+ str(cc) +', '+ str(r)+')\n'
			f.write(ss)



		#_, ax = plt.subplots()
		#circle = plt.Circle((x0, y0), r)
		#ax.imshow(image, cmap='gray', interpolation='nearest')
		#ax.add_artist(circle)
		#plt.show()
	f.write(' } \n celldef()')

