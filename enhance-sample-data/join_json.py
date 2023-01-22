import os
import sys
import json	

cwd = os.getcwd()

def processJson(dir):
	combined_json = []
	print("processing json")
	print(cwd + "/" + dir)
	print( str(os.listdir(cwd + "/" + dir).__len__()) + " files found")
	for filename in os.listdir(cwd + "/" + dir):
		if filename.endswith('.json'):
			#print(filename)
			json_data = json.load(open(cwd + "/" + dir  + filename))
			if "scores" not in json_data:
				print("\n no scores in data")
				print(json_data)
				continue
			elif "dst_aesthetic_score" not in json_data["scores"]:
				print("\n no dst_aesthetic_score in data")
				print(json_data)
				continue
			else:
				combined_json.append(json_data)
	#create a new json file with the combined data
	print("writing combined json")
	print(cwd + "/" + dir.replace("/","") + ".json")
	with open(cwd + "/" + dir.replace("/","") + ".json", 'w') as outfile:
		json.dump(combined_json, outfile)

	
