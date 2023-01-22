import os
import sys
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

#if there are 2 args

arg1 = 1
arg2 = 0.5
if len(sys.argv) == 2:
	arg1 = sys.argv[1]
	arg2 = sys.argv[2]


def load_json(path):
	return pd.read_json(path)

def load_json2(path):
	return json.load(open(path))

json_data = load_json2("samples mask.json")

for data in json_data:
	if "scores" not in data:
		print("no scores in data")
		print(data)
		continue
	else:
		if "dst_aesthetic_score" not in data["scores"]:
			print("no dst_aesthetic_score in data")
			print(data)
			continue
		
#sort by json_data["scores"]["dst_aesthetic_score"]
sorted_json_data_by_aesthetic_score = sorted(json_data, key=lambda k: float(k['scores']['dst_aesthetic_score']), reverse=True)

sorted_json_data_by_aesthetic_difference = sorted(json_data, key=lambda k: float(k['scores']['aesthetic_score_difference']), reverse=True)

sorted_json_data_by_dst_similarity = sorted(json_data, key=lambda k: float(k['scores']['dst_similarity']), reverse=True)

sorted_json_data_by_diff_similarity = sorted(json_data, key=lambda k: float(k['scores']['diff_similarity']), reverse=True)

#filter json_data by ["modelQuery"]["params"]["ddim_steps"] < 1000

filtered_json_data_by_aesthetic_score = [x for x in json_data if float(x["scores"]["dst_aesthetic_score"]) > 5.0]

filtered_json_data_by_dst_similarity = [x for x in filtered_json_data_by_aesthetic_score if float(x["scores"]["dst_similarity"]) > 6.5]

filtered_json_data_by_ddim_steps = [x for x in filtered_json_data_by_dst_similarity if int(x["modelQuery"]["params"]["ddim_steps"]) < 1000]


#find correlations between aesthetic_score_difference and cfg_scale, ddim_steps, and denoising_strength
dst_aesthetic_score = []
cfg_scale = []
ddim_steps = []
denoising_strength = []
mod_similarity = []
dst_similarity = []
diff_similarity = []
dst_aesthetic_score = []
src_similarity = []
src_aesthetic_score = []
diff_aesthetic_score = []
statsReport = { }
#statsReport = { cfg_scale : {}, ddim_steps : {}, denoising_strength : {}, mod_similarity : {}, dst_similarity : {}, diff_similarity : {}, dst_aesthetic_score: {}, src_similarity: {}, src_aesthetic_score: {}, diff_aesthetic_score: {}}
statsReport["cfgScale"] = {}
statsReport["ddimSteps"] = {}
statsReport["denoisingStrength"] = {}
statsReport["modSimilarity"] = {}
statsReport["dstSimilarity"] = {}
statsReport["diffSimilarity"] = {}
statsReport["dstAestheticScore"] = {}
statsReport["aestheticScoreDifference"] = {}
statsReport["srcSimilarity"] = {}
statsReport["srcAestheticScore"] = {}
statsReport["diffAestheticScore"] = {}


for data in filtered_json_data_by_ddim_steps:
	cfg_scale.append(float(data["modelQuery"]["params"]["cfg_scale"]))
	ddim_steps.append(float(data["modelQuery"]["params"]["ddim_steps"]))
	denoising_strength.append(float(data["modelQuery"]["params"]["denoising_strength"]))
	mod_similarity.append(float(data["scores"]["mod_similiarity"]))
	dst_similarity.append(float(data["scores"]["dst_similarity"]))
	diff_similarity.append(float(data["scores"]["diff_similarity"]))
	dst_aesthetic_score.append(float(data["scores"]["dst_aesthetic_score"]))
	src_similarity.append(float(data["scores"]["src_similarity"]))
	src_aesthetic_score.append(float(data["scores"]["src_aesthetic_score"]))
	diff_aesthetic_score.append(float(data["scores"]["aesthetic_score_difference"]))


