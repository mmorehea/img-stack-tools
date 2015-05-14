import os
import sys
import subprocess
import shutil
import glob

inp = sys.argv[1]
batchmode = 0
if os.path.isdir(inp):
	print 'Directory is detected, switching into batch mode'
	batchmode = 1

if batchmode:
	ll = glob.glob('*.nrrd')
	for each in ll:
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
			
		sti = 'convert ./tempTIFF/*.png ' + inp[:-4] + 'tiff'
		subprocess.call(sti, shell=True)
		print 'TIFF built, cleaning up!'
		shutil.rmtree('tempTIFF')

else:

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
		
	sti = 'convert ./tempTIFF/*.png ' + inp[:-4] + 'tiff'
	subprocess.call(sti, shell=True)
	print 'TIFF built, cleaning up!'
	shutil.rmtree('tempTIFF')

