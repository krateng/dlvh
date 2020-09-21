import yaml
import os
import sys
from doreah.control import mainfunction
from . import DATA_DIR


DATA_DIR = os.path.join(DATA_DIR,"ytd")
settingsfile = os.path.join(DATA_DIR,"presets.yml")

@mainfunction({},shield=True)
def main(preset=None,url=None,new=None):
	if new is None and preset is not None and url is not None:
		with open(settingsfile,"r") as f:
			settings = yaml.safe_load(f)

		if preset in settings:
			selected = settings[preset]
			print("Downloading to directory",selected["path"])
			os.chdir(selected["path"])
			os.system("youtube-dl " + url)
		else:
			print("Preset",preset,"undefined.")
	elif new is not None:
		settings = {}
		path = os.getcwd()
		with open(settingsfile,"r") as f:
			settings = yaml.safe_load(f)

		settings[new] = {"path":path}

		with open(settingsfile,"w") as f:
			yaml.dump(settings,f)

		print("Added current directory as preset",new)

	else:
		print("You need to specify --new to create a new preset!")


def create_bash_complete():

	pass
