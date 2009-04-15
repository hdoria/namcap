# 
# namcap rules - carch
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
		return "carch"
	def long_name(self):
		return "Verifies that no specific host type is used"
	def prereq(self):
		return ""
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		arches = ['i686','i586','x86_64']
		archmatch = re.compile('%s' % '|'.join(arches))
		# Match an arch=(i686) line
		archline = re.compile('arch=\w*(%s)' % '|'.join(arches))
		# Match a [ "$CARCH" = "x86_64" ] line
		archif = re.compile('''\[\s*("|')\$CARCH("|').*("|')(%s)("|')\s*\]''' % '|'.join(arches))
		for i in pkginfo.pkgbuild:
			if archmatch.match(i):
				if not archline.match(i) and not archif.match(i):
					ret[1].append(("specific-host-type-used %s", ",".join(arches)))
		return ret
	def type(self):
		return "pkgbuild"
# vim: set ts=4 sw=4 noet:
