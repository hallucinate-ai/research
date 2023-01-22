import torch
from PIL import Image
import open_clip
import os
import sys
import json
import numpy as np
open_clip.list_pretrained()
#exit()
model, _, preprocess = open_clip.create_model_and_transforms('ViT-g-14', pretrained='laion2b_s12b_b42k')
#model.to('cuda')
def process(dir):
	for filename in os.listdir(dir):
		if filename.endswith('.json'):
			print(filename)
			json_file = json.load(open(dir + "/" + filename))
			print(json_file)
			if "prompt" in json_file["modelQuery"]["params"]:
				prompt = json_file["modelQuery"]["params"]["prompt"]
			elif "prompt" in json_file:
				prompt = json_file["prompt"]
			print(prompt)
			text = open_clip.tokenize([prompt])
			image_dst = preprocess(Image.open(dir + "/" +filename.replace(".json", ".jpg"))).unsqueeze(0)
			with torch.no_grad(), torch.cuda.amp.autocast():
				dst_image_features = model.encode_image(image_dst).float()
				dst_text_features = model.encode_text(text).float()
				dst_text_features /= dst_text_features.norm(dim=-1, keepdim=True)
				dst_similarity = dst_text_features.cpu().numpy() @ dst_image_features.cpu().numpy().T
				print("dst_similarity:", dst_similarity[0][0])  # prints: [[1., 0., 0.]]
			json_file["scores"]["dst_similarity"] = str(dst_similarity[0][0])
			json_file["scores"]["prompt_length"] = str(len(prompt))
			with open(dir + "/" + filename, 'w') as outfile:
				json.dump(json_file, outfile)
			
		




process("./samples")