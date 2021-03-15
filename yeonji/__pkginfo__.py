from . import modulenames

name = "yeonji"
author = {
	"name":"Johannes Krattenmacher",
	"email":"yeonji@dev.krateng.ch",
	"github":"krateng"
}
desc = "Collection of command line tools"
version = 0,6,4


requires = [
	"tabulate",
	"send2trash",
	"doreah>=1.6.11",
	"unidecode",
	"emoji"
]

resources = [
]



commands = {
	mod:mod + ":main"
	for mod in modulenames
}
