#testing.

import shapemorph
import os
import re
import shutil

def displacement(check_list):
	gaps = []
	for i, j in enumerate(check_list):
		if j == 1:
			gaps.append(i)
	return gaps

def natural_sort(l): 
    convert = lambda text: int(text) if text.isdigit() else text.lower() 
    alphanum_key = lambda key: [ convert(c) for c in re.split('([0-9]+)', key) ] 
    return sorted(l, key = alphanum_key)

#get file names
dest = '/home/archimedes/Documents/src/python/shapemorph/third'
files = [f for f in os.listdir(dest) if os.path.isfile(os.path.join(dest,f)) ]

total_files = len(files)

#print files

sorted_files = natural_sort(files)

#Test output
src_dest = os.getcwd() + '/4thtry_mk1'

validity = []
for f in sorted_files:
	if (shapemorph.checkContours(f, dest)):
		validity.append(1)
	else:
		validity.append(0)

#print validity

gaps = displacement(validity)

iterate = []
ndx = 0
while (ndx + 1) < len(gaps):
	iterate.append([gaps[ndx], gaps[ndx+1]])
	ndx = ndx + 1

print 'Gaps between slices at indexes...',
print gaps

extension = '.tiff'

#print sorted_files	

missing = []

for pair in iterate:

	scale_gap = 1/float(pair[1]-pair[0])
	currScale = scale_gap


	#copy original files over for pairs

	file1 = sorted_files[pair[0]]
	file2 = sorted_files[pair[1]]

	shutil.copy(dest + '/' + file1, src_dest)

	while currScale < 1:

		replace = '_' + str(int(currScale*100)) + extension
		file3 = file1.replace(".tiff", replace)
		file3 = src_dest + '/' + file3
		currScale = currScale + scale_gap

		try:
			shapemorph.main(file1, file2, currScale, file3, dest)
		except IndexError:
			print 'Pairing error at {}'.format(pair)
			missing.append(pair)
			print 'Missing images -> {}'.format(pair[1]-pair[0])
			#shutil.copy()
			continue

if (gaps[-1] < total_files):
	for file_index in range(gaps[-1], (total_files), 1):
		orig_file = dest + '/' + sorted_files[file_index]
		shutil.copy(orig_file, src_dest)


# take care of gaps here








# while (ndx+1)<len(sorted_files):
#     scale = .1
#     while scale < 1:
#     	file1 = sorted_files[ndx]
#     	file2 = sorted_files[ndx+10]
    	
#     	try:
#     	shapemorph.main(file1, file2, scale, file1 + '_' + str(scale), dest)
    	
#     	scale = scale + .1
#     ndx = ndx+10

# try:
# 	shapemorph.main('VCN_c01_input05_axon_cropped-000.tiff', 'VCN_c01_input05_axon_cropped-010.tiff', .5, src_dest + '/w0t.tiff', dest)
# except IndexError:
# 	print 'woops.'


