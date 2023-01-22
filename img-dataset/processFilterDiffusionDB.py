import os
import sys
import pandas as pd
import urllib.parse
import urllib.request
import shutil
import asyncio
import csv
import nest_asyncio
import json 
import subprocess

async def execute(command, args):
    # Create the subprocess; redirect the standard output into a pipe
    process = await asyncio.create_subprocess_exec(
        command, *args,
        stdout=asyncio.subprocess.PIPE,
        stderr=asyncio.subprocess.PIPE)

    # Read one line of output
    data = await process.stdout.readline()
    line = data.decode('utf-8').rstrip()

    # Wait for the subprocess exit
    await process.wait()
    if process.returncode != 0:
        error = await process.stderr.read()
        print ("error: " + str(error))
        #raise subprocess.CalledProcessError(process.returncode, args,
        #                                    output=data, stderr=error)
    return line

def aesthetics(cwd, output_dir, i):
    ## create file if not exists ##
    if not os.path.exists(cwd + "/diffusionDB-Aesthetics/data/aesthetics.json"):
        ## create the file ##
        aesthetics = {}
        ## write the file ##
        with open(cwd + "/diffusionDB-Aesthetics/data/aesthetics.json", 'w') as outfile:
            json.dump(aesthetics, outfile)
    ## open the aesthetic ratings json file ##
    with open(cwd + "/diffusionDB-Aesthetics/data/aesthetics.json") as json_file:
        aesthetics = json.load(json_file)
    command = "python3" 
    ## execute the command ##
    ## wait for the command to finish ##
    os.chdir(cwd + "/clip-aesthetic-prediction")
    args = [ "infer.py" , output_dir , "--batch-size", "32", "--output-file", cwd + "/diffusionDB-Aesthetics/data/output-" + str(i) + ".tsv"]
    #loop = asyncio.get_event_loop()
    #loop.run_until_complete(execute(command, args))
    #loop.close()
    results = subprocess.run([command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
    ## add each item from the tsv file to the json file ##
    with open(cwd + "/diffusionDB-Aesthetics/data/output-" + str(i) + ".tsv") as tsvfile:
        reader = csv.reader(tsvfile, delimiter='\t')
        rowNum = 0
        for row in reader:
            if rowNum > 0:
                if float(row[1]) > 6.5:
                    print ("row[0]: " + row[0] + " row[1]: " + row[1])
                    aesthetics[row[0]] = row[1]
                    if os.path.exists(output_dir + "/" + row[0]):
                        shutil.copy(output_dir + "/" + row[0], cwd + "/diffusionDB-Aesthetics/images/" + row[0])
                        print("copied: " + output_dir + "/" + row[0] + " to " + cwd + "/diffusionDB-Aesthetics/images/" + row[0])
            rowNum = rowNum + 1

    ## write the file ##
    with open(cwd + "/diffusionDB-Aesthetics/data/aesthetics.json", 'w') as outfile:
        json.dump(aesthetics, outfile)

    #os.remove(cwd + "/diffusionDB-Aesthetics/data/output-" + str(i) + ".tsv")
    os.chdir(cwd)
    return
    ## get the list of image names ##



async def main():
    cwd = os.path.dirname(os.path.realpath(__file__))
    thisFile = os.path.abspath(__file__)
    
    index = 0

    ## if the index file does not exist, create it ##
    if not os.path.exists(cwd + "/index"):
        ## create the file ##
        with open(cwd + "/index", 'w') as outfile:
            outfile.write(str(index))
            
    ## read the index file ##
    with open(cwd + "/index", 'r') as infile:
        index = int(infile.read())


    ## iterate through the folders ##
    for i in range(index, 14000):
        with open(cwd + "/index", 'r') as infile:
            index = int(infile.read())
        i = i + 1
        with open(cwd + "/index", 'w') as outfile:
            outfile.write(str(i))
        print("i: " + str(i))
        ## create the output directory if it does not exist ##
        output_dir = cwd + "/diffusionDBLarge/images/part-" + str(i)
        ## create the output directory if it does not exist ##
        if not os.path.exists(output_dir):
            os.makedirs(output_dir)
        os.chdir(output_dir)
        command = "python3" 
        args = [ cwd + "/download.py", "-l", "-i", str(i), "-r", str(i + 1), "-o", output_dir]
        ##loop = asyncio.get_event_loop()
        ##loop.run_until_complete(execute(command, args))
        results = subprocess.run([command, *args], stdout=subprocess.PIPE, stderr=subprocess.PIPE, shell=True)
        ## get files in the output directory ##
        os.chdir(cwd)
        files = os.listdir(output_dir)
        if len(files) > 0:
            for file in files:
                ## get the file extension ##
                fileExtension = os.path.splitext(file)[1]   
                if fileExtension == ".zip":
                    ## unzip the file ##
                    os.chdir(output_dir)
                    shutil.unpack_archive(output_dir + "/" + file, output_dir )
                    os.chdir(cwd)
                    ## delete the zip file ##
                    ## os.remove(output_dir + "/" + file)
        files = os.listdir(output_dir)
        if len(files) > 0:
            for file in files:
                ## get the file extension ##
                fileExtension = os.path.splitext(file)[1]
                if fileExtension == "json":
                    ## move the file to the json directory ##
                    print ("moving " + output_dir + "/" + file + " to " + cwd + "/diffusionDBLarge/data/" + file)
                    shutil.move(output_dir + "/" + file, cwd + "/diffusionDBLarge/data/" + file)
   
        print (command + " " +" ".join(args))
        aesthetics(cwd, output_dir, i)
        ## delete the output directory ##   
        shutil.rmtree(output_dir, ignore_errors=True)


if __name__ == "__main__":
    ## resolve a promise to run the main function ##
    asyncio.run(main())
    ##yield main()