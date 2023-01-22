import * as json from 'json';

var arg1, arg2, cfg_scale, data, ddim_steps, denoising_strength, dst_aesthetic_score, dst_similarity, dst_similarity_max, dst_similarity_min, dst_similarity_score, intercept_aesthetic_score, intercept_cfg_scale, intercept_ddim_steps, intercept_denoising_strength, intercepts, mod_similarity, mod_similarity_max, mod_similarity_min, mod_similarity_score, predicted_aesthetic_score, regr_aesthetic_score, regr_cfg_scale, regr_ddim_steps, regr_denoising_strength, regressions, t1, t2;
data = json.load(open("statsReport.json"));
regressions = data["regressions"];
intercepts = data["intercepts"];
intercept_aesthetic_score = intercepts["aesthetic_score"];
intercept_cfg_scale = intercepts["cfg_scale"];
intercept_denoising_strength = intercepts["denoising_strength"];
intercept_ddim_steps = intercepts["ddim_steps"];
regr_aesthetic_score = regressions["aesthetic_score"];
regr_cfg_scale = regressions["cfg_scale"];
regr_denoising_strength = regressions["denoising_strength"];
regr_ddim_steps = regressions["ddim_steps"];
dst_aesthetic_score = data["dst_aesthetic_score"];
cfg_scale = data["cfg_scale"];
ddim_steps = data["ddim_steps"];
denoising_strength = data["denoising_strength"];
dst_similarity = data["dst_similarity"];
mod_similarity = data["mod_similarity"];

if (sys.argv.length < 2) {
    console.log("Usage: python convertParameters.py <input_file>");
    sys.exit(1);
} else {
    arg1 = sys.argv[1];
    arg2 = sys.argv[2];
}

t1 = Number.parseFloat(arg1);
t2 = Number.parseFloat(arg2);
dst_similarity_min = dst_similarity["mean"] - dst_similarity["std"] * 2;
dst_similarity_max = dst_similarity["mean"] + dst_similarity["std"] * 2;
dst_similarity_score = (dst_similarity_max - dst_similarity_min) * Number.parseFloat(arg2) + dst_similarity_min;
mod_similarity_min = mod_similarity["mean"] - mod_similarity["std"] * 2;
mod_similarity_max = mod_similarity["mean"] + mod_similarity["std"] * 2;
mod_similarity_score = (mod_similarity_max - mod_similarity_min) * Number.parseFloat(arg2) + mod_similarity_min;
console.log("mod_similarity_score = ", mod_similarity_score);
console.log("dst_similarity_score = ", dst_similarity_score);
console.log(t1, t2);
regr_aesthetic_score = regr_aesthetic_score.replace("[", "");
regr_aesthetic_score = regr_aesthetic_score.replace("]", "");
regr_aesthetic_score = regr_aesthetic_score.split("  ");
console.log(regr_aesthetic_score);
predicted_aesthetic_score = Number.parseFloat(intercept_aesthetic_score) + Number.parseFloat(mod_similarity_score) * Number.parseFloat(regr_aesthetic_score[0]) + Number.parseFloat(dst_similarity_score) * Number.parseFloat(regr_aesthetic_score[1]);
console.log("predicted_aesthetic_score = ", predicted_aesthetic_score);