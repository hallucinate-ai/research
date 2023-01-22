import os
import sys
import json

#open the json file
json_file = json.load(open("samples_txt2img.json"))
new_json = []
#loop through the json file and fix the data
for data in json_file:
	new_dict = {}
	#print(data["scores"]["aesthetic_score_difference"])
	src_aesthetic_score = data["scores"]["src_aesthetic_score"]
	dst_aesthetic_score = data["scores"]["dst_aesthetic_score"]
	new_dict["modelQuery"] = data["modelQuery"]
	new_dict["bg_image"] = data["bg_image"]
	new_dict["scores"] = data["scores"]
	if "scores" in data:
		if "dst_aesthetic_score" in data["scores"] and "src_aesthetic_score" in data["scores"]:
			new_dict["scores"]["src_aesthetic_score"] = dst_aesthetic_score
			new_dict["scores"]["dst_aesthetic_score"] = src_aesthetic_score
			new_dict["scores"]["aesthetic_score_difference"] = str(  float(data["scores"]["dst_aesthetic_score"]) - float(data["scores"]["src_aesthetic_score"]))
			print(new_dict["scores"]["aesthetic_score_difference"])
			
	new_json.append(new_dict)

#write the new json file
with open("fixed.json", 'w') as outfile:
	json.dump(new_json, outfile)