# get the standard deviation of the variables
std_cfg_scale = np.std(cfg_scale)
std_ddim_steps = np.std(ddim_steps)
std_denoising_strength = np.std(denoising_strength)
std_mod_similarity = np.std(mod_similarity)
std_dst_similarity = np.std(dst_similarity)
std_diff_similarity = np.std(diff_similarity)
std_dst_aesthetic_score = np.std(dst_aesthetic_score)
std_src_similarity = np.std(src_similarity)
std_src_aesthetic_score = np.std(src_aesthetic_score)
std_diff_aesthetic_score = np.std(diff_aesthetic_score)

mean_cfg_scale = np.mean(cfg_scale)
mean_ddim_steps = np.mean(ddim_steps)
mean_denoising_strength = np.mean(denoising_strength)
mean_mod_similarity = np.mean(mod_similarity)
mean_dst_similarity = np.mean(dst_similarity)
mean_diff_similarity = np.mean(diff_similarity)
mean_dst_aesthetic_score = np.mean(dst_aesthetic_score)
mean_src_similarity = np.mean(src_similarity)
mean_src_aesthetic_score = np.mean(src_aesthetic_score)
mean_diff_aesthetic_score = np.mean(diff_aesthetic_score)


#remove an index from every list if it is beyond 2 standard deviation from the mean
for i in range(len(cfg_scale)-1, -1, -1):
	if cfg_scale[i] > (np.mean(cfg_scale) + 2* std_cfg_scale) or cfg_scale[i] < (np.mean(cfg_scale) - 2*std_cfg_scale):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif ddim_steps[i] > (np.mean(ddim_steps) + 2*std_ddim_steps) or ddim_steps[i] < (np.mean(ddim_steps) - 2*std_ddim_steps):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif denoising_strength[i] > (np.mean(denoising_strength) + 2*std_denoising_strength) or denoising_strength[i] < (np.mean(denoising_strength) - 2*std_denoising_strength):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif mod_similarity[i] > (np.mean(mod_similarity) + 2*std_mod_similarity) or mod_similarity[i] < (np.mean(mod_similarity) - 2*std_mod_similarity):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif dst_similarity[i] > (np.mean(dst_similarity) + 2*std_dst_similarity) or dst_similarity[i] < (np.mean(dst_similarity) - 2*std_dst_similarity):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif diff_similarity[i] > (np.mean(diff_similarity) + 2*std_diff_similarity) or diff_similarity[i] < (np.mean(diff_similarity) - 2*std_diff_similarity):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif dst_aesthetic_score[i] > (np.mean(dst_aesthetic_score) + 2*std_dst_aesthetic_score) or dst_aesthetic_score[i] < (np.mean(dst_aesthetic_score) - 2*std_dst_aesthetic_score):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif src_similarity[i] > (np.mean(src_similarity) + 2*std_src_similarity) or src_similarity[i] < (np.mean(src_similarity) - 2*std_src_similarity):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif src_aesthetic_score[i] > (np.mean(src_aesthetic_score) + 2*std_src_aesthetic_score) or src_aesthetic_score[i] < (np.mean(src_aesthetic_score) - 2*std_src_aesthetic_score):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]
	elif diff_aesthetic_score[i] > (np.mean(diff_aesthetic_score) + 2*std_diff_aesthetic_score) or diff_aesthetic_score[i] < (np.mean(diff_aesthetic_score) - 2*std_diff_aesthetic_score):
		del cfg_scale[i]
		del ddim_steps[i]
		del denoising_strength[i]
		del mod_similarity[i]
		del dst_similarity[i]
		del diff_similarity[i]
		del dst_aesthetic_score[i]
		del src_similarity[i]
		del src_aesthetic_score[i]
		del diff_aesthetic_score[i]

