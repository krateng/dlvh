import yaml
import os
import sys
from doreah.control import mainfunction
from . import DATA_DIR


DATA_DIR = os.path.join(DATA_DIR,"ytd")
settingsfile = os.path.join(DATA_DIR,"presets.yml")
configfiles = ["ytd.yaml","ytd.yml",".ytd"]

@mainfunction({},shield=True)
def main(preset=None,url=None,new=None):
	if new is None and preset is not None and url is not None:

		# no preset, dl here
		if preset == ".":
			folder = os.getcwd()
			options = []

		# preset
		else:
			with open(settingsfile,"r") as f:
				settings = yaml.safe_load(f)

			# abort if not existing
			if not preset in settings:
				print("Preset",preset,"undefined.")
				return


			selected = settings[preset]

			folder = selected["path"]
			options = selected["options"]


		print("Downloading to directory",folder)
		tmpfolder = folder
		while True:
			for c in configfiles:
				local_configfile = os.path.join(tmpfolder,c)
				try:
					with open(local_configfile,"r") as f:
						localsettings = yaml.safe_load(f)
						options += localsettings["options"]
						print("Reading settings from",local_configfile)
				except:
					pass

			if os.path.dirname(tmpfolder) != tmpfolder:
				tmpfolder = os.path.dirname(tmpfolder)
			else:
				break

		os.chdir(folder)
		os.system("youtube-dl " + " ".join(options) + " " + url)

	elif new is not None:
		settings = {}
		path = os.getcwd()
		try:
			with open(settingsfile,"r") as f:
				settings = yaml.safe_load(f)
		except:
			settings = {}

		settings[new] = {"path":path,"options":[]}

		with open(settingsfile,"w") as f:
			yaml.dump(settings,f)

		print("Added current directory as preset",new)

	else:
		print("You need to specify --new to create a new preset!")


def create_bash_complete():

	pass
