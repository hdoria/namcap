# 
# namcap rules - array
# Copyright (C) 2003-2007 Jesse Young <jesseyoung@gmail.com>
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
		return "array"
	def long_name(self):
		return "Verifies that array variables are actually arrays"
	def prereq(self):
		return ""
	def analyze(self, pkginfo, tar):
		arrayvars = ['arch', 'license', 'depends', 'makedepends',
			 'optdepends', 'provides', 'conflicts' , 'replaces',
			 'backup', 'source', 'noextract', 'md5sums']
		ret = [[],[],[]]
		for i in pkginfo.pkgbuild:
			m = re.match('\s*(.*)\s*=\s*(.*)\n', i)
			for j in arrayvars:
				if m and m.group(1) == j:
					if not m.group(2).startswith('('):
						ret[1].append(("variable-not-array %s", j))

		return ret
	def type(self):
		return "pkgbuild"
# vim: set ts=4 sw=4 noet:
