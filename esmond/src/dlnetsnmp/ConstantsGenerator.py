#!/usr/bin/python
# Copyright (c) 2007 D-Level s.r.l. - All rights reserved

# Based on pynetsnmp-0.26.5 original code by Zenoss, Inc.

# This program is free software; you can redistribute it and/or
# modify it under the terms of the GNU General Public License
# as published by the Free Software Foundation; either version 2
# of the License, or (at your option) any later version.

# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
# GNU General Public License for more details.

# You should have received a copy of the GNU General Public License
# along with this program; if not, write to the Free Software
# Foundation, Inc., 51 Franklin Street, Fifth Floor, Boston, MA  02110-1301, USA.

import re
import os
import optparse

class ConstantsGenerator (object):
	FILENAME = 'DLNetSNMP_CONSTANTS.py'
	
	DEFAULTS = (
		'#------- Default Constants -------\n\n',
		'USM_LENGTH_OID_TRANSFORM = 10',
		'NULL = None',
	)
	
	INCLUDE_FILES = (
		'callback',
		'asn1',
		'snmp',
		'snmp_api',
		'snmp_impl',
		'snmp_logging',
		'snmp_client',
		'mib',
		'default_store',
		'parse',
	)
	
	def __init__ (self, output_path, includes_path):
		self.output_path = output_path
		self.includes_path = includes_path

		self._sp = '[ \t]*'
		self._junk = ['usm', '(x)', 'sizeof', '(string)', '(byte)', '{', '?', 'err', 'strlen']
		self._comment = re.compile ('/\\*(.*\\*/|[^*]*$)')
		self._define = re.compile (
			self._sp.join (
				['^',
				 '#',
				 'define',
				 '([A-Za-z0-9_]+)',
				 '([^\\\\]+)$']
			)
		)
		
	def _process_include (self, f, output):
		fn = os.path.join (self.includes_path, '%s.h' % f)
		print 'Processing "%s"' % fn
		lines = open (fn).readlines ()
		output.write ('\n#------- %s.h -------\n\n' % f)
		for line in lines:
			line = self._comment.sub ('', line)
			m = self._define.match (line)
			if m:
				value = m.group (2).strip ()
				value = value.replace ('(u_char)', '')
				if value:
					for j in self._junk:
						if value.find (j) > -1:
							break
					else:
						output.write ('%s = %s\n' % (m.group (1), value))
	
	def _add_defaults (self, output):
		for i in self.DEFAULTS:
			output.write (i + '\n')
		
	def generate (self):
		try:
			tmp_filename = os.path.join (self.output_path, self.FILENAME + '.new')
			output = open (tmp_filename, 'w')
			
			output.write ('# Copyright (c) 2007 D-Level s.r.l. - All rights reserved\n')
			output.write ('# THIS FILE WAS AUTO-GENERATED BY ConstantsGenerator.py - DO NOT EDIT!!!\n\n')
			
			self._add_defaults (output)
			
			for f in self.INCLUDE_FILES:
				self._process_include (f, output)
			output.close ()
			os.rename (tmp_filename, os.path.join (self.output_path, self.FILENAME))
		except IOError:
			pass

def main ():
	parser = optparse.OptionParser (version='1.0', prog='setup')

	parser.add_option (
		'-o',
		'--output-path',
		type = 'string',
		dest = 'output_path',
		default = '',
		help = 'Path (without basename) where to store the generated constants.'
	)

	parser.add_option (
		'-i',
		'--includes-path',
		type = 'string',
		dest = 'includes_path',
		default = '',
		help = 'Path where to search for the NetSNMP includes.'
	)
	
	options = parser.parse_args ()[0]
	
	if not options.output_path:
		options.output_path = os.path.dirname (__file__)
		
	if not options.includes_path:
		parser.print_help ()
		return

	cg = ConstantsGenerator (
		output_path = os.path.expandvars (os.path.expanduser (options.output_path)),
		includes_path = os.path.expandvars (os.path.expanduser (options.includes_path))
	)
	
	cg.generate ()
	
if __name__ == '__main__':
	main ()
	