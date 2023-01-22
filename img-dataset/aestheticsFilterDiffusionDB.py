import os
import sys
import re
import shutil
import json

cwd = os.path.dirname(os.path.realpath(__file__))
fileDict = {}


## get each tab separated value from tsv file
with open(cwd + "/aestheticsDiffusiondb.tsv", "r") as tsvFile:
	### get all of the lines from tsvFile
	lines = tsvFile.readlines()
	#print("lines: " + str(len(lines)))
	for i in range(0, len(lines)):
		line = lines[i]
		#print (line)
		fields = line.split("\t")
		#print(fields)
		## get the first field
		filename = fields[0]
		#print(filename)
		## get the second field
		## if fields[1] is a number, then convert it to a float
		#print(fields[1])
		aestheticValue = fields[1]
		## use a regular expression to filter out non numeric values from aestheticValue 
		aestheticValue = re.sub(r'[^\d\.]', '', aestheticValue)
		if aestheticValue != "":
			if float(aestheticValue) > 0:
				aestheticValue = float(aestheticValue)
			else:
				aestheticValue = 0
		else:
			aestheticValue = 0
		#print(filename)
		#print(aestheticValue)
		## assign the aestheticValue to the filename key in the fileDict
		fileDict[filename] = aestheticValue

		#if filename.endswith('.jpg') or filename.endswith('.png') or filename.endswith('.jpeg') or filename.endswith('.gif') or filename.endswith('.webp'):
		#	fileDict[filename] = aestheticValue

filterDict = {}
print( "fileDict: " + str(len(fileDict.keys())))
## filter the fileDict for aesthetic values to include only keys with aestheticValue above 6.5
for key in fileDict.keys():
	value = fileDict[key]
	if float(value) > float(6.5):
		filterDict[key] = float(value)
		#print (key + " " + str(value))

for key in filterDict.keys():
	value = filterDict[key]
	print (key + " " + str(value))
	if not os.path.exists(cwd + "/filteredDiffusiondb"):
		os.makedirs(cwd + "/filteredDiffusiondb")
	if not os.path.exists(cwd + "/filteredDiffusiondb/" + key):
		shutil.copy(cwd + "/images/" + key, cwd + "/filteredDiffusiondb/" + key)

## save the filteredDict to a json file
with open(cwd + "/filteredDiffusionDB.json", "w") as jsonFile:
	json.dump(filterDict, jsonFile)


countFilterDict = len(filterDict.keys())
countFileDict = len(fileDict.keys())
print("countFilteredFileDict: " + str(countFilterDict))
print("countFileDict: " + str(countFileDict))


	