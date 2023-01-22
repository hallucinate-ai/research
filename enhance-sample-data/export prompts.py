import os
import sys
import json
cwd = os.getcwd()

dir = "samples img2img"


prompt_list = []


for file in os.listdir(dir):
	if "json" in file and "kate" not in file:
		with open(dir + "/" + file ) as f:
			data = json.load(f)
			print(data["modelQuery"]["params"]["prompt"])
			prompt_list.append(data["modelQuery"]["params"]["prompt"])

dir = "samples"

for file in os.listdir(dir):
	if "json" in file and "kate" not in file:
		with open(dir + "/" + file ) as f:
			data = json.load(f)
			print(data["modelQuery"]["params"]["prompt"])
			prompt_list.append(data["modelQuery"]["params"]["prompt"])


# write prompts to json file
with open("./prompts.json", "w") as f:
	json.dump(prompt_list, f)



