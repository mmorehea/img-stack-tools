import os
import sys
import subprocess
import shutil
import glob
from skimage import io, color, measure, draw, img_as_bool
import numpy as np
from scipy import optimize
import matplotlib.pyplot as plt


inp = sys.argv[1]
batchmode = 0
	
try:
	os.mkdir('tempTIFF')
except:
	pass
stnrrd = 'unu dice -a 2 -i ' + inp + ' -o ./tempTIFF/del'
subprocess.call(stnrrd, shell=True)
print 'Temp PNGs built, creating TIFF'

l = glob.glob('./tempTIFF/*')
number = len(l)
for xx,ii in enumerate(l):
	print 'converting ' + str(xx) + '/' + str(number-1)
	sttiff = 'unu quantize -i '+ ii +' -b 16 -o ' + ii[:-4] +'png'
	subprocess.call(sttiff, shell=True)
	

ll = glob.glob('./tempTIFF/*.png')

