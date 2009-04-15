# 
# namcap rules - md5sums
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

import pacman

class package:
	def short_name(self):
		return "md5sums"
	def long_name(self):
		return "Verifies md5sums are included in a PKGBUILD"
	def prereq(self):
		return ""
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		if hasattr(pkginfo, 'source'):
			if not hasattr(pkginfo, 'md5sums'):
				ret[0].append(("missing-md5sums", ()))
			else:
				if len(pkginfo.source) > len(pkginfo.md5sums):
					ret[0].append(("not-enough-md5sums %i needed", len(pkginfo.source)))
				elif len(pkginfo.source) < len(pkginfo.md5sums):
					ret[0].append(("too-many-md5sums %i needed", len(pkginfo.source)))
		if hasattr(pkginfo, 'md5sums'):
			for sum in pkginfo.md5sums:
				if len(sum) != 32:
					ret[0].append(("improper-md5sum %s", sum))
		return ret
	def type(self):
		return "pkgbuild"
# vim: set ts=4 sw=4 noet:
