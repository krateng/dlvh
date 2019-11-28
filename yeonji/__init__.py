name = "yeonji"
author = {
	"name":"Johannes Krattenmacher",
	"email":"python@krateng.dev",
	"github":"krateng"
}
desc = "Collection of command line tools"
version = 0,3

import pkgutil, importlib, sys
modulenames = [modname for importer, modname, ispkg in pkgutil.iter_modules(__import__(__name__).__path__)]
modules = [importlib.import_module("." + name,package=__name__) for name in modulenames]


requires = [
	"tabulate",
	"send2trash"
]

resources = [
]



commands = {
	mod:mod + ":main"
	for mod in modulenames
}
