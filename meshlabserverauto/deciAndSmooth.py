import glob # can get list of files in directory
import subprocess # can call terminal commands
import sys
import math
import os

MESHLAB_SCRIPT = 'deciAndSmooth.mlx' # Name of original meshlab script
TEMP_SCRIPT = 'newScript.mlx' # Name of temporary meshlab script file to write
MIN_FACES = 500 # Minimum number of faces needed to run the script
MIN_DECIMATION = 0.05 # Minimum value of 'TargetPerc' parameter for decimation (for very large number of faces)
DECIMATION_SCALE = 1000 # Higher values of this will result in meshes being less decimated when they have few faces

def calc_decimation(numFaces):
	return math.exp((MIN_FACES - numFaces) / DECIMATION_SCALE) + MIN_DECIMATION

if len(sys.argv) <= 2:
	print 'Include the base directory and output directory when calling this script.'
	print 'For example: python deciAndSmooth.py testinput/ testoutput/'
	sys.exit()

baseDir = sys.argv[1]
outputDir = sys.argv[2]
if not baseDir.endswith('/'):
	baseDir += '/'
if not outputDir.endswith('/'):
	outputDir += '/'
   
f = []
for (paths, dirs, files) in os.walk(baseDir):
    for x in files:
        if x.endswith(".obj"):
            f.append(os.path.join(paths, x))

    
files = f#glob.glob(baseDir + '*.obj')
command = 'meshlabserver -s ' + TEMP_SCRIPT + ' -i %s -o ' + outputDir + '%s'

with open(MESHLAB_SCRIPT) as script:
	scriptText = script.read().replace('<Param type="RichFloat" value=".2" name="TargetPerc"/>', '<Param type="RichFloat" value="%f" name="TargetPerc"/>')	
	
for fileName in files:
	numFaces = 0
	with open(fileName) as obj:
		line = obj.readline()
		for line in obj:
			# print line
			if line.startswith('f '):
				numFaces += 1
				
	decimationValue = calc_decimation(numFaces)
	print 'File: ' + fileName + ', num faces: ' + str(numFaces) + ', TargetPerc: ' + str(decimationValue)
	shortFileName = fileName.replace(baseDir, '', 1)
	if numFaces > 100:
		with open(TEMP_SCRIPT, 'w+') as scriptOutput:
			scriptOutput.write(scriptText % decimationValue)
			
		newCommand = command % (fileName, shortFileName)
		print newCommand
		subprocess.call(newCommand, shell=True)
	else:
		print 'Not running filters for file ' + fileName
