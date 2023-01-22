import os
import sys

#change directory to samples directory
os.chdir('samples')

#iterate through every png file in the directory
for filename in os.listdir('.'):
	if filename.endswith('.png'):
		if os.path.exists(filename.replace("_src", "").replace("_dst", "").replace(".png", ".json")):
			print('Did not remove ' + filename)
		else:
			print('Removed ' + filename)
			os.remove(filename)
	else:
		print('Not a png file: ' + filename)