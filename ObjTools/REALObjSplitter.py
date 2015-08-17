#OBJ Point Extractor
#Written By Michael and Jake

import sys
import re
import os


inputDir = '/home/callie/Downloads/blah/'


vs = re.compile('v [\s\S]*')
fs = re.compile('f [\s\S]*')
gs = re.compile('g [\s\S]*')

nueronal = re.compile('.*neuronal.*')
nucleusRE = re.compile('.*nucleus.*')
cellBodyRE = re.compile('.*cell_body.*')
dendRE = re.compile('.*dend.*')
axonRE = re.compile('.*axon.*')
def data():
    totalCount = 0
    runningCount = 0
    openFile = None
    gFound = False
    logFile = open('log.txt', 'w+')
    nucleus = False
    cellBody = False
    dend = False
    axon = False
    for inputFile in os.listdir(inputDir):
        with open(inputDir+inputFile) as f:
    
        for line in f:
            if(gs.match(line)):
                if (openFile != None):
                    openFile.close()
                    
                gLine = line.split()
                output = gLine[1]
                
                #Match the type for the log file
                if(nucleusRE.match(line)):
                    nucleus = True
                if(cellBodyRE.match(line)):
                    cellBody = True
                if(dendRE.match(line)):
                    dend = True
                if(axonRE.match(line)):
                    axon = True
                
                #clean up the names of the files
                if (output[-1] == '_'):
                    output = output[0:-1]
                if (output[0:3] == 'obj'):
                    output = output[5:]
                if (nueronal.match(line)):
                    spl = output.split('_neuronal')
                    output = spl[0] + spl[1]
                output = output + '.obj'
                
                directory = inputFile
                if not os.path.exists(directory):
                        os.makedirs(directory)
                #Make the File
                
                openFile = open(directory +'/'+ output, 'w+')
                gFound = True
                totalCount = totalCount + runningCount
                runningCount = 0
            elif (gFound == True):
                if(vs.match(line)):
                    runningCount = runningCount +1
                    openFile.write(line)
                    
                elif(fs.match(line)):    
                    sLine = line.split()
                    
                    openFile.write(sLine[0] + " " + str(int(sLine[1])-totalCount) + " " + str(int(sLine[2])-totalCount) + " " + str(int(sLine[3])-totalCount) + "\n")
    #Write the log stuff
    totalCount = 0
    runningCount = 0
    logFile.write(inputFile)
    logFile.write('\nFound nucleus: ' + str(nucleus) +'\n')
    logFile.write('Found cellBody: ' + str(cellBody)+'\n')
    logFile.write('Found dend: ' + str(dend)+'\n')
    logFile.write('Found axon: ' + str(axon)+'\n\n\n')                
    nucleus = False
       cellBody = False
    dend = False
    axon = False                
                    

data()
