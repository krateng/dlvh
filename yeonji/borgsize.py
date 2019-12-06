import sys
import os
import re
import tabulate
from doreah.control import mainfunction

@mainfunction({},shield=True)
def main(*args):

	repo = args[0]

	archivelist = os.popen("borg list " + repo).read()

	archives = archivelist.split("\n")[:-1]
	archives = [a.split() for a in archives]
	archivenames = [a[0] for a in archives]

	sizes = []
	for a in archivenames:
		print("Analyzing archive",a)
		info = os.popen("borg info " + repo + "::" + a).read()
		info = info.split("\n")
		info = [line for line in info if line.startswith("This archive:")][0]
		_, origsize, compressedsize, dedupsize = re.split(r'\s{2,}', info)
		sizes.append([a,origsize,compressedsize,dedupsize])

	print(tabulate.tabulate(sizes,headers=["Archive","Original Size","Compressed Size","Deduplicated Size"]))
