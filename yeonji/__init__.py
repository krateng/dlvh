
# local data
import os
try:
	DATA_DIR = os.environ["XDG_DATA_HOME"].split(":")[0]
	assert os.path.exists(DATA_DIR)
except:
	DATA_DIR = os.path.join(os.environ["HOME"],".local/share/")
DATA_DIR = os.path.join(DATA_DIR,"yeonji")
os.makedirs(DATA_DIR,exist_ok=True)

# package finder
import pkgutil, importlib, sys, inspect
modulenames = [modname for importer, modname, ispkg in pkgutil.iter_modules(__import__(__name__).__path__)]
modulenames = [m for m in modulenames if not m.startswith("_")]
#modules = {name:importlib.import_module("." + name,package=__name__) for name in modulenames}


# give packages their own directories
for m in modulenames:
#	mod = modules[m]
	dir = os.path.join(DATA_DIR,m)
	os.makedirs(dir,exist_ok=True)
	#print("assigning",dir,"to",mod)
	#mod.DATA_DIR = dir
	#sys.modules[__name__ + "." + m] = mod

#def datadir():
#	fr = inspect.stack()[1]
#	mod = inspect.getmodule(fr[0])
#	return os.path.join(DATA_DIR,mod.__name__)
