# 
# namcap rules - sfurl
# Copyright (C) 2004-2007 Ben Mazer <ben@benmazer.net>
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

import pacman,re

class package:
	def short_name(self):
		return "sfurl"
	def long_name(self):
		return "Checks for proper sourceforge URLs"
	def prereq(self):
		return ""
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		if hasattr(pkginfo, 'source'):
			for source in pkginfo.source:
				if re.match('(http://|ftp://)\w+.dl.(sourceforge|sf).net',source) != None:
					ret[1].append(("specific-sourceforge-mirror", ()))
				if re.match('(http://|ftp://)dl.(sourceforge|sf).net',source) != None:
					ret[1].append(("using-dl-sourceforge", ()))
		return ret
	def type(self):
		return "pkgbuild"
# vim: set ts=4 sw=4 noet:
