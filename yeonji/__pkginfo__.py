from . import modulenames

name = "yeonji"
author = {
	"name":"Johannes Krattenmacher",
	"email":"python@krateng.dev",
	"github":"krateng"
}
desc = "Collection of command line tools"
version = 0,5,5


requires = [
	"tabulate",
	"send2trash",
	"doreah>=1.6.11"
]

resources = [
]



commands = {
	mod:mod + ":main"
	for mod in modulenames
}