#normalize the data as a vector
dst_aesthetic_score_norm = [(x - min(dst_aesthetic_score)) / (max(dst_aesthetic_score) - min(dst_aesthetic_score)) for x in dst_aesthetic_score]
dst_similarity_norm = [(x - min(dst_similarity)) / (max(dst_similarity) - min(dst_similarity)) for x in dst_similarity]
mod_similarity_norm = [(x - min(mod_similarity)) / (max(mod_similarity) - min(mod_similarity)) for x in mod_similarity]
diff_similarity_norm = [(x - min(diff_similarity)) / (max(diff_similarity) - min(diff_similarity)) for x in diff_similarity]
src_similarity_norm = [(x - min(src_similarity)) / (max(src_similarity) - min(src_similarity)) for x in src_similarity]
cfg_scale_norm = [(x - min(cfg_scale)) / (max(cfg_scale) - min(cfg_scale)) for x in cfg_scale]
ddim_steps_norm = [(x - min(ddim_steps)) / (max(ddim_steps) - min(ddim_steps)) for x in ddim_steps]
denoising_strength_norm = [(x - min(denoising_strength)) / (max(denoising_strength) - min(denoising_strength)) for x in denoising_strength]

statsReport = { 
	"cfg_scale" : { "mean" : mean_cfg_scale, "std" : std_cfg_scale , "min" : min(cfg_scale), "max": max(cfg_scale) },
	"ddim_steps" : { "mean" : mean_ddim_steps, "std" : std_ddim_steps , "min" : min(ddim_steps), "max": max(ddim_steps) },
	"denoising_strength" : { "mean" : mean_denoising_strength, "std" : std_denoising_strength , "min" : min(denoising_strength), "max": max(denoising_strength) },
	"mod_similarity" : { "mean" : mean_mod_similarity, "std" : std_mod_similarity , "min" : min(mod_similarity), "max": max(mod_similarity) }, 
	"dst_similarity" : { "mean" : mean_dst_similarity, "std" : std_dst_similarity , "min" : min(dst_similarity), "max": max(dst_similarity) },
	"diff_similarity" : { "mean" : mean_diff_similarity, "std" : std_diff_similarity , "min" : min(diff_similarity), "max": max(diff_similarity) }, 
	"dst_aesthetic_score": { "mean" : mean_dst_aesthetic_score, "std" : std_dst_aesthetic_score , "min" : min(dst_aesthetic_score), "max": max(dst_aesthetic_score) }, 
	"src_similarity": { "mean" : mean_src_similarity, "std" : std_src_similarity , "min" : min(src_similarity), "max": max(src_similarity) }, 
	"src_aesthetic_score": { "mean" : mean_src_aesthetic_score, "std" : std_src_aesthetic_score , "min" : min(src_aesthetic_score), "max": max(src_aesthetic_score) },
	"diff_aesthetic_score": { "mean" : mean_diff_aesthetic_score, "std" : std_diff_aesthetic_score , "min" : min(diff_aesthetic_score), "max": max(diff_aesthetic_score) },
	}



#predict the highest dst_aesthetic_score based on cfg_scale, ddim_steps, and denoising_strength

length = int(round(len(dst_aesthetic_score) / 2))

#split the data into training/testing sets

cfg_scale_train = cfg_scale[:length]
cfg_scale_test = cfg_scale[length:]

ddim_steps_train = ddim_steps[:length]
ddim_steps_test = ddim_steps[length:]

denoising_strength_train = denoising_strength[:length]
denoising_strength_test = denoising_strength[length:]

dst_aesthetic_score_train = dst_aesthetic_score[:length]
dst_aesthetic_score_test = dst_aesthetic_score[length:]

dst_similarity_train = dst_similarity[:length]
dst_similarity_test = dst_similarity[length:]

mod_similarity_train = mod_similarity[:length]
mod_similarity_test = mod_similarity[length:]

diff_similarity_train = diff_similarity[:length]
diff_similarity_test = diff_similarity[length:]

src_similarity_train = src_similarity[:length]
src_similarity_test = src_similarity[length:]

regr = linear_model.LinearRegression()
regr1 = linear_model.LinearRegression()
regr2 = linear_model.LinearRegression()
regr3 = linear_model.LinearRegression()
regr4 = linear_model.LinearRegression()
regr5 = linear_model.LinearRegression()
regr6 = linear_model.LinearRegression()

regr1.fit(np.column_stack((dst_aesthetic_score_train, dst_similarity_train, mod_similarity_train)), cfg_scale_train)
regr2.fit(np.column_stack((dst_aesthetic_score_train, dst_similarity_train, mod_similarity_train)), ddim_steps_train)
regr3.fit(np.column_stack((dst_aesthetic_score_train, dst_similarity_train, mod_similarity_train)), denoising_strength_train)
regr4.fit(np.column_stack((dst_aesthetic_score_train, dst_similarity_train)), mod_similarity_train )
regr5.fit(np.column_stack((dst_aesthetic_score_train, mod_similarity_train)), dst_similarity_train )
regr6.fit(np.column_stack((mod_similarity_train, dst_similarity_train)), dst_aesthetic_score_train )


selected_norm1 = arg1
selected_norm2 = arg2
#convert the selected_norm value to the corresponding mod_similarity value using the min and max of the mod_similarity
#selected_dst_aesthetic_score = (selected_norm1 * (max(dst_aesthetic_score) - min(dst_aesthetic_score))) + min(dst_aesthetic_score)
#print("selected_dst_aesthetic_score: ", selected_dst_aesthetic_score) # target aesthetic score
selected_mod_similarity = (selected_norm2 * (max(mod_similarity) - min(mod_similarity))) + min(mod_similarity)
print("selected_mod_similarity: ", selected_mod_similarity) #similarity between the src image and the dst image
selected_dst_similarity = (selected_norm1 * (max(dst_similarity) - min(dst_similarity))) + min(dst_similarity)
print("selected_dst_similarity: " ,selected_dst_similarity) #similarity to the promp image

# predict the dst_aesthetic_score using the selected_mod_similarity and selected_dst_similarity
#selected_dst_similarity = regr6.predict(np.column_stack((selected_mod_similarity, selected_dst_aesthetic_score)))
selected_dst_aesthetic_score = regr6.predict(np.column_stack((selected_mod_similarity, selected_dst_similarity)))
print("selected_dst_aesthetic_score: ", selected_dst_aesthetic_score)

# predict the cfg_scale, ddim_steps, denoising_strength using the selected_dst_aesthetic_score, selected_dst_similarity, selected_mod_similarity
selected_cfg_scale = regr1.predict(np.column_stack((selected_dst_aesthetic_score, selected_dst_similarity, selected_mod_similarity)))
selected_ddim_steps = regr2.predict(np.column_stack((selected_dst_aesthetic_score, selected_dst_similarity, selected_mod_similarity)))
selected_denoising_strength = regr3.predict(np.column_stack((selected_dst_aesthetic_score, selected_dst_similarity, selected_mod_similarity)))

print("selected_cfg_scale: ", selected_cfg_scale)
print("selected_ddim_steps: ", selected_ddim_steps)
print("selected_denoising_strength: ", selected_denoising_strength)

test = regr1.intercept_
statsReport["regressions"] = {}
statsReport["regressions"] = { "cfg_scale": str(regr1.coef_), "ddim_steps": str(regr2.coef_), "denoising_strength": str(regr3.coef_), "aesthetic_score": str(regr6.coef_)}
statsReport["intercepts"] = {}
statsReport["intercepts"] = { "cfg_scale": str(regr1.intercept_), "ddim_steps": str(regr2.intercept_), "denoising_strength": str(regr3.intercept_), "aesthetic_score": str(regr6.intercept_)}
print("Regression Coefficients: ", statsReport["regressions"])

#write the statsReport to a json file
with open("./statsReport.json", "w") as f:
	json.dump(statsReport, f, indent=4)