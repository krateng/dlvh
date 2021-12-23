from . import modulenames

commands = {
	mod:mod + ":main"
	for mod in modulenames
}
