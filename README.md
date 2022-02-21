# dlvh

dlvh (**d**own**l**oad **v**ideo **h**ere) is a wrapper for [yt-dlp](https://github.com/yt-dlp/yt-dlp) that allows you to quickly download videos in a folder according to predefined nested local rules.

## How to use

Use `dlvh *URL*` to download to current folder, `dlvh -p *preset* *URL*` to download to a preset, and `dlvh -n *preset*` (in the target directory) to define new preset.

You can have dlvh configuration files on each level of the directory tree. These files use a simple yaml structure:

```yaml
options:
  download-archive: .ytdlarchive # Relative to the folder where the download happens
  cookies: ^/yt_cookies.txt # Relative to THIS configuration file, even in subfolders
  output: '"%(id)s.%(title)s.%(ext)s"' # Careful with quoting strings!
  merge-output-format: mkv
flags:
- restrict-filenames
- prefer-free-formats
```

Let's say you have the following folder structure:

```
├── audio  
│   ├── `dlvh.yml` # `extract-audio`  
│   ├── unsettling_screaming  
│   └── calm_nature_sounds  
└── video  
    ├── `dlvh.yml` # `embed-thumbnail`, `download-archive: .ytdlarchive`  
    ├── asmr  
    └── dance_covers  
        ├── `dlvh.yml` # `download-archive: ^ytdlarchive`  
        ├── twice  
        └── redvelvet  
```


When you download something to `audio/calm_nature_sounds`, the flag `extract-audio` from its parent folder will be respected.  
When you download something to `video/asmr`, the flag `embed-thumbnail` and the option `download-archive: .ytdlarchive` will be respected, meaning a local file `video/asmr/.ytdlarchive` will be used as archive.  
When you download something to `videos/dance_covers/twice` however, its parent folder's option `download-archive: ^ytdlarchive` overwrites this, meaning a common archive file `dance_covers/.ytdlarchive` will be used for all subfolders.
