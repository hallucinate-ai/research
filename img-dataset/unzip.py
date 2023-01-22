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
	zipFileList = os.listdir(cwd + "/imageArchives")
	#sort the list
	zipFileList.sort()
	zipFileList = [file for file in zipFileList if file.endswith(".zip")]

	if not os.path.exists(cwd + "images"):
		os.makedirs(cwd + "images")
	else:
		pass
	#filter if the file is a zip file
	for zipFile in zipFileList:
		print("Unzipping " + zipFile)
		#unzip the file
		shutil.unpack_archive(cwd + "/imageArchives/" + zipFile, cwd + "/images/")
		os.remove(cwd + "/imageArchives/" + zipFile)
	return

if __name__ == "__main__":
	main()