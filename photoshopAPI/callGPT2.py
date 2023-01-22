import os 
import sys
import openai
import json
## call GPT3 API
## fix the prompt token estimate ##
def GPT3(prompt):
	openai.api_key = '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'
	max_tokens = 512
	##calculate the number of tokens in the prompt
	prompt_tokens = len(prompt.split())
	response = openai.Completion.create(
	  model="text-davinci-003",
	  prompt=prompt,
	  temperature=0,
	  max_tokens=max_tokens,
	  top_p=1,
	  frequency_penalty=0,
	  presence_penalty=1,
	)
	return response

def main():
	## get the location of the current file ##
	this_file = os.path.abspath(__file__)
	## remove file name from this_file ##
	cwd = os.path.dirname(this_file)
	## import text file preprompt.txt into the variable preprompt ##
	preprompt = open(cwd +"/legalDoc.txt", "r").read()
	## ask for the prompt from the user ##
	##prompt = input("Please enter the instruction prompt: ")
	## call GPT3 API
	response = GPT3(preprompt)
	## write the response to output.txt
	with open(cwd +"/output.txt", "w") as text_file:
		text_file.write(response['choices'][0]['text'])

	print(response)

main()
