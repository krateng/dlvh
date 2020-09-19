import os
import yaml
from doreah.control import mainfunction



@mainfunction({},shield=True)
def main(url,**meta):
	vidid = url[-11:]

	metadata = {}
	for folder in ("../..","..","."):
		metadatafile = os.path.join(folder,"metadata.yml")
		if os.path.exists(metadatafile):
			with open(metadatafile) as yamlfile:
				metadata.update(yaml.safe_load(yamlfile))
	metadata.update(meta)


	os.system("youtube-dl --extract-audio --audio-format mp3 " + url)
	os.system('id3v2 *{vidid}* --song "{title}" --artist "{artist}" --album "{album}" --TPE2 "{albumartist}"'.format(vidid=vidid,**metadata))
