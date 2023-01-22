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


def main():
	cwd = os.path.dirname(os.path.realpath(__file__))
	for i in range(1, 2000):
		#download the file
		command = "python3 download.py -i " + str(i) + " -r" + str(i + 1)
		print(command)
		subprocess.call(command, shell=True)
		zipFileList = os.listdir(cwd + "/images")
		#sort the list
		zipFileList.sort()
		if not os.path.exists("/tmp/images"):
			os.makedirs("/tmp/images")
		else:
			shutil.rmtree("/tmp/images")
			os.makedirs("/tmp/images")
		#filter if the file is a zip file
		zipFileList = [file for file in zipFileList if file.endswith(".zip")]
		for zipFile in zipFileList:
			print("Unzipping " + zipFile)
			#unzip the file
			shutil.unpack_archive(cwd + "/images/" + zipFile, "/tmp/images/")
			command = "s3cmd --config=cw-object-storage-config_stable-diffusion put /tmp/images/*.png s3://diffusiondb/images/"
			print(command)
			subprocess.call(command, shell=True)
			commannd = "s3cmd --config=cw-object-storage-config_stable-diffusion put /tmp/images/*.json s3://diffusiondb/metadata/"
			print(command)
			subprocess.call(command, shell=True)
			os.remove(cwd + "/images/" + zipFile)
	return

if __name__ == "__main__":
	main()