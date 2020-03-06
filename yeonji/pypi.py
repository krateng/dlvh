import setuptools
import importlib
import sys
import os
import shutil
import glob
from doreah.control import mainfunction

@mainfunction({},shield=True)
def main(packagename):

	assert os.path.exists(packagename)
	sys.argv = (sys.argv[0],"sdist","bdist_wheel")

	module = importlib.import_module(packagename)
	pkginfo = importlib.import_module(".__pkginfo__",package=packagename)
	pkginfo = pkginfo.__dict__

	# extract info

	with open("README.md", "r") as fh:
	    long_description = fh.read()

	setuptools.setup(
	    name=pkginfo.get("links",{}).get("pypi") or pkginfo["name"],
	    version=".".join(str(n) for n in pkginfo["version"]),
	    author=pkginfo["author"]["name"],
	    author_email=pkginfo["author"]["email"],
	    description=pkginfo["desc"],
		license=pkginfo.get("license") or "GPLv3",
	    long_description=long_description,
	    long_description_content_type="text/markdown",
	    url="https://github.com/" + pkginfo["author"]["github"] + "/" + (pkginfo.get("links",{}).get("github") or pkginfo.get("name")),
	    packages=[packagename],
	    classifiers=[
	        "Programming Language :: Python :: 3",
	        "License :: OSI Approved :: GNU General Public License v3 (GPLv3)",
	        "Operating System :: OS Independent",
	    ],
		python_requires=">=3.5",
		install_requires=pkginfo["requires"],
		package_data={'': pkginfo["resources"]},
		include_package_data=True,
		entry_points = {
			"console_scripts":[
				cmd + " = " + pkginfo["name"] + "." + pkginfo["commands"][cmd]
				for cmd in pkginfo["commands"]
			]
		}
	)


	os.system("git tag v" + ".".join(str(n) for n in pkginfo["version"]))


	os.system("python3 -m twine upload --skip-existing dist/*")

	shutil.rmtree("build")
	shutil.rmtree("dist")
	for d in glob.glob("*.egg-info"):
		shutil.rmtree(d)
