import yaml
import os
import sys
import subprocess


from doreah.control import mainfunction
from doreah.io import col
from appdirs import user_config_dir


settingsfile = os.path.join(user_config_dir('dlvh'),"presets.yml")
configfiles = ["dlvh.yml","dlvh.yaml",".dlvh","ytd.yml","ytd.yaml",".ytd"]
processname = "yt-dlp"


def download_vid(url,additionals,preset):

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


	print("[dlvh] Downloading to directory",folder)

	# Go up the dir tree for all config files
	tmpfolder = folder
	print("[dlvh] Reading local settings...")
	while True:
		for c in configfiles:
			local_configfile = os.path.join(tmpfolder,c)
			try:
				with open(local_configfile,"r") as f:
					localsettings = yaml.safe_load(f)



					if "options" in localsettings:
						loc_options = localsettings["options"]
						# adjust relative paths from settings file
						for o in loc_options:
							if isinstance(loc_options[o],str) and loc_options[o].startswith("^"):
								loc_options[o] = loc_options[o].replace("^",tmpfolder)

						# already loaded ones from lower directories or presets take precedence
						options = {**loc_options,**options}

					if "flags" in localsettings:
						loc_flags = localsettings["flags"]
						flags += loc_flags

					print(f"[dlvh]\t{local_configfile}")


			except FileNotFoundError:
				pass

		if os.path.dirname(tmpfolder) != tmpfolder:
			tmpfolder = os.path.dirname(tmpfolder)
		else:
			# reached filesystem root
			break

	# go back to where we actually want to be
	os.chdir(folder)

	# add command-supplied options
	options = {**options,**additionals}

	print("[dlvh] The following options have been loaded:")
	for o in options:
		print("\t",col['magenta'](o),options[o])
	for f in flags:
		print("\t",col['magenta'](f))

	cmd_options = [item for pair in [(f"--{k}",v) for k,v in options.items()] for item in pair] # what
	cmd_flags = ["--" + k for k in flags]

	print("[dlvh] Issuing command")
	subprocess.run([processname] + cmd_options + cmd_flags + [url])


# TODO: yt-dlp flags must all be specifed manually?
@mainfunction({'p':'preset','n':'new'},shield=True)
def main(url=None,preset=None,new=None,**additionals):

	# download video
	if new is None and url is not None:
		download_vid(url,additionals,preset=preset)

	# create new preset
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

	# invalid
	else:
		print("You need to specify --new to create a new preset!")
