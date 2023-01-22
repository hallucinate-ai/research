import os
import sys
import pandas as pd
import urllib.parse
import urllib.request
import shutil
import asyncio
import aiohttp
import async_timeout
import nest_asyncio

async def download_images(urls, output_dir, max_pics=3000000, max_workers=100, timeout=5):
	## download the images from the URLs using the number of workers and timeout ##
	## the max_pics is the maximum number of images to download ##
	## the max_workers is the number of workers to use to download the images ##
	## the timeout is the time to wait for a response from the server ##


	## create the output directory if it does not exist ##
	this_file = os.path.abspath(__file__)
	## remove file name from this_file ##
	cwd = os.path.dirname(this_file)
	output_dir = cwd +"/aesthetics/data/images/"
	session = aiohttp.ClientSession()
	## download each item in the list of URLs ##
	async def download(url, session, output_dir):
		print ("Downloading images...")
		print ("url: " + str(url) + " output_dir: " + str(output_dir) + " max_pics: " + str(max_pics) + " max_workers: " + str(max_workers) + " timeout: " + str(timeout))	
		## get the file name from the URL ##
		filename = os.path.basename(urllib.parse.urlsplit(url).path)
		## create the full path to the file ##
		filepath = os.path.join(output_dir, filename)
		## if the file already exists, skip it ##
		if os.path.exists(filepath):
			return
		## download the file ##
		try:
			async with session.get(url, timeout=timeout) as response:
				with open(filepath, 'wb') as f:
					## write the image to the file ##
					img_raw = await response.read()
					f.write(img_raw)

		except Exception as e:
			print(e)
			return

	## download all the images in the list of URLs ##
	async def download_all(urls, output_dir, max_workers=32):
		## create the output directory if it does not exist ##
		if not os.path.exists(output_dir):
			os.makedirs(output_dir)
		## create the tasks to download the images ##
		tasks = []
		for url in urls:
			print("---TASKS-------------------------")
			print("url: " + str(url) + " output_dir: " + str(output_dir) + " max_pics: " + str(max_pics) + " max_workers: " + str(max_workers) + " timeout: " + str(timeout))
			task = asyncio.ensure_future(download(url, session, output_dir))

			tasks.append(task)
		## run the tasks concurrently ##
		await asyncio.gather(*tasks)

	## run the download_all function ##
	nest_asyncio.apply()
	loop = asyncio.get_event_loop()
	loop.run_until_complete(download_all(urls, output_dir, max_workers))

	## close the session ##
	await session.close()


		


def main():
	## get the location of the current file ##
	this_file = os.path.abspath(__file__)
	## remove file name from this_file ##
	cwd = os.path.dirname(this_file)
	## import a parquet file into the variable df ##
	df = pd.read_parquet(cwd +"/aesthetics/data/train-00000-of-00002-df9f00425d2c8694.parquet")
	## get every key URL from the parquet file ##
	urls = df['URL'].tolist()
	## break the list of URLs into chunks of 1000 ##
	for i in range(0, len(urls), 1000):	
		## get the chunk of URLs ##
		urls_chunk = urls[i:i + 1000]
		## use the fastest web crawling library to get the images from the URLs ##
		asyncio.run(download_images(urls_chunk, cwd +"/aesthetics/data/images/", max_pics=3000000, max_workers=100, timeout=10))
	
	df = pd.read_parquet(cwd +"/aesthetics/data/train-00001-of-00002-6f0b948a05090da1.parquet")
	## get every key URL from the parquet file ##
	urls = df['URL'].tolist()
	## break the list of URLs into chunks of 1000 ##
	for i in range(0, len(urls), 1000):	
		## get the chunk of URLs ##
		urls_chunk = urls[i:i + 1000]
		## use the fastest web crawling library to get the images from the URLs ##
		asyncio.run(download_images(urls_chunk, cwd +"/aesthetics/data/images/", max_pics=3000000, max_workers=100, timeout=10))




if __name__ == "__main__":
	## resolve a promise to run the main function ##
	##asyncio.run(main())
	main()