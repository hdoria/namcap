# 
# namcap rules - depends
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

import re, os, os.path, pacman, subprocess

pkgcache = {}

def load(name, path=None):
	if not pkgcache.has_key(name):
		pkgcache[name] = pacman.load(name)
	return pkgcache[name]

libcache = {'i686': {}, 'x86-64': {}}

def getcovered(current, dependlist, covereddepend):
	if current == None:
		for i in dependlist:
			pac = load(i)
			if pac != None and hasattr(pac, 'depends'):
				for j in pac.depends:
					if j != None and not j in covereddepend.keys():
						covereddepend[j] = 1
						getcovered(j, dependlist, covereddepend)
	else:
		pac = load(current)
		if pac != None and hasattr(pac, 'depends'):
			for i in pac.depends:
				if i != None and not i in covereddepend.keys():
					covereddepend[i] = 1
					getcovered(i, dependlist, covereddepend)

def figurebitsize(line):
	"""
	Given a line of output from readelf (usually Shared library:) return 'i686' or 'x86-64' if the binary is a 32bit or 64bit binary
	"""

	address = line.split()[0]
	if len(address) == 18: # + '0x' + 16 digits
		return 'x86-64'
	else:
		return 'i686'

def scanlibs(data, dirname, names):
	"""
	Walk over all the files in the package and run "readelf -d" on them.
	If they depend on a library, store that library's path in sharedlibs
	"""
	sharedlibs, scripts = data
	for i in names:
		if os.path.isfile(dirname+'/'+i):
			var = subprocess.Popen('readelf -d ' + dirname+'/'+i,
					shell=True,
					stdout=subprocess.PIPE,
					stderr=subprocess.PIPE).communicate()
			for j in var[0].split('\n'):
				n = re.search('Shared library: \[(.*)\]', j)
				# Is this a Shared library: line?
				if n != None:
					# Find out its architecture
					architecture = figurebitsize(j)
					try:
						libpath = os.path.abspath(libcache[architecture][n.group(1)])[1:]
						sharedlibs.setdefault(libpath, {})[dirname+'/'+i] = 1
					except KeyError:
						# Ignore that library if we can't find it
						# TODO: review it
						pass
				# But we can check to see if it's a script we know about
				else:
					fd = open(dirname+'/'+i)
					firstline = fd.readline()
					if re.match('#!.*python',firstline) != None:
						scripts.setdefault('python', {})[dirname+'/'+i] = 1
					elif re.match('#!.*perl',firstline) != None:
						scripts.setdefault('perl', {})[dirname+'/'+i] = 1
					elif re.match('#!.*ruby',firstline) != None:
						scripts.setdefault('ruby', {})[dirname+'/'+i] = 1
					elif re.match('#!.*bash',firstline) != None or re.match('#!.*sh',firstline) != None:
						scripts.setdefault('bash', {})[dirname+'/'+i] = 1
					elif re.match('#!.*wish',firstline) != None:
						scripts.setdefault('tk', {})[dirname+'/'+i] = 1
					elif re.match('#!.*expect',firstline) != None:
						scripts.setdefault('expect', {})[dirname+'/'+i] = 1
					fd.close()
	return
			
def finddepends(liblist):
	dependlist = {}
	foundlist = []

	somatches = {}
	actualpath = {}

	for j in liblist.keys():
		actualpath[j] = os.path.realpath('/'+j)[1:]

	# Sometimes packages don't include all so .so, .so.1, .so.1.13, .so.1.13.19 files
	# They rely on ldconfig to create all the symlinks
	# So we will strip off the matching part of the files and use this regexp to match the rest
	so_end = re.compile('(\.\d+)*')

	pacmandb = '/var/lib/pacman/local'
	for i in os.listdir(pacmandb):
		if os.path.isfile(pacmandb+'/'+i+'/files'):
			file = open(pacmandb+'/'+i+'/files')
			for j in file.readlines():
				if j[len(j)-1:]=='\n':
					j = j[:len(j)-1]

				for k in liblist.keys():
					# If the file is an exact match, so it's a match up to a point and everything after that point matches a the regexp
					# i.e. gpm includes libgpm.so and libgpm.so.1.19.0, but everything links to libgpm.so.1
					# We compare find libgpm.so.1.19.0 startswith libgpm.so.1 and .19.0 matches the regexp
					if j == actualpath[k] or (j.startswith(actualpath[k]) and so_end.match(j[len(actualpath[k]):])):
						n = re.match('(.*)-([^-]*)-([^-]*)', i)
						if not dependlist.has_key(n.group(1)):
							dependlist[n.group(1)] = {}
						for x in liblist[k]:
							dependlist[n.group(1)][x] = 1
						foundlist.append(k)
			file.close()

	ret = []
	for i in liblist.keys():
		if i not in foundlist:
			ret.append('Library ' + i + ' has no package associated')
	return dependlist, ret

