var scikit = require('scikit-learn')
var json = require("json")
var fs = require("fs")
var readablestream = require("readable-stream")
var math = require('mathjs')
var ml = require('machine_learning')


// crete a linear regression model
var regr1 = new scikit.linear_model.LinearRegression()
var regr2 = ml.regression.linear_regression({
    data: [
        [0, 0],
        [1, 1],
        [2, 2]
    ],
    label: [0, 1, 2],
    n_in: 1,
    n_out: 1
});


function load_json_samples(file) {
    let json = fs.readFileSync(file)
    let samples = JSON.parse(json)
    return samples
}

function prepare_data() {
    let samples = load_json_samples('samples_img2img.json')
        //filter samples list where sameple['scores']['ddim_steps'] < 1000
    let filter_json_data_by_ddim_steps = samples.filter(sample => sample['modelQuery']['params']['ddim_steps'] < 1000)
    let filter_json_data_by_aesthetic_score = filter_json_data_by_ddim_steps.filter(sample => sample["scores"]["dst_aesthetic_score"] > 5.0)
    let filter_json_data_by_dst_similarity = filter_json_data_by_aesthetic_score.filter(sample => sample["scores"]["dst_similarity"] > 6.5)
    let filtered_data = filter_json_data_by_dst_similarity

    let dst_aesthetic_score = []
    let cfg_scale = []
    let ddim_steps = []
    let denoising_strength = []
    let mod_similarity = []
    let dst_similarity = []
    let diff_similarity = []
    let src_similarity = []
    let src_aesthetic_score = []
    let diff_aesthetic_score = []

    for (let i = 0; i < filtered_data.length; i++) {
        // convert to float
        dst_aesthetic_score.push(parseFloat(filtered_data[i]["scores"]["dst_aesthetic_score"]))
        dst_aesthetic_score.push(parseFloat(filtered_data[i]["scores"]["dst_aesthetic_score"]))
        cfg_scale.push(parseFloat(filtered_data[i]["modelQuery"]["params"]["cfg_scale"]))
        ddim_steps.push(parseFloat(filtered_data[i]["modelQuery"]["params"]["ddim_steps"]))
        denoising_strength.push(parseFloat(filtered_data[i]["modelQuery"]["params"]["denoising_strength"]))
        mod_similarity.push(parseFloat(filtered_data[i]["scores"]["mod_similiarity"]))
        dst_similarity.push(parseFloat(filtered_data[i]["scores"]["dst_similarity"]))
        diff_similarity.push(parseFloat(filtered_data[i]["scores"]["diff_similarity"]))
        dst_aesthetic_score.push(parseFloat(filtered_data[i]["scores"]["dst_aesthetic_score"]))
        src_similarity.push(parseFloat(filtered_data[i]["scores"]["src_similarity"]))
        src_aesthetic_score.push(parseFloat(filtered_data[i]["scores"]["src_aesthetic_score"]))
        diff_aesthetic_score.push(parseFloat(filtered_data[i]["scores"]["diff_aesthetic_score"]))
    }

    let std_cfg_scale = math.std(cfg_scale)
    let std_ddim_steps = math.std(ddim_steps)
    let std_denoising_strength = math.std(denoising_strength)
    let std_mod_similarity = math.std(mod_similarity)
    let std_dst_similarity = math.std(dst_similarity)
    let std_diff_similarity = math.std(diff_similarity)
    let std_dst_aesthetic_score = math.std(dst_aesthetic_score)
    let std_src_similarity = math.std(src_similarity)
    let std_src_aesthetic_score = math.std(src_aesthetic_score)
    let std_diff_aesthetic_score = math.std(diff_aesthetic_score)
    let mean_cfg_scale = math.mean(cfg_scale)
    let mean_ddim_steps = math.mean(ddim_steps)
    let mean_denoising_strength = math.mean(denoising_strength)
    let mean_mod_similarity = math.mean(mod_similarity)
    let mean_dst_similarity = math.mean(dst_similarity)
    let mean_diff_similarity = math.mean(diff_similarity)
    let mean_dst_aesthetic_score = math.mean(dst_aesthetic_score)
    let mean_src_similarity = math.mean(src_similarity)
    let mean_src_aesthetic_score = math.mean(src_aesthetic_score)
    let mean_diff_aesthetic_score = math.mean(diff_aesthetic_score)

    dst_aesthetic_score = []
    cfg_scale = []
    ddim_steps = []
    denoising_strength = []
    mod_similiarity = []
    dst_similarity = []
    diff_similarity = []
    src_similarity = []
    src_aesthetic_score = []
    diff_aesthetic_score = []

    for (let i = 0; i < filtered_data.length; i++) {
        // if dst_aesthetic score is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["dst_aesthetic_score"] > mean_dst_aesthetic_score + 2 * std_dst_aesthetic_score || filtered_data[i]["scores"]["dst_aesthetic_score"] < mean_dst_aesthetic_score - 2 * std_dst_aesthetic_score) {
            continue
        }
        // if ddim_steps is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["modelQuery"]["params"]["ddim_steps"] > mean_ddim_steps + 2 * std_ddim_steps || filtered_data[i]["modelQuery"]["params"]["ddim_steps"] < mean_ddim_steps - 2 * std_ddim_steps) {
            continue
        }
        // if denoising_strength is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["modelQuery"]["params"]["denoising_strength"] > mean_denoising_strength + 2 * std_denoising_strength || filtered_data[i]["modelQuery"]["params"]["denoising_strength"] < mean_denoising_strength - 2 * std_denoising_strength) {
            continue
        }
        // if cfg_scale is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["modelQuery"]["params"]["cfg_scale"] > mean_cfg_scale + 2 * std_cfg_scale || filtered_data[i]["modelQuery"]["params"]["cfg_scale"] < mean_cfg_scale - 2 * std_cfg_scale) {
            continue
        }
        // if mod_similarity is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["mod_similiarity"] > mean_mod_similarity + 2 * std_mod_similarity || filtered_data[i]["scores"]["mod_similiarity"] < mean_mod_similarity - 2 * std_mod_similarity) {
            continue
        }
        // if dst_similarity is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["dst_similarity"] > mean_dst_similarity + 2 * std_dst_similarity || filtered_data[i]["scores"]["dst_similarity"] < mean_dst_similarity - 2 * std_dst_similarity) {
            continue
        }
        // if diff_similarity is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["diff_similarity"] > mean_diff_similarity + 2 * std_diff_similarity || filtered_data[i]["scores"]["diff_similarity"] < mean_diff_similarity - 2 * std_diff_similarity) {
            continue
        }
        // if src_similarity is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["src_similarity"] > mean_src_similarity + 2 * std_src_similarity || filtered_data[i]["scores"]["src_similarity"] < mean_src_similarity - 2 * std_src_similarity) {
            continue
        }
        // if src_aesthetic_score is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["src_aesthetic_score"] > mean_src_aesthetic_score + 2 * std_src_aesthetic_score || filtered_data[i]["scores"]["src_aesthetic_score"] < mean_src_aesthetic_score - 2 * std_src_aesthetic_score) {
            continue
        }
        // if diff_aesthetic_score is greater or less than 2 standard deviations from the mean, then skip
        if (filtered_data[i]["scores"]["diff_aesthetic_score"] > mean_diff_aesthetic_score + 2 * std_diff_aesthetic_score || filtered_data[i]["scores"]["diff_aesthetic_score"] < mean_diff_aesthetic_score - 2 * std_diff_aesthetic_score) {
            continue
        }

        dst_aesthetic_score.push(filtered_data[i]["scores"]["dst_aesthetic_score"])
        cfg_scale.push(filtered_data[i]["modelQuery"]["params"]["cfg_scale"])
        ddim_steps.push(filtered_data[i]["modelQuery"]["params"]["ddim_steps"])
        denoising_strength.push(filtered_data[i]["modelQuery"]["params"]["denoising_strength"])
        mod_similiarity.push(filtered_data[i]["scores"]["mod_similiarity"])
        dst_similarity.push(filtered_data[i]["scores"]["dst_similarity"])
        diff_similarity.push(filtered_data[i]["scores"]["diff_similarity"])
        src_similarity.push(filtered_data[i]["scores"]["src_similarity"])
        src_aesthetic_score.push(filtered_data[i]["scores"]["src_aesthetic_score"])
        diff_aesthetic_score.push(filtered_data[i]["scores"]["diff_aesthetic_score"])
    }

    // put every list into a dictionary
    let data = {
        "dst_aesthetic_score": dst_aesthetic_score,
        "cfg_scale": cfg_scale,
        "ddim_steps": ddim_steps,
        "denoising_strength": denoising_strength,
        "mod_similiarity": mod_similiarity,
        "dst_similarity": dst_similarity,
        "diff_similarity": diff_similarity,
        "src_similarity": src_similarity,
        "src_aesthetic_score": src_aesthetic_score,
        "diff_aesthetic_score": diff_aesthetic_score
    }
    return data
}

