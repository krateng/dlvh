import yaml
import os
import sys
from doreah.control import mainfunction
from . import DATA_DIR


DATA_DIR = os.path.join(DATA_DIR,"ytd")
settingsfile = os.path.join(DATA_DIR,"presets.yml")

@mainfunction({})
def main(preset=None,url=None,new=None,path=None):
	if new is None and path is None:
		with open(settingsfile,"r") as f:
			settings = yaml.safe_load(f)

		selected = settings[preset]
		os.chdir(selected["path"])
		os.system("youtube-dl " + url)
	elif new is not None and path is not None:
		settings = {}
		with open(settingsfile,"r") as f:
			settings = yaml.safe_load(f)
			print(settings)

		settings[new] = {"path":path}

		with open(settingsfile,"w") as f:
			yaml.dump(settings,f)

	else:
		print("You need to specify --new and --path to create a new preset!")