def getprovides(depends, provides):
	for i in depends.keys():
		pac = load(i)

		if pac != None and hasattr(pac, 'provides') and pac.provides != None:
			provides[i] = pac.provides

def filllibcache():
	var = subprocess.Popen('ldconfig -p', 
			shell=True,
			stdout=subprocess.PIPE,
			stderr=subprocess.PIPE).communicate()
	for j in var[0].split('\n'):
		g = re.match('\s*(.*) \((.*)\) => (.*)',j)
		if g != None:
			if g.group(2).startswith('libc6,x86-64'):
				libcache['x86-64'][g.group(1)] = g.group(3)
			else:
				libcache['i686'][g.group(1)] = g.group(3)


class package:
	def short_name(self):
		return "depends"
	def long_name(self):
		return "Checks dependencies semi-smartly."
	def prereq(self):
		return "extract"
	def analyze(self, pkginfo, data):
		liblist = [{},{}]
		dependlist = {}
		smartdepend = {}
		smartprovides = {}
		covereddepend = {}
		pkgcovered = {}
		ret = [[],[],[]]
		filllibcache()
		os.environ['LC_ALL'] = 'C'
		os.path.walk(data, scanlibs, liblist)

		# Ldd all the files and find all the link and script dependencies
		dependlist, tmpret = finddepends(liblist[0])

		# Handle "no package associated" errors
		for i in tmpret:
			ret[1].append(i)

		# Do the script handling stuff
		for i, v in liblist[1].iteritems():
			if not dependlist.has_key(i):
				dependlist[i] = {}
			for j in v.keys():
				dependlist[i][j] = 1
			files = [x[len(data)+1:] for x in v.keys()]
			ret[2].append(("script-link-detected %s in %s", (i, str(files))))

		# Remove the package name from that list, we can't depend on ourselves.
		if dependlist.has_key(pkginfo.name):
			del dependlist[pkginfo.name]

		# Do the info stuff
		for i, v in dependlist.iteritems():
			if type(v) == dict:
				files = [x[len(data)+1:] for x in v.keys()]
				ret[2].append(("link-level-dependence %s on %s", (str(files), i)))

		# Check for packages in testing
		if os.path.isdir('/var/lib/pacman/sync/testing'):
			for i in dependlist.keys():
				p = pacman.load(i, '/var/lib/pacman/sync/testing/')
				q = load(i)
				if p != None and q != None and p.version == q.version:
					ret[1].append(("dependency-is-testing-release %s", i))

		# Find all the covered dependencies from the PKGBUILD
		pkgdepend = {}
		if hasattr(pkginfo, 'depends'):
			for i in pkginfo.depends:
				pkgdepend[i] = 1

		# Include the optdepends from the PKGBUILD
		if hasattr(pkginfo, 'optdepends'):
			for i in pkginfo.optdepends:
				pkgdepend[i] = 1

		getcovered(None, pkgdepend, pkgcovered)

		# Do tree walking to find all the non-leaves (branches?)
		getcovered(None, dependlist, covereddepend)
		for i in covereddepend.keys():
			ret[2].append(("dependency-covered-by-link-dependence %s", i))

		# Set difference them to find the leaves
		for i in dependlist.keys():
			if not i in covereddepend.keys():
				smartdepend[i] = 1

		# Get the provides so we can reference them later
		getprovides(dependlist, smartprovides)

		# Do the actual message outputting stuff
		for i in smartdepend.keys():
			# If (i is not in the PKGBUILD's dependencies
			# and i isn't the package name
			# and ((there are provides for i
			# and those provides aren't included in the package's dependencies)
			# or there are no provides for i))
			all_dependencies = getattr(pkginfo, 'depends', []) + getattr(pkginfo, 'optdepends', []) + pkgcovered.keys()
			if (i not in all_dependencies and i != pkginfo.name and ((smartprovides.has_key(i) and len([c for c in smartprovides[i] if c in pkgcovered.keys()]) == 0) or not smartprovides.has_key(i))):
					if type(dependlist[i]) == dict:
						ret[0].append(("dependency-detected-not-included %s from files %s", (i, str([x[len(data)+1:] for x in dependlist[i].keys()])) ))
					else:
						ret[0].append(("dependency-detected-not-included %s", i))
		if hasattr(pkginfo, 'depends'):
			for i in pkginfo.depends:
				if covereddepend.has_key(i) and dependlist.has_key(i):
					ret[1].append(("dependency-already-satisfied %s", i))
				# if i is not in the depends as we see them and it's not in any of the provides from said depends
				elif not smartdepend.has_key(i) and i not in [y for x in smartprovides.values() for y in x]:
					ret[1].append(("dependency-not-needed %s", i))
		ret[2].append(("depends-by-namcap-sight depends=(%s)", ' '.join(smartdepend.keys()) ))
		return ret
	def type(self):
		return "tarball"
# vim: set ts=4 sw=4 noet:
