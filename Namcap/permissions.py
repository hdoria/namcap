# 
# namcap rules - permissions
# Copyright (C) 2003-2007 Jason Chu <jason@archlinux.org>
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

import tarfile

class package:
	def short_name(self):
		return "permissions"
	def long_name(self):
		return "Checks file permissions."
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		for i in tar.getmembers():
			if not i.mode & 4 and not (i.issym() or i.islnk()):
				ret[1].append(("file-not-world-readable %s", i.name))
			if i.mode & 2 and not (i.issym() or i.islnk()):
				ret[1].append(("file-world-writable %s", i.name))
			if not i.mode & 1 and i.isdir():
				ret[1].append(("directory-not-world-executable %s", i.name))
			if str(i.name).endswith('.a') and i.mode != 0644:
				ret[1].append(("incorrect-library-permissions %s", i.name))
		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
