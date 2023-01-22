import os
from re import X
import sys
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

def load_json(path):
	return pd.read_json(path)

def load_json2(path):
	return json.load(open(path))

cwd = os.getcwd()

json_data = load_json2(cwd + "/samples mask.json")

print("Total number of samples: " + str(len(json_data)))

def sort_by_score(json_data, score_name):
	return sorted(json_data, key=lambda x: x["scores"][score_name], reverse=True)

def filter_by_score(json_data, score_name, min_score, max_score):
	return [x for x in json_data if float(x["scores"][score_name]) >= min_score and float(x["scores"][score_name])	 <= max_score]

def get_average_score(json_data, score_name):
	return np.mean([float(x["scores"][score_name]) for x in json_data])

def fiter_by_param(json_data, param_name, param_value):
	return [x for x in json_data if x["modelQuery"]["params"][param_name] == param_value]

def get_values_for_param(json_data, param_name):
	return [x["modelQuery"]["params"][param_name] for x in json_data]


sampler_names = get_values_for_param(json_data, "sampler_name")
unique_sampler_names = list(set(sampler_names))
print("Sampler names: " + str(unique_sampler_names))
average_scores = {}
for sampler_name in unique_sampler_names:
	mean_score = get_average_score(fiter_by_param(json_data, "sampler_name", sampler_name), "dst_aesthetic_score")
	average_scores[sampler_name] = mean_score
print("Average scores: " + str(average_scores))

#sort = sort_by_score(json_data, "dst_aesthetic_score")

#sort by json_data["scores"]["dst_aesthetic_score"]

#filter json_data by ["modelQuery"]["params"]["ddim_steps"] < 1000

filtered_json_data_by_ddim_steps = [x for x in json_data if float(x["modelQuery"]["params"]["ddim_steps"]) < 10000]

#filtered_json_data_by_sampler_name = [x for x in filtered_json_data_by_ddim_steps if x["modelQuery"]["params"]["sampler_name"] == "lms"]	

#find correlations between dst_aesthetic_score and dst_similarity

filtered_json_data_by_aesthetic_score = filter_by_score( filtered_json_data_by_ddim_steps, "dst_aesthetic_score", 5, 20)

dst_aesthetic_score = []
dst_similarity = []
dst_pixels = []
for data in filtered_json_data_by_ddim_steps:
	dst_aesthetic_score.append(float(data["scores"]["dst_aesthetic_score"]))
	dst_similarity.append(float(data["scores"]["dst_similarity"]))
	dst_pixels.append(float(data["scores"]["pixels"]))

plt.scatter(dst_aesthetic_score, dst_pixels)
plt.title("dst_aesthetic_score vs pixels")
plt.xlabel("dst_aesthetic_score")
plt.ylabel("pixels")
plt.show()

pixel_range = max(dst_pixels) - min(dst_pixels)
pixel_increment = 256*256
print ("pixel range: " + str(pixel_range))
print ("pixel increment: " + str(pixel_increment))
print ("pixel range / pixel increment: " + str(pixel_range / pixel_increment))

scoreDict = {}
for i in range(0, int(pixel_range/pixel_increment)):
	min_pixel = (i * pixel_increment) + min(dst_pixels)
	max_pixel = (i+1) * pixel_increment + min(dst_pixels)
	filtered_json_data_by_pixel = filter_by_score( filtered_json_data_by_ddim_steps, "pixels", min_pixel, max_pixel)
	average_score = get_average_score(filtered_json_data_by_pixel, "dst_aesthetic_score")
	if float(average_score) > 0:
		scoreDict[min_pixel] = average_score

print(scoreDict)

#split scoreDict into 2 lists
pixel_list = list(scoreDict.keys())
aesthic_mean_list = list(scoreDict.values())


plt.scatter(pixel_list, aesthic_mean_list)
plt.title("pixel_list vs aesthic_mean_list")
plt.xlabel("pixel_list")
plt.ylabel("aesthic_mean_list")
plt.show()

#get range of a list


#find correlations between aesthetic_score_difference and diff_similarity
aesthetic_score_difference = []
diff_similarity = []
for data in filtered_json_data_by_aesthetic_score:
	aesthetic_score_difference.append(float(data["scores"]["aesthetic_score_difference"]))
	diff_similarity.append(float(data["scores"]["diff_similarity"]))

