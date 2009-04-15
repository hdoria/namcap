# 
# namcap rules - gnomemime
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
#   Foundation, Inc., 59 Temple Place, Suite 330, Boston, MA 02111-1307  USA
# 

import tarfile

class package:
    def short_name(self):
        return "gnomemime"
    def long_name(self):
        return "Checks for generated GNOME mime files"
    def prereq(self):
        return "tar"
    def analyze(self, pkginfo, tar):
        mime_files = [
                'opt/gnome/share/applications/mimeinfo.cache',
                'opt/gnome/share/mime/XMLnamespaces', 
                'opt/gnome/share/mime/aliases', 
                'opt/gnome/share/mime/globs', 
                'opt/gnome/share/mime/magic', 
                'opt/gnome/share/mime/subclasses'
                ]

        ret = [[],[],[]]
        for i in tar.getnames():
            if i in mime_files:
                ret[0].append("File (" + i + ") is an auto-generated GNOME mime file.")
        return ret
    def type(self):
        return "tarball"
# vim: set ts=4 sw=4 noet:
