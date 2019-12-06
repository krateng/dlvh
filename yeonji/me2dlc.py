import os
import shutil
from doreah.control import mainfunction

@mainfunction({},shield=True)
def main():
	STEAMDIR = "~/.steam/steam/steamapps/common/Mass Effect 2"
	APPID = 24980

	tempdir = os.path.join(os.path.expanduser(STEAMDIR),"dlc_installers")
	os.makedirs(tempdir)

	for f in os.listdir("."):
		if f.endswith(".exe"):
			shutil.copy(f,tempdir)

			os.system("protontricks -c 'wine ./dlc_installers/" + f + "' " + str(APPID))
