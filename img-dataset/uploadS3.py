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
		shutil.unpack_archive(cwd + "/images/" + zipFile, cwd+ "/images/")
		shutil.delete(cwd + "/images/" + zipFile)
	return

if __name__ == "__main__":
	main()