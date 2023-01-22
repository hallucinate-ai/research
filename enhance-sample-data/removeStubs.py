def removeStubs(dirname):
	import os
	import sys
	import json
	#change directory to samples directory
	cwd = os.getcwd()
	os.chdir(dirname)
	#iterate through every png file in the directory
	for filename in os.listdir('.'):
		if filename.endswith('_src.png'):
			if os.path.exists( str(cwd + "/" + dirname + filename).replace("_src.png", ".json")):
				print('Did not remove ' + filename)
			else:
				print('Removed ' + filename)
				os.remove(str(cwd + "/" + dirname + filename))
		elif filename.endswith('_dst.png'):
			if os.path.exists(str(cwd + "/" + dirname + filename).replace("_dst.png", ".json")):
				print('Did not remove ' + filename)
			else:
				print('Removed ' + filename)
				os.remove(str(cwd + "/" + dirname + filename))
		elif filename.endswith('_mask.png'):
			if os.path.exists(str(cwd + "/" + dirname + filename).replace("_mask.png", ".json")):
				print('Did not remove ' + filename)
			else:
				print('Removed ' + filename)
				os.remove(str(cwd + "/" + dirname + filename))
		elif filename.endswith('.json'):
			if os.path.exists(str(cwd + "/" + dirname + filename).replace(".json", "_dst.png")):
				print('Did not remove ' + filename)
			else:
				print('Removed ' + filename)
				os.remove(str(cwd + "/" + dirname + filename))
			
			new_json_file = {}
			json_file = json.load(open(str(cwd + "/" + dirname + filename)))
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
			print(new_json_file)
			with open(filename, 'w') as outfile:
				json.dump(new_json_file, outfile)
		
		else:
			print('Not a png or json file: ' + filename)

if __name__ == "__main__":
	removeStubs()