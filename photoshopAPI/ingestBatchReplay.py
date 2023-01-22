import os 
import sys
import json

cwd = os.path.dirname(os.path.abspath(__file__))
## parent directory of cwd ##
parent = os.path.dirname(cwd)
## subdirectory of parent ##
subdir = os.path.join(parent, "alchemist-recordings")
## get the list of files in the subdirectory ##
files = os.listdir(subdir)
## loop through the files in the subdirectory ##
filelist = []
for file in files:
	if file.endswith(".json"):
		filelist.append(file)

commandList = {}
	
for file in filelist:	
	file_path = os.path.join(subdir, file)
	## open the file ##
	with open(file_path) as f:
		name = file.split(".")[0]
		## load the json file into a dictionary ##
		data = json.load(f)
		print(file_path)
		print(data)
		commandList[name] = {}
		commandList[name]["batchPlay"] = data
		commandList[name]["comments"] = []
		commandList[name]["kwargs"] = {}
		commandList[name]["emits"] = {}

with open(cwd + "/commandList.json", "w") as f:
	json.dump(commandList, f, indent=4)
