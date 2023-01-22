import os 
import sys
import json

cwd = os.path.dirname(os.path.abspath(__file__))
## open commandList.json ##
with open(cwd + "/template.json", "r") as f:
	commandList = json.load(f)

commandListKeys= list(commandList.keys())

lines = []
lines.append("//HALLUCINATE APP INTEGRATION FOR PHOTOSHOP API FUNCTIONS")
lines.append("//GPT3 will generate the code from the functions below")

function_text = []
for key in commandListKeys:
	print(key)
	print(commandList[key])
	## string length of comments ##
	commentlen = len(commandList[key]["comments"])
	if commentlen > 0:
		kwargs = commandList[key]["kwargs"]
		emits = commandList[key]["emits"]
		comments = commandList[key]["comments"]
		kwarg_keys = list(kwargs.keys())
		kwargs_string = '' 
		for keys in kwarg_keys:
			kwargs_string = kwargs_string + keys + ', '
		kwargs_string = kwargs_string[:-2]
		function_text = []
		function_text.append("function " + key + "(" + kwargs_string + "){\n")
		for comment in comments:
			function_text.append("  //" + comment + "\n")
		function_text.append("  let emits = {}\n")
		function_text.append("  return (emits)\n")
		function_text.append("}\n")
		function_text.append("\n")
		## concatenate the lines of the function ##
		lines = lines + function_text

## write the list of lines to a file ##
print("linecount: " + str(len(lines)))

## delete the file if it exists ##
filename = cwd + "/gptFunctions.txt"
if os.path.exists(filename):
	os.remove(filename)
with open(filename, "w+") as f:
	f.writelines(lines)                          


lines = []
lines.append("//HALLUCINATE APP INTEGRATION FOR PHOTOSHOP API FUNCTIONS \n")
lines.append("//Photoshop plugin code will be generated from the functions below \n")
function_text = []
for key in commandListKeys:
	print(key)
	print(commandList[key])
	## string length of comments ##
	#emits = json.dumps(emits)
	commentlen = len(commandList[key]["comments"])
	emitslen = len(commandList[key]["emits"])
	if emitslen > 0:
		kwargs = commandList[key]["kwargs"]
		emits = commandList[key]["emits"]
		emits = json.dumps(emits)
		comments = commandList[key]["comments"]
		kwarg_keys = list(kwargs.keys())
		kwargs_string = '' 
		for keys in kwarg_keys:
			kwargs_string = kwargs_string + keys + ', '
		kwargs_string = kwargs_string[:-2]
		for arg in kwarg_keys:
			emits = emits.replace('"' + arg + '"', arg)
		function_text = []
		function_text.append("function " + key + "(" + kwargs_string + "){\n")
		for comment in comments:
			function_text.append("  //" + comment + "\n")
		function_text.append('  let emits = {}\n')
		function_text.append("  emits =  + JSON.parse\""+ emits +"\")\n")
		function_text.append("  return (emits)\n")
		function_text.append("}\n")
		function_text.append("\n")
		## concatenate the lines of the function ##
		lines = lines + function_text

filename = cwd + "/pluginFunctions.txt"
if os.path.exists(filename):
	os.remove(filename)
with open(filename, "w+") as f:
	f.writelines(lines)
## write the list of lines to a file ##
                         
