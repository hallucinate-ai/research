import os
import sys
import shutil
from urllib.error import HTTPError
from urllib.request import urlretrieve
from os.path import exists
import subprocess
import shutil
import os
import time
import argparse
from PIL import Image
import json
def main():
	uploadedFileList = {}
	cwd = os.path.dirname(os.path.realpath(__file__))
	uploadedFilejson = cwd + "/uploadedFileList.json"
	uploadedFilejson = open(uploadedFilejson, "r").read()
	uploadedFileList = json.loads(uploadedFilejson)
	if (len(uploadedFileList.keys()) == 0):
		uploadedFileList = {}
	fileList = os.listdir(cwd + "/images/")
	## filter fileList with the keys from uploadedFileList
	fileList = [file for file in fileList if not file in uploadedFileList.keys()]
	i = 0
	for file in fileList:

		if file.endswith(".jpg") or file.endswith(".png") or file.endswith(".jpeg") or file.endswith(".gif") or file.endswith(".bmp") or file.endswith(".webp"):				
			skip = False
			try:
				im = Image.open(cwd + "/images/" + file)
				im.verify()
			except Exception as e:
				print(cwd + "/images/" + file + " deleted")
				os.remove(cwd + "/images/" + file)
				skip = True
				pass
			if (skip == False):
				command = "s3cmd --config=cw-object-storage-config_stable-diffusion put ./images/" + file + " s3://aesthetics/" + file
				print(command)
				subprocess.call(command, shell=True)
				uploadedFileList[file] = 1
				i = i + 1
				if (i % 100 == 0):
					with open(cwd + "/uploadedFileList.json", "w") as outfile:
						json.dump(uploadedFileList, outfile)


	return

if __name__ == "__main__":
	main()