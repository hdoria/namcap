#!/usr/bin/env python
from distutils.core import setup

DATAFILES = [('/usr/share/man/man1', ['namcap.1']),
		('/usr/share/namcap', ['tags'])]

setup(name="namcap",
	version="2.0",
	description="Pacman package analyzer",
	author="Jason Chu",
	author_email="jason@archlinux.org",
	py_modules=["pacman"], packages=["Namcap"], scripts=["namcap.py", 'parsepkgbuild'],data_files =DATAFILES)

# vim: set ts=4 sw=4 noet:
