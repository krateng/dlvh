# ytd

ytd is a wrapper for yt-dlp that allows you to quickly download videos in a folder according to predefined nested local rules.

## How to use

Use `ytd *URL*` to download to current folder, `ytd -p *preset* *URL*` to download to a preset, and `ytd -n *preset*` (in the target directory) to define new preset.

You can have ytd configuration files on each level of the directory tree. These files use a simple yaml structure:

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

├── audio
│   ├── `ytd.yml` # `extract-audio`
│   ├── unsettling_screaming
│   └── calm_nature_sounds
└── video
    ├── `ytd.yml` # `embed-thumbnail`, `download-archive: .ytdlarchive`
    ├── asmr
    └── dance_covers
        ├── `ytd.yml` # `download-archive: ^ytdlarchive`
        ├── twice
        └── redvelvet

When you download something to `audio/calm_nature_sounds`, the flag `extract-audio` from its parent folder will be respected.
When you download something to `video/asmr`, the flag `embed-thumbnail` and the option `download-archive: .ytdlarchive` will be respected, meaning a local file `.ytdlarchive` will be used as archive.
When you download something to `videos/dance_covers/twice` however, its parent folder's option `download-archive: ^ytdlarchive` overwrites this, meaning a common archive file in the `dance_covers` folder will be used for all subfolders.
