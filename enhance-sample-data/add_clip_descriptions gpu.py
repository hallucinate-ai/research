import torch
from PIL import Image
import open_clip
import os
import sys
import json
import numpy as np
open_clip.list_pretrained()
#exit()
device = "cuda" if torch.cuda.is_available() else "cpu"
model, _, preprocess = open_clip.create_model_and_transforms('ViT-g-14', pretrained='laion2b_s12b_b42k', device=device)
model=model.cuda()
#model.to('cuda')
def process(dir):
	for filename in os.listdir(dir):
		if filename.endswith('.json'):
			print(filename)
			json_file = json.load(open(dir + "/" + filename))
			prompt = json_file["modelQuery"]["params"]["prompt"]
			print(prompt)
			text = open_clip.tokenize([prompt])
			image_src = preprocess(Image.open(dir + "/" +filename.replace(".json", "_src.png"))).unsqueeze(0).to(device)
			image_dst = preprocess(Image.open(dir + "/" +filename.replace(".json", "_dst.png"))).unsqueeze(0).to(device)
			with torch.no_grad(), torch.cuda.device(device):
				src_image_features = model.encode_image(image_src).float()
				dst_image_features = model.encode_image(image_dst).float()
				src_text_features = model.encode_text(text).to(device).float()
				dst_text_features = model.encode_text(text).to(device).float()
				##print("src_text_features:", src_text_features)  # prints: [[1., 0., 0.]]
				##print("dst_text_features:", dst_text_features)  # prints: [[1., 0., 0.]]		
				##print("src_image_features:", src_image_features)  # prints: [[1., 0., 0.]]
				##print("dst_image_features:", dst_image_features)  # prints: [[1., 0., 0.]]
				src_image_features /= src_image_features.norm(dim=-1, keepdim=True)
				dst_text_features /= dst_text_features.norm(dim=-1, keepdim=True)
				src_similarity = src_text_features.cpu().numpy() @ src_image_features.cpu().numpy().T
				dst_similarity = dst_text_features.cpu().numpy() @ dst_image_features.cpu().numpy().T
				mod_similiarity = src_image_features.cpu().numpy() @ dst_image_features.cpu().numpy().T
				print("src_similarity:", src_similarity[0][0])  # prints: [[1., 0., 0.]]
				print("dst_similarity:", dst_similarity[0][0])  # prints: [[1., 0., 0.]]
				print("mod_similiarity:", mod_similiarity[0][0])  # prints: [[1., 0., 0.]]

			json_file["scores"]["src_similarity"] = str(src_similarity[0][0])
			json_file["scores"]["dst_similarity"] = str(dst_similarity[0][0])
			json_file["scores"]["mod_similiarity"] = str(mod_similiarity[0][0])
			json_file["scores"]["diff_similarity"] = str(dst_similarity[0][0] - src_similarity[0][0])
			json_file["scores"]["prompt_length"] = str(len(prompt))
			with open(dir + "/" + filename, 'w') as outfile:
				json.dump(json_file, outfile)
			
		




process("./samples mask/")
