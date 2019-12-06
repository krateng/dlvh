import sys
import os
import random
from send2trash import send2trash
from doreah.control import mainfunction


@mainfunction({},shield=True)
def main(*args):
	vids = args[0:-1]
	out = args[-1]

	assert not os.path.exists(out)

	files = []

	rand = random.randrange(100000000,999999999)
	rand = str(rand)

	i = 0
	for v in vids:
		if os.path.isfile(v):
			print(v,"is a file")
			files.append(v)
		else:
			print(v,"is not a file")
			filename = rand + "_" + str(i)
			cmd = "youtube-dl -o \"" + filename + ".%(ext)s\" --merge-output-format mkv " + v
			print("Command",cmd)
			assert 0 == os.system(cmd)
			files.append(filename + ".mkv")

		i += 1


	with open(rand + "_file.txt","w") as fil:
		fil.write("\n".join("file '" + f + "'" for f in files))

	assert 0 == os.system("ffmpeg -f concat -safe 0 -i " + rand + "_file.txt -c copy " + out)
	os.remove(rand + "_file.txt")

	for f in files:
		send2trash(f)
