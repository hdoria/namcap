# 
# namcap rules - __init__
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

__tarball__ = ['depends', 'directoryname', 'fileownership', 'gnomemenu', 'perllocal', 'permissions', 'symlink', 'urlpkg', 'capsnamespkg', 'emptydir', 'scrollkeeper', 'libtool', 'gnomemime', 'licensepkg', 'infodirectory', 'fhsmanpages', 'fhsinfopages']

__pkgbuild__ = ['md5sums', 'tags', 'url', 'invalidstartdir', 'capsnames', 'carch', 'sfurl', 'badbackups', 'license', 'arrays']

__all__ = __tarball__ + __pkgbuild__

# vim: set ts=4 sw=4 noet:
