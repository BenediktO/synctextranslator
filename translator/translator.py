#!/usr/bin/env python

import sys
import subprocess
import configparser

from pathlib import Path

from linenumber_converter.converter import LineNumberConverter

# source: https://wiki.contextgarden.net/SyncTeX
#okular --unique 'test.pdf#src:24 test.tex'&


def callOkular(pdf_file, line, tex_file):
	cmd = 'okular --unique "%s#src:%d %s"&' %(pdf_file, line, tex_file)
	subprocess.call(cmd, shell=True)


def callZathura(pdf_file, line, tex_file):
	cmd = 'zathura --synctex-forward %d:0:%s %s&' %(line, tex_file, pdf_file)
	subprocess.call(cmd, shell=True)


def callVSCode(pdf_file, line, tex_source):
	cmd = 'code -g %s:%d' %(tex_source, line)
	subprocess.call(cmd, shell=True)


def translate(line, tex_source, tex_file, pdf_file, target):
	convert = LineNumberConverter(tex_source, tex_file)

	newline = convert.convert(line)

	if target == 'okular':
		callOkular(pdf_file, newline, tex_file)

	elif target == 'zathura':
		callZathura(pdf_file, newline, tex_file)


def translate_inv(line, tex_source, tex_file, pdf_file, target):
	convert = LineNumberConverter(tex_source, tex_file)

	newline = convert.convert_inv(line)

	if target == 'vscode':
		callVSCode(pdf_file, newline, tex_source)


def load_config(conffile, origin):
	if not conffile.endswith('.conf'):
		conffile = '/'.join(conffile.split('/')[0:-1]) + '/synctex.conf'

	config = configparser.ConfigParser()

	config.read(conffile)

	section = origin.split('/')[-1]
	return config.get(section, 'tex_source'), config.get(section, 'tex_file'), config.get(section, 'pdf_file')

def main(*args, **kwargs):
	if len(sys.argv) == 5:
		line = sys.argv[1]
		origin = sys.argv[2]
		conffile = sys.argv[3]
		target = sys.argv[4]
		tex_source, tex_file, pdf_file = load_config(conffile, origin)

	elif len(sys.argv) == 6:
		line, tex_source, tex_file, pdf_file, target = sys.argv[1:]

	else:
		print('Usage: %s line tex_source tex_file pdf_file target' %sys.argv[0])
		print('Usage: %s line origin configfile target' %sys.argv[0])
		return

	if not line.isnumeric():
		print('Linenumber must be an integer')
		return

	line = int(line)

	targets = ['okular', 'zathura']
	targets_inv = ['vscode']

	if target in targets:
		translate(line, tex_source, tex_file, pdf_file, target)

	elif target in targets_inv:
		translate_inv(line, tex_source, tex_file, pdf_file, target)

	else:
		print('target %s unknown' %target)
