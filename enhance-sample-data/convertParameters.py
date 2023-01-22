import os
import sys
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt



data = json.load(open("statsReport.json"))

regressions = data["regressions"]
intercepts = data["intercepts"]
#print(regressions)
#print the keys of data
#print(data.keys())
intercept_aesthetic_score = intercepts['aesthetic_score']
intercept_cfg_scale = intercepts['cfg_scale']
intercept_denoising_strength = intercepts['denoising_strength']
intercept_ddim_steps = intercepts['ddim_steps']
regr_aesthetic_score = regressions["aesthetic_score"]
regr_cfg_scale = regressions["cfg_scale"]
regr_denoising_strength = regressions["denoising_strength"]
regr_ddim_steps = regressions["ddim_steps"]
dst_aesthetic_score = data["dst_aesthetic_score"]
cfg_scale = data["cfg_scale"]
ddim_steps = data["ddim_steps"]
denoising_strength = data["denoising_strength"]
dst_similarity = data["dst_similarity"]
mod_similarity = data["mod_similarity"]

#print(data.keys())

if (len(sys.argv) < 2):
	print("Usage: python convertParameters.py <input_file>")
	sys.exit(1)
else:
	arg1 = sys.argv[1]
	arg2 = sys.argv[2]

#predict the aesthetic score from the linear regression regr_aesthetic_score using arg1 and arg2
t1 = float(arg1)
t2 = float(arg2)

dst_similarity_min = dst_similarity["mean"] - (dst_similarity["std"] * 2)
dst_similarity_max = dst_similarity["mean"] + (dst_similarity["std"] * 2)
dst_similarity_score = ((( dst_similarity_max - dst_similarity_min ) * float(arg2)) + dst_similarity_min)

mod_similarity_min = mod_similarity["mean"] - (mod_similarity["std"] * 2)
mod_similarity_max = mod_similarity["mean"] + (mod_similarity["std"] * 2)
mod_similarity_score = ((( mod_similarity_max - mod_similarity_min ) * float(arg2)) + mod_similarity_min)

print("mod_similarity_score = ", mod_similarity_score)
print("dst_similarity_score = ", dst_similarity_score)
print(t1,t2)
regr_aesthetic_score = regr_aesthetic_score.replace("[", "")
regr_aesthetic_score = regr_aesthetic_score.replace("]", "")
regr_aesthetic_score = regr_aesthetic_score.split("  ")
print (regr_aesthetic_score)

predicted_aesthetic_score = float(intercept_aesthetic_score) + (float(mod_similarity_score) * float(regr_aesthetic_score[0])) + ( float(dst_similarity_score) * float(regr_aesthetic_score[1]) )

print("predicted_aesthetic_score = ",predicted_aesthetic_score)