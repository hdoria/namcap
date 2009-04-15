# 
# namcap rules - licensepkg
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
import os.path

class package:
	def short_name(self):
		return "licensepkg"
	def long_name(self):
		return "Verifies license is included in a package file"
	def prereq(self):
		return "tar"
	def analyze(self, pkginfo, tar):
		ret = [[],[],[]]
		if not hasattr(pkginfo, 'license') or len(pkginfo.license) == 0:
			ret[0].append(("missing-license", ()))
		else:
			licensepaths = [x for x in tar.getnames() if x.startswith('usr/share/licenses') and not x.endswith('/')]
			licensedirs = [os.path.split(os.path.split(x)[0])[1] for x in licensepaths]
			licensefiles = [os.path.split(x)[1] for x in licensepaths]
			# Check all licenses for validity
			for license in pkginfo.license:
				lowerlicense = license.lower()
				if lowerlicense.startswith('custom') or lowerlicense in ("bsd", "mit", "isc", "python", "zlib", "libpng"):
					if pkginfo.name not in licensedirs:
						ret[0].append(("missing-custom-license-dir usr/share/licenses/%s", pkginfo.name))
					elif len(licensefiles) == 0:
						ret[0].append(("missing-custom-license-file usr/share/licenses/%s/*", pkginfo.name))
				# A common license
				else:
					commonlicenses = [x.lower() for x in os.listdir('/usr/share/licenses/common')]
					if lowerlicense not in commonlicenses:
						ret[0].append(("not-a-common-license %s", license))
		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