#plt.scatter(aesthetic_score_difference, diff_similarity)
#plt.title("aesthetic_score_difference vs diff_similarity")
#plt.xlabel("aesthetic_score_difference")
#plt.ylabel("diff_similarity")
#plt.show()




#find correlations between aesthetic_score_difference and cfg_scale, ddim_steps, and denoising_strength
mod_similarity = []
dst_similarity = []
src_similarity = []
dst_aesthetic_score = []
aesthetic_score_difference = []
pixels = []
for data in filtered_json_data_by_aesthetic_score:
	mod_similarity.append(float(data["scores"]["mod_similiarity"]))
	dst_similarity.append(float(data["scores"]["dst_similarity"]))
	dst_aesthetic_score.append(float(data["scores"]["dst_aesthetic_score"]))
	src_similarity.append(float(data["scores"]["src_similarity"]))
	pixels.append(int(data["scores"]["pixels"]))
	aesthetic_score_difference.append(float(data["scores"]["aesthetic_score_difference"]))

print("diff_similarity vs cfg_scale")
print(np.corrcoef(mod_similarity, dst_similarity))
print("dst_aesthetic_score vs ddim_steps")
print(np.corrcoef(mod_similarity, dst_aesthetic_score))
print("dst_aesthetic_score vs denoising_strength")
print(np.corrcoef(mod_similarity, src_similarity))
plt.show()

#predict the highest aesthetic_score_difference based on cfg_scale, ddim_steps, and denoising_strength
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

length = int(round(len(mod_similarity) / 2))

#split the data into training/testing sets

dst_similarity_train = dst_similarity[:length]
dst_similarity_test = dst_similarity[length:]

dst_aesthetic_score_train = dst_aesthetic_score[:length]
dst_aesthetic_score_test = dst_aesthetic_score[length:]

mod_similarity_train = mod_similarity[:length]
mod_similarity_test = mod_similarity[length:]

src_similarity_train = src_similarity[:length]
src_similarity_test = src_similarity[length:]

aesthetic_score_difference_train = aesthetic_score_difference[:length]
aesthetic_score_difference_test = aesthetic_score_difference[length:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(np.column_stack(( dst_aesthetic_score_train, dst_similarity_train)), mod_similarity_train)

# Make predictions using the testing set
mod_similarity_pred = regr.predict(np.column_stack((dst_aesthetic_score_test, dst_similarity_test)))

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"

% mean_squared_error(mod_similarity_test, mod_similarity_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(mod_similarity_test, mod_similarity_pred))

# Plot outputs in a 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(cfg_scale_test, ddim_steps_test, denoising_strength_test, c=diff_similarity_test)
ax.scatter(mod_similarity_test, src_similarity_test, dst_similarity_test, c=aesthetic_score_difference_test)
ax.set_xlabel('mod_similarity_test')
ax.set_ylabel('src_similarity_test')
ax.set_zlabel('dst_similarity_test')
m = plt.cm.ScalarMappable(cmap=plt.cm.jet)
m.set_array(aesthetic_score_difference_test)
#label the colorbar
plt.colorbar(m, label='aesthetic_score_difference_test')
plt.show()

# Plot outputs


#load stats_data
with open('stats_data.json', "r") as f:
	stats_data = json.load(f)


stats = {}
stats["name"] = "fitness_landscape"
stats["correlations"] = {}
stats["correlations"]["dst_similarity"] = str(np.corrcoef(mod_similarity, dst_similarity)[0][1])
stats["correlations"]["dst_aesthetic_score"] = str(np.corrcoef(mod_similarity, dst_aesthetic_score)[0][1])
stats["coefficients"] = str(regr.coef_)
stats["mean_squared_error"] = str(mean_squared_error(mod_similarity_test, mod_similarity_pred))
stats["variance_score"] = str(r2_score(mod_similarity_test, mod_similarity_pred))

if len(stats_data) == 0:
	stats_data.append(stats)
else:
	for key, value in stats.items():
		#check if value is empty
		if value:
			if "name" in value:
				if value["name"] == stats["name"]:
					break
	stats_data.append(stats)		

#save stats_data
with open('stats_data.json', 'w') as f:
	json.dump(stats_data, f, indent=4)
