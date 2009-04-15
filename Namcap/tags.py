# 
# namcap rules - tags
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
		return "tags"
	def long_name(self):
		return "Looks for Maintainer and Contributor comments"
	def prereq(self):
		return ""
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		contributortag = 0
		maintainertag = 0
		idtag = 0
		for i in pkginfo.pkgbuild:
			if re.match("#\s*Contributor\s*:",i) != None:
				contributortag = 1
			if re.match("#\s*Maintainer\s*:",i) != None:
				maintainertag = 1

		if contributortag != 1:
			ret[2].append(("missing-contributor", ()))

		if maintainertag != 1:
			ret[1].append(("missing-maintainer", ()))

		return ret
	def type(self):
		return "pkgbuild"
# vim: set ts=4 sw=4 noet:
