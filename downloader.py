import requests
import json
from urllib.parse import unquote
import sys
import re
from dotenv import load_dotenv
import os
import glob
import colorama
import subprocess

TARGET_API = "https://api.modrinth.com/v2"
TARGET_PATH = os.getenv('APPDATA') + "\\.minecraft\\mods\\"
MODS = ["sodium", "lithium", "iris", "lambdynamiclights", "sodium-extra", "fabric-api"]

class ModirinthApiClient:
	def __init__(self, token, version):
		self.version = version
		self.token = token

	def _parse_json(self, req) -> dict:
		"""
			private parses the json response of the modirinth api
		"""
		loaded = json.loads(req.text)
		target = {}
		for i in loaded:
			if self.version in i["game_versions"]:
				target = i
				break
		if not target:
			raise Exception("version not found")
		return unquote(target["files"][0]["url"])

	def get_link(self, mod_name) -> str:
		"""
			public returns the link of the target mod
		"""
		headers = {
			"Authorization": self.token
		}
		req = requests.get(TARGET_API + f"/project/{mod_name}/version", headers=headers)
		if req.status_code != 200:
			raise Exception("couldn't find %s" % mod_name)
		return self._parse_json(req)

def validate_version(version) -> bool:
	pattern = r'^\d+\.\d+(\.\d+)?$'
	return bool(re.search(pattern, version))


def download_file(url, path):
	"""
		download file from url
	"""
	local_filename = url.split('/')[-1]
	# NOTE the stream=True parameter below
	with requests.get(url, stream=True) as r:
		r.raise_for_status()
		with open(path + local_filename, 'wb') as f:
			for chunk in r.iter_content(chunk_size=8192): 
				# If you have chunk encoded response uncomment if
				# and set chunk_size parameter to None.
				#if chunk: 
				f.write(chunk)
	return local_filename

def clean_mods_folder():
	user_input = input(colorama.Fore.CYAN + "delete mod folder? [Y/N]" + colorama.Fore.RESET)
	if user_input == 'Y' or user_input == 'y':
		files = glob.glob(TARGET_PATH + "*")
		for f in files:
			os.remove(f)
	else:
		pass

def main():
	if len(sys.argv) < 2:
		print("usage: python downloader.py <mc_version>")
		sys.exit(1)
	colorama.init()
	load_dotenv()
	clean_mods_folder()
	TOKEN = os.getenv("TOKEN")
	version = sys.argv[1]
	links = []
	if not validate_version(version):
		raise ValueError("Invalid version")
	client = ModirinthApiClient(TOKEN, version)
	for i in MODS:
		links.append(client.get_link(i))
	for i in links:
		download_file(i, TARGET_PATH)
		print("["+ colorama.Fore.GREEN + "+" + colorama.Fore.RESET + "] downloaded " + i)
    

if __name__ == '__main__':
	main()