import glob
from PIL import Image
import os
import sys
import subprocess
import numpy as np

def main():
	l = 'VCN_c18_dendrite.vtk'
	polygons = []
	pointsTrigger = 0
	polygonTrigger = 0
	with open(l) as f:
		for lines in f:
			jj = lines.strip()
			jj = jj.split(' ')
			#print jj
			if jj[0] == 'POINTS':
				pointsTrigger = 1
				points = []
				continue
			if jj[0] == 'POLYGONS':
				pointsTrigger = 0
				polygonTrigger = 1
				
				
				continue
			
			if pointsTrigger == 1:
				if len(jj) == 1:
					continue		
				#print jj
				try:
					numStr = jj
				except:
					print jj
				
				points.append(numStr)
				continue
					
			if polygonTrigger == 1:
				
				try:
					numStr = [str(int(i) + 1) for i in jj[1:]]
					polygons.append(numStr)
				except:
					continue
				
				
	print len(points[-1])
	f = open('out.obj', 'w')
	for each in points:
		if len(each) == 0:
			continue
		f.write('v ' + ' '.join(each)  +'\n')
	f.write('\n')
	f.write('g mesh \n')
	
	for each in polygons:
		f.write('f ' + ' '.join(each) + '\n')
	f.write('g')
	f.close
	#ss = 'meshlabserver -i out.obj -o ' + l[:-4] +'.obj -s ' + 'smoothAndReduce.mlx'
	#subprocess.call(ss, shell= True)	
	
	

	


if __name__ == "__main__":	
	#path = sys.argv[1] 
	main()


				
