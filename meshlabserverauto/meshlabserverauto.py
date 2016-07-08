import os
import sys
import subprocess

directory = './output'

if not os.path.exists(directory):
    os.makedirs(directory)

for root, dirs, files in os.walk(sys.argv[1], topdown=False):
    for name in files:
        s = 'meshlabserver -i ' + os.path.join(root, name) + ' -o output/' + name[:-17] + '.obj -s ' + sys.argv[2]
        #print(os.path.join(root, name))
        print s
        #print name
        subprocess.call(s, shell=True)
