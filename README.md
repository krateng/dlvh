Install with `pip install yeonji`

# borgsize

Lists sizes of all backups in a borg repository. Type `borgsize *repopath*`, e.g. `borgsize ~/myrepos/coolrepo`.

# flacco

Flacco is a simple tool for organizing CD rips from cdparanoia. It renames the flac files (or converts from wav files) and tags them with the desired title in one step. Type `flacco *num* *title*`, e.g. `flacco 1 "As If It's Your Last"`.

[AUR](https://aur.archlinux.org/packages/flacco/)

# fsclean

Clean unicode filenames in a directory tree. Use `--dryrun` to check what would be renamed. Existing files will not be overwritten.

# me2dlc

Installs ME2 DLCs from exe files on Linux using Steam Proton. Navigate to directory with files, then run `me2dlc`. Requires protontricks.

# ytd

Quickly downloads videos to predefined locations. Use `ytd *preset* *URL*` to download and `ytd --new *preset*` (in the target directory) to define new preset. You can specifiy additional options in configuration files in the target folder and all its parent folders.

# ytdlj

Merges any number of local files / youtube videos into a new file. Type `ytdlj *URLs/files* *outputname*`, e.g. `ytdlj party1.mkv ../party2.mkv https://www.youtube.com/watch?v=b3_lVSrPB6w fullvideo.mkv`.

# yttag

Download a video's audio and immediately id3-tag it according to command line arguments or supplied files. The script will look for `artist`,`albumartist`,`album` and `title` in `metadata.yml` files in this directory and up to three parent directories, but the command line flags will always have preference.
