# 
# namcap rules - emptydir
# Copyright (C) 2004-2007 Jason Chu <jason@archlinux.org>
# 
#   This program is free software; you can redistribute it and/or modify
#   it under the terms of the GNU General Public License as published by
#   the Free Software Foundation; either version 2 of the License, or
#   (at your option) any later version.
#
#   This program is distributed in the hope that it will be useful,
#   but WITHOUT ANY WARRANTY; without even the implied warranty of
#   MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#   GNU General Public License for more details.
#
#   You should have received a copy of the GNU General Public License
#   along with this program; if not, write to the Free Software
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA  02111-1307  USA
# 

import pacman

def inDir(dir, files):
	for i in files:
		if i[:len(dir)] == dir:
			return 1
	return 0

class package:
	def short_name(self):
		return "emptydir"
	def long_name(self):
		return "Warns about empty directories in a package"
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]

		# Strip trailing directory slashes (since python 2.5.1)
		dirs = [x.rstrip('/') + '/' for x in tar.getnames() if x.endswith('/')]

		files = [x for x in tar.getnames() if not x.endswith('/')]
		for i in dirs:
			if not inDir(i, files):
				ret[1].append(("empty-directory %s", i))
		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
