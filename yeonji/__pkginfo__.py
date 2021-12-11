from . import modulenames

name = "yeonji"
author = {
	"name":"Johannes Krattenmacher",
	"email":"yeonji@dev.krateng.ch",
	"github":"krateng"
}
desc = "Collection of command line tools"
version = 0,7,1


requires = [
	"tabulate",
	"send2trash",
	"doreah>=1.6.11",
	"unidecode",
	"emoji",
	"yt-dlp"
]

resources = [
]



commands = {
	mod:mod + ":main"
	for mod in modulenames
}
