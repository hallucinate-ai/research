import os
import sys
import pandas as pd
import json
import numpy as np
import matplotlib.pyplot as plt

def load_json(path):
	return pd.read_json(path)

def load_json2(path):
	return json.load(open(path))

json_data = load_json2("samples_txt2img.json")

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
filtered_json_data_by_ddim_steps = [x for x in json_data if int(x["modelQuery"]["params"]["ddim_steps"]) < 1000]

#filtered_json_data_by_sampler_name = [x for x in filtered_json_data_by_ddim_steps if x["modelQuery"]["params"]["sampler_name"] == "lms"]	

#find correlations between dst_aesthetic_score and dst_similarity
dst_aesthetic_score = []
dst_similarity = []
for data in sorted_json_data_by_aesthetic_score:
	dst_aesthetic_score.append(float(data["scores"]["dst_aesthetic_score"]))
	dst_similarity.append(float(data["scores"]["dst_similarity"]))

#plt.scatter(dst_aesthetic_score, dst_similarity)
#plt.title("dst_aesthetic_score vs dst_similarity")
#plt.xlabel("dst_aesthetic_score")
#plt.ylabel("dst_similarity")
#plt.show()


#find correlations between aesthetic_score_difference and diff_similarity
aesthetic_score_difference = []
diff_similarity = []
for data in sorted_json_data_by_aesthetic_difference:
	aesthetic_score_difference.append(float(data["scores"]["aesthetic_score_difference"]))
	diff_similarity.append(float(data["scores"]["diff_similarity"]))

#plt.scatter(aesthetic_score_difference, diff_similarity)
#plt.title("aesthetic_score_difference vs diff_similarity")
#plt.xlabel("aesthetic_score_difference")
#plt.ylabel("diff_similarity")
#plt.show()




#find correlations between aesthetic_score_difference and cfg_scale, ddim_steps, and denoising_strength
dst_similarity = []
cfg_scale = []
ddim_steps = []
denoising_strength = []
for data in filtered_json_data_by_ddim_steps:
	dst_similarity.append(float(data["scores"]["dst_similarity"]))
	cfg_scale.append(float(data["modelQuery"]["params"]["cfg_scale"]))
	ddim_steps.append(float(data["modelQuery"]["params"]["ddim_steps"]))
	denoising_strength.append(float(data["modelQuery"]["params"]["denoising_strength"]))

print("diff_similarity vs cfg_scale")
print(np.corrcoef(dst_similarity, cfg_scale))
print("dst_aesthetic_score vs ddim_steps")
print(np.corrcoef(dst_similarity, ddim_steps))
print("dst_aesthetic_score vs denoising_strength")
print(np.corrcoef(dst_similarity, denoising_strength))
plt.show()

#predict the highest aesthetic_score_difference based on cfg_scale, ddim_steps, and denoising_strength
from sklearn import linear_model
from sklearn.metrics import mean_squared_error, r2_score

length = int(round(len(dst_similarity) / 2))

#split the data into training/testing sets

cfg_scale_train = cfg_scale[:length]
cfg_scale_test = cfg_scale[length:]

ddim_steps_train = ddim_steps[:length]
ddim_steps_test = ddim_steps[length:]

denoising_strength_train = denoising_strength[:length]
denoising_strength_test = denoising_strength[length:]

dst_similarity_train = dst_similarity[:length]
dst_similarity_test = dst_similarity[length:]

# Create linear regression object
regr = linear_model.LinearRegression()

# Train the model using the training sets
regr.fit(np.column_stack((cfg_scale_train, ddim_steps_train, denoising_strength_train)), dst_similarity_train)

# Make predictions using the testing set
dst_similarity_pred = regr.predict(np.column_stack((cfg_scale_test, ddim_steps_test, denoising_strength_test)))

# The coefficients
print('Coefficients: \n', regr.coef_)
# The mean squared error
print("Mean squared error: %.2f"

% mean_squared_error(dst_similarity_test, dst_similarity_pred))
# Explained variance score: 1 is perfect prediction
print('Variance score: %.2f' % r2_score(dst_similarity_test, dst_similarity_pred))

# Plot outputs in a 3d plot
fig = plt.figure()
ax = fig.add_subplot(111, projection='3d')
#ax.scatter(cfg_scale_test, ddim_steps_test, denoising_strength_test, c=diff_similarity_test)
ax.scatter(cfg_scale_test, ddim_steps_test, denoising_strength_test, c=dst_similarity_pred)
ax.set_xlabel('cfg_scale')
ax.set_ylabel('ddim_steps')
ax.set_zlabel('denoising_strength')
#set the color label to "dst_aesthetic_score"
m = plt.cm.ScalarMappable(cmap=plt.cm.jet)
m.set_array(dst_similarity_test)
#label the colorbar
plt.colorbar(m, label='dst_similarity')

plt.show()

# Plot outputs

with open('stats_data.json', "r") as f:
	stats_data = json.load(f)


stats = {}
stats["name"] = "dst_similarity"
stats["correlations"] = {}
stats["correlations"]["cfg_scale"] = str(np.corrcoef(dst_similarity, cfg_scale)[0][1])
stats["correlations"]["ddim_steps"] = str(np.corrcoef(dst_similarity, ddim_steps)[0][1])
stats["correlations"]["diff_similarity"] = str(np.corrcoef(dst_similarity, denoising_strength)[0][1])
stats["coefficients"] = str(regr.coef_)
stats["mean_squared_error"] = str(mean_squared_error(dst_similarity_test, dst_similarity_pred))
stats["variance_score"] = str(r2_score(dst_similarity_test, dst_similarity_pred))

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