import yaml
import os
import sys
from doreah.control import mainfunction
from . import DATA_DIR


DATA_DIR = os.path.join(DATA_DIR,"ytd")
settingsfile = os.path.join(DATA_DIR,"presets.yml")
configfiles = ["ytd.yml","ytd.yaml",".ytd"]
processname = "yt-dlp"

@mainfunction({'p':'preset','n':'new'},shield=True)
def main(url=None,preset=None,new=None):
	if new is None and url is not None:

		# no preset, dl here
		if preset is None:
			folder = os.getcwd()
			options = {}
			flags = []

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
			options = selected.get("options",{})
			flags = selected.get("flags",[])


		print("[ytd] Downloading to directory",folder)
		tmpfolder = folder
		print("[ytd] Reading local settings...")
		while True:
			for c in configfiles:
				local_configfile = os.path.join(tmpfolder,c)
				try:
					with open(local_configfile,"r") as f:
						localsettings = yaml.safe_load(f)


						# already loaded ones from lower directories take precedence
						if "options" in localsettings:
							loc_options = localsettings["options"]
							# adjust relative paths from settings file
							for o in loc_options:
								if isinstance(loc_options[o],str) and loc_options[o].startswith("^"):
									loc_options[o] = loc_options[o].replace("^",tmpfolder)
							options = {**loc_options,**options}
						if "flags" in localsettings:
							loc_flags = localsettings["flags"]
							flags += loc_flags



						print("[ytd]\t",local_configfile)
				except FileNotFoundError:
					pass

			if os.path.dirname(tmpfolder) != tmpfolder:
				tmpfolder = os.path.dirname(tmpfolder)
			else:
				break

		os.chdir(folder)


	#	print("The following options have been loaded from local configuration:")
	#	for o in options:
	#		print("   ",o)

		cmd_options = ["--" + k + " " + options[k] for k in options]
		cmd_flags = ["--" + k for k in flags]

		cmd = processname + " " + " ".join(cmd_options) + " " + " ".join(cmd_flags) + " " + url
		print("[ytd] Issuing command: " + cmd)
		os.system(cmd)

	elif new is not None:
		settings = {}
		path = os.getcwd()
		try:
			with open(settingsfile,"r") as f:
				settings = yaml.safe_load(f)
		except:
			settings = {}

		settings[new] = {"path":path,"options":{},"flags":[]}

		with open(settingsfile,"w") as f:
			yaml.dump(settings,f)

		print("Added current directory as preset",new)

	else:
		print("You need to specify --new to create a new preset!")


def create_bash_complete():

	pass
