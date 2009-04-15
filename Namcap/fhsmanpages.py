# 
# namcap rules - fhsmanpages
# Copyright (C) 2008 Aaron Griffin <aaronmgriffin@gmail.com>
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

import os
import tarfile

class package:
	def short_name(self):
		return "fhs-manpages"
	def long_name(self):
		return "Verifies correct installation of man pages"
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		gooddir = 'usr/share/man'
		bad_dir = 'usr/man'
		ret = [[],[],[]]
		for i in tar.getmembers():
			if i.name.startswith(bad_dir):
				ret[0].append(("non-fhs-man-page %s", i.name))
			elif not i.name.startswith(gooddir):
				#Check everything else to see if it has a 'man' path component
				for part in i.name.split(os.sep):
					if part == "man":
						ret[1].append(("potential-non-fhs-man-page %s", i.name))

		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
