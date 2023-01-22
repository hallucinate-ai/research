import os
import sys
import json
#change directory to samples directory
os.chdir('samples')

#iterate through every png file in the directory
for filename in os.listdir('.'):
	if filename.endswith('.jpg'):
		if os.path.exists(filename.replace(".jpg", ".json")):
			print('Did not remove ' + filename)
		else:
			print('Removed ' + filename)
			os.remove(filename)
	elif filename.endswith('.json'):
		if os.path.exists(filename.replace(".json", ".jpg")):
			print('Did not remove ' + filename)
		else:
			print('Removed ' + filename)
			os.remove(filename)
		
		new_json_file = {}
		json_file = json.load(open(filename))
		if "prompt" in json_file:
			new_json_file["modelQuery"] = {}
			new_json_file["modelQuery"]["model"] = "stable-diffusion-v1"
			new_json_file["modelQuery"]["params"] = {}
			move_params = ["prompt", "denoising_strength","ddim_steps","cfg_scale","contextBytes","maskBytes"]
			for param in move_params:
				new_json_file["modelQuery"]["params"][param] = json_file[param]
			new_json_file["modelQuery"]["params"]["seed"] = 0
		else:
			new_json_file["modelQuery"] = json_file["modelQuery"]
		
		new_json_file["scores"] = json_file["scores"]
		new_json_file["bg_image"] = {}
		new_json_file["bg_image"]["url"] = "noise_512x512.png"
		new_json_file["bg_image"]["caption"] = "noise perlin"
		new_json_file["bg_image"]["id"] = ""
		new_json_file["bg_image"]["size"] = [512,512]
		new_json_file["bg_image"]["image_ratio"] = "1"
		print(new_json_file)
		with open(filename, 'w') as outfile:
			json.dump(new_json_file, outfile)
	
	else:
		print('Not a png or json file: ' + filename)