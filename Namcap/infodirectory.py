#
# namcap rules - infodirectory
# Copyright (C) 2008 Allan McRae <allan@archlinux.org>
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
		return "infodirectory"
	def long_name(self):
		return "Checks for info directory file."
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		for i in tar.getnames():
			if i == "usr/share/info/dir":
				ret[0].append(("info-dir-file-present %s", i))
		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
