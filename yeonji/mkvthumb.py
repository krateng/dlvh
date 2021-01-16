from doreah.control import mainfunction
import os
import sys
import shutil
import glob
from send2trash import send2trash

import ffmpeg
import pymkv
from wand.image import Image

join = os.path.join

VIDEO_FORMATS = ['webm','mp4','avi']
THUMBNAIL_FORMATS = ['png','jpeg','jpg']
IMAGE_FORMATS = ['webp','bmp','tga','dds']


class Silence:
    def __enter__(self):
        self._original_stdout = sys.stdout
        sys.stdout = open(os.devnull, 'w')

    def __exit__(self, exc_type, exc_val, exc_tb):
        sys.stdout.close()
        sys.stdout = self._original_stdout


def handlefile(filename,ytdl=True):
	folder,file = os.path.split(filename)
	rawfile,ext = os.path.splitext(file)
	ext = ext[1:]


	# find thumbnail
	for iext in THUMBNAIL_FORMATS:
		thumbnailfilename = join(folder,rawfile + '.' + iext)
		if os.path.exists(thumbnailfilename):
			thumbnailtarget = join(folder,'cover.' + iext)
			assert not os.path.exists(thumbnailtarget)
			print("Using thumbnail",thumbnailfilename)
			shutil.copyfile(thumbnailfilename,thumbnailtarget)
			send2trash(thumbnailfilename)
			break
	else:
		for iext in IMAGE_FORMATS:
			thumbnailfilename = join(folder,rawfile + '.' + iext)
			if os.path.exists(thumbnailfilename):
				thumbnailtarget = join(folder,'cover.jpg')
				assert not os.path.exists(thumbnailtarget)
				print("Using thumbnail",thumbnailfilename)
				with Silence():
					i = Image(filename=thumbnailfilename)
					i.save(filename=thumbnailtarget)
				send2trash(thumbnailfilename)
				break

		else:
			if ytdl:
				possibleid = rawfile[-11:]
				thumbnailtarget = join(folder,rawfile + ".%(ext)s")
				os.system("youtube-dl --skip-download --write-thumbnail -o '" + thumbnailtarget + "' " + possibleid)
				return handlefile(filename,ytdl=False)
			else:
				print("No thumbnail found!")
				return False



	# convert video if necessary
	if ext.lower() in VIDEO_FORMATS:
		target = rawfile + ".mkv"
		print("Converting",file,"to",target)
		fullsource = join(folder,file)
		fulltarget = join(folder,target)
		with Silence():
			vid = ffmpeg.input(fullsource)
			out = ffmpeg.output(vid,fulltarget,c='copy')
			out.run()
		send2trash(fullsource)

		filename = fulltarget
		folder,file = os.path.split(filename)
		rawfile,ext = os.path.splitext(file)
		ext = ext[1:]

	elif ext.lower() == "mkv":
		pass

	else:
		print("Not a valid file!")
		return False




	with Silence():
		mkv = pymkv.MKVFile(filename)
		mkv.add_attachment(thumbnailtarget)
		mkv.mux(filename+'.tmp')
	send2trash(thumbnailtarget)
	send2trash(filename)
	shutil.move(filename+'.tmp',filename)
	#os.system("mkvmerge -o " + join(folder,target + ".tmp")

@mainfunction({},shield=True)
def main(path):
	if os.path.isfile(path):
		return handlefile(path)
	elif os.path.isdir(path):
		for f in os.listdir(path):
			fname = join(path,f)
			if os.path.isfile(fname) and fname.split('.')[-1].lower() in VIDEO_FORMATS+['mkv']:
				handlefile(fname)
