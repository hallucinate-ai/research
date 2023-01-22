## import remove_stubs.py
import os
import sys
from removeStubs import removeStubs
## append the folder foo to the path
sys.path.append('improved-aesthetic-predictor')
#from batch_inference_aesthetics import processAesthetics
from join_json import processJson
#from add_clip_descriptions import processClip

def main():
	if len(sys.argv) < 2:
		print("Usage: python3 enhance.py [directory]")
		return
	dirname = sys.argv[1]
	#removeStubs(dirname)
	#processAesthetics(dirname)
	#processClip(dirname)
	processJson(dirname)
	print("done")

if __name__ == "__main__":
	main()