#
# namcap rules - fhsinfopages
# Copyright (C) 2009 Hugo Doria <hugo@archlinux.org>
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
		return "fhs-infopages"
	def long_name(self):
		return "Verifies correct installation of info pages"
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		for i in tar.getmembers():
			if i.name.startswith('usr/info'):
				ret[0].append(("non-fhs-info-page %s", i.name))
			elif not i.name.startswith('usr/share/info'):
				for part in i.name.split(os.sep):
					if part == "info":
						ret[1].append(("potential-non-fhs-info-page %s", i.name))

		return ret
	def type(self):
		return "tarball"