function process_samples(samples) {
    let prepared_data = prepare_data()
    let length = prepared_data["dst_aesthetic_score"].length / 2

    dst_aesthetic_score_train = prepared_data["dst_aesthetic_score"].slice(0, length)
    dst_aesthetic_score_test = prepared_data["dst_aesthetic_score"].slice(length, prepared_data["dst_aesthetic_score"].length)
    cfg_scale_train = prepared_data["cfg_scale"].slice(0, length)
    cfg_scale_test = prepared_data["cfg_scale"].slice(length, prepared_data["cfg_scale"].length)
    ddim_steps_train = prepared_data["ddim_steps"].slice(0, length)
    ddim_steps_test = prepared_data["ddim_steps"].slice(length, prepared_data["ddim_steps"].length)
    denoising_strength_train = prepared_data["denoising_strength"].slice(0, length)
    denoising_strength_test = prepared_data["denoising_strength"].slice(length, prepared_data["denoising_strength"].length)
    mod_similiarity_train = prepared_data["mod_similiarity"].slice(0, length)
    mod_similiarity_test = prepared_data["mod_similiarity"].slice(length, prepared_data["mod_similiarity"].length)
    dst_similarity_train = prepared_data["dst_similarity"].slice(0, length)
    dst_similarity_test = prepared_data["dst_similarity"].slice(length, prepared_data["dst_similarity"].length)
    diff_similarity_train = prepared_data["diff_similarity"].slice(0, length)
    diff_similarity_test = prepared_data["diff_similarity"].slice(length, prepared_data["diff_similarity"].length)
    src_similarity_train = prepared_data["src_similarity"].slice(0, length)
    src_similarity_test = prepared_data["src_similarity"].slice(length, prepared_data["src_similarity"].length)
    src_aesthetic_score_train = prepared_data["src_aesthetic_score"].slice(0, length)
    src_aesthetic_score_test = prepared_data["src_aesthetic_score"].slice(length, prepared_data["src_aesthetic_score"].length)
    diff_aesthetic_score_train = prepared_data["diff_aesthetic_score"].slice(0, length)
    diff_aesthetic_score_test = prepared_data["diff_aesthetic_score"].slice(length, prepared_data["diff_aesthetic_score"].length)

    regr1.fit(cfg_scale_train, dst_aesthetic_score_train)
    regr2.fit(ddim_steps_train, dst_aesthetic_score_train)
    regr3.fit(denoising_strength_train, dst_aesthetic_score_train)
    regr4.fit(mod_similiarity_train, dst_aesthetic_score_train)

    // put the regression models into a list
    //let models = [regr1, regr2, regr3, regr4]
    //return (models)
}

function predict(arg1, arg2) {
    let prepared_data = prepare_data()
    let dst_similarity = prepared_data["dst_similarity"]
    let mod_similarity = prepared_data["mod_similarity"]
        //convert dst_aesthetic_score and mod_similarity to normalized vectors
    let mod_similarity_normalized = mod_similarity.map(x => (x - Math.min(...mod_similarity)) / (Math.max(...mod_similarity) - Math.min(...mod_similarity)))
    let dst_similarity_normalized = dst_similarity.map(x => (x - Math.min(...dst_similarity)) / (Math.max(...dst_similarity) - Math.min(...dst_similarity)))
    let selected_mod_similarity = mod_similarity_normalized[arg2]
    let selected_dst_similarity = dst_similarity_normalized[arg1]

    console.log(selected_dst_similarity)
    console.log(selected_mod_similarity)
}

console.log(predict(1, 1))