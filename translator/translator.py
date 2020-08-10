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


def translate(line, tex_source, tex_file, pdf_file, target):
	convert = LineNumberConverter(tex_source, tex_file)

	newline = convert.convert(line)

	if target == 'okular':
		callOkular(pdf_file, newline, tex_file)

	elif target == 'zathura':
		callZathura(pdf_file, newline, tex_file)


def load_config(texfile):
	filename = Path(texfile).name
	config_filename = (Path(texfile).parent / '_build' / filename).with_suffix('.conf')

	config = configparser.ConfigParser()

	config.read(config_filename)

	return config.get('DEFAULT', 'tex_source'), config.get('DEFAULT', 'tex_file'), config.get('DEFAULT', 'pdf_file')

def main(*args, **kwargs):
	if len(sys.argv) == 4 and sys.argv[2].endswith('.tex'):
		tex_source, tex_file, pdf_file = load_config(sys.argv[2])
		line = sys.argv[1]
		target = sys.argv[3]

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

	targets = ['okular', 'zathura']
	targets_inv = []

	if target in targets:
		translate(line, tex_source, tex_file, pdf_file, target)

	elif target in targets_inv:
		pass#translate(line, tex_source, tex_file, pdf_file, mode)

	else:
		print('target %s unknown' %target)
