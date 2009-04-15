# 
# namcap rules - invalidstartdir
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

import pacman, re

class package:
	def short_name(self):
		return "invalidstartdir"
	def long_name(self):
		return "Looks for anything that's not $startdir/pkg or $startdir/src"
	def prereq(self):
		return ""
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		for i in pkginfo.pkgbuild:
			startdirs = re.split('\$startdir',i)
			for j in startdirs[1:]:
				if j[:4] != '/pkg' and j[:4] != '/src':
					ret[0].append(("file-referred-in-startdir", ()))
				elif j[:4] == '/pkg':
					ret[2].append(("recommend-use-pkgdir", ()))
				elif j[:4] == '/src':
					ret[2].append(("recommend-use-srcdir", ()))
		return ret
	def type(self):
		return "pkgbuild"
# vim: set ts=4 sw=4 noet:
