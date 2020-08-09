#!/usr/bin/env python

import argparse, sys
import subprocess

from linenumber_converter.converter import LineNumberConverter

# source: https://wiki.contextgarden.net/SyncTeX
#okular --unique 'test.pdf#src:24 test.tex'&


def callOkular(pdf, line, tex):
	cmd = 'okular --unique "%s#src:%d %s"' %(pdf, line, tex)
	subprocess.call(cmd, shell=True)

def main(*args, **kwarsg):
	#TODO: fix args
	line, source, latex, pdf = sys.argv[1:5]
	mode = 'okular'

	line = int(line)

	convert = LineNumberConverter(source, latex)

	newline = convert.convert(line)

	if mode == 'okular':
		callOkular(pdf, newline, latex)
