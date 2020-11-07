#!/usr/bin/env python3
# -*- coding: UTF-8 -*-

#  This file is part of the synctextranslator package.
#
#  Copyright (C) 2020  Benedikt Otto <s6beotto@uni-bonn.de>
#
#  This program is free software: you can redistribute it and/or modify
#  it under the terms of the GNU General Public License as published by
#  the Free Software Foundation, either version 3 of the License, or
#  any later version.
#
#  This program is distributed in the hope that it will be useful,
#  but WITHOUT ANY WARRANTY; without even the implied warranty of
#  MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the
#  GNU General Public License for more details.
#
#  You should have received a copy of the GNU General Public License
#  along with this program.  If not, see <https://www.gnu.org/licenses/>.


import sys
import subprocess

from linenumber_converter.converter import LineNumberConverter

# source: https://wiki.contextgarden.net/SyncTeX
#okular --unique 'test.pdf#src:24 test.tex'&


def callOkular(pdf_file, line, tex_file):
	# Call okular in unique mode with reference to the tex file
	cmd = 'okular --unique "%s#src:%d %s"&' %(pdf_file, line, tex_file)
	subprocess.call(cmd, shell=True)


def callZathura(pdf_file, line, tex_file):
	# Call zathura with reference to the tex file
	cmd = 'zathura --synctex-forward %d:0:"%s" %s&' %(line, tex_file, pdf_file)
	subprocess.call(cmd, shell=True)

TARGETS = {
	'okular': callOkular,
	'zathura': callZathura,
	}


def callVSCode(pdf_file, line, tex_source):
	# Open file at specific line in VSCode
	cmd = 'code -g "%s":%d' %(tex_source, line)
	subprocess.call(cmd, shell=True)

TARGETS_INV = {
	'vscode': callVSCode,
	}

def translate(line, tex_source, tex_file, pdf_file, target):
	# forward synctex
	if tex_source != tex_file:
		convert = LineNumberConverter(tex_source, tex_file)

		newline = convert.convert(line)

	else:
		newline = line

	if target in TARGETS:
		TARGETS[target](pdf_file, newline, tex_file)


def translate_inv(line, tex_source, tex_file, pdf_file, target):
	# backward synctex
	convert = LineNumberConverter(tex_source, tex_file)

	newline = convert.convert_inv(line)

	if target in TARGETS_INV:
		TARGETS_INV[target](pdf_file, newline, tex_source)


def load_config(origin):
	# extract configuration from the % synctextranslator section of the tex file
	#if not origin.endswith('.tex'):
	origin = '.'.join(origin.split('.')[:-1]) + '.tex'
	origin_pdf = '.'.join(origin.split('.')[:-1]) + '.pdf'

	active = False
	extracted = []

	with open(origin) as f:
		for line in f:
			if line.lstrip(' \t')[0:1] != '%':
				active = False

			if active:
				extracted.append(line.lstrip(' \t%').strip('\n '))

			if '% synctextranslator' in line:
				active = True

	params = {
		'tex_source': origin,
		'tex_file': origin,
		'pdf_file': origin_pdf,
	}
	params = {**params, **{line.split('=')[0].strip(' '): line.split('=')[1].lstrip(' ') for line in extracted if '=' in line}}
	if not 'directory' in params:
		params['directory'] = ''
	# 3 keys are needed: tex_source, tex_file, pdf_file
	return params.get('directory') + params.get('tex_source'), \
			params.get('directory') + params.get('tex_file'), \
			params.get('directory') + params.get('pdf_file')

def main(*args, **kwargs):
	'''
	Main function
	'''
	if len(sys.argv) == 4:
		line = sys.argv[1]
		origin = sys.argv[2]
		target = sys.argv[3]
		tex_source, tex_file, pdf_file = load_config(origin)

	elif len(sys.argv) == 6:
		line, tex_source, tex_file, pdf_file, target = sys.argv[1:]

	else:
		print('Usage: %s line tex_source tex_file pdf_file target' %sys.argv[0])
		print('Usage: %s line tex_file target' %sys.argv[0])
		return

	if not line.isnumeric():
		print('Linenumber must be an integer')
		return

	line = int(line)

	if target in ['editor', 'viewer']:
		# 'editor' and 'viewer' are meta targets, look them up in configfile
		import os
		CONFIGFILE = os.path.expanduser('~/.config/synctextranslator.conf')
		if os.path.exists(CONFIGFILE):
			import configparser
			config = configparser.ConfigParser()
			config.read(CONFIGFILE)
			target = config.get('DEFAULT', target)

	if target in TARGETS:
		translate(line, tex_source, tex_file, pdf_file, target)

	elif target in TARGETS_INV:
		translate_inv(line, tex_source, tex_file, pdf_file, target)

	else:
		print('target %s unknown' %target)
