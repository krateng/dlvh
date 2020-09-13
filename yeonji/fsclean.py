import os
import re
import emoji
import string
import unidecode
from doreah.io import col
from doreah.control import mainfunction

import yaml
import datetime

nowstr = datetime.datetime.now().strftime("%Y-%m-%d-%H-%M-%S")

customreplace = {
	"ä":"ae",
	"ü":"ue",
	"ö":"oe",
	"Ä":"AE",
	"Ü":"UE",
	"Ö":"OE"
}

# LEVELS
# 1 - Remove Emojis, because they are a crime against God
# 2 - ASCIIfy, transliterate different alphabets etc
# 3 - Remove whitespaces
# 4 - Lower Case everything
#


def cleanf(name,level):
	name = " ".join(name.split())
	name = "".join(customreplace[char] if char in customreplace else char for char in name)
	if level == 1:
		# get rid of emojis, automatically included in asciifying
		name = emoji.get_emoji_regexp().sub('',name)
		name = " ".join(name.split())
	if level > 1:
		# asciify
		name = unidecode.unidecode(name)
		name = name.replace("/","-")
		# replace all whitespaces with normal one (and collapse multiple into one)
		name = " ".join(name.split())
	if level > 2:
		name = name.replace(" ","_")
	if level > 3:
		name = name.lower()

	name = name.strip()
	assert name != ""
	return name


@mainfunction({},flags=["dryrun","save_log"],shield=True)
def main(rootpath,level=3,dryrun=False,save_log=False):
	found,changed = 0,0
	renamed = []
	for root, dirs, files in os.walk(rootpath,topdown=False):
		for f in files+dirs:
			found += 1
			fc = cleanf(f,level=level)
			oldname = os.path.join(root,f)
			newname = os.path.join(root,fc)
			if fc != f:
				changed += 1
				print(col["red"](oldname))
				print(col["green"](newname))
				renamed.append({"original":oldname,"new":newname})
				if not dryrun:
					if os.path.exists(newname):
						print(newname,"already exists!")
					else:
						os.rename(oldname,newname)

	print("Renamed",changed,"of",found,"files.")
	if save_log:
		with open("rename_" + nowstr + ".yml","w") as log:
			yaml.dump(renamed,log)
