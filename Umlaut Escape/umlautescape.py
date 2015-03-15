#!/usr/bin/python
# -*- coding: utf8 -*-

"""A simple command-line tool for replacing Umlauts in HTML and Latex documents.
by Tobias Küster, 2010

Usage: umlautescape.py [Options] File
Options:
  -h, --help            show this help message and exit
  -m MODE, --mode=MODE  mode; one from ['latex', 'html']
  -i, --inverse         reverse substitution?
"""

def replace(string, tuples, inverse=False):
	"""Substitute Umlauts (or any other patterns) in a string.
	@param string: string in which to replace the Umlauts
	@param table: a list of tuples (umlaut, escape sequence)
	@param inverse: if True, the escape sequences are subst. with the umlauts
	@return: string with the umlauts being escaped (or reverted, if inverse set)
	"""
	for key, value in tuples:
		if inverse:
			key, value = value, key
		string = string.replace(key, value)
	return string

# replacement tables for HTML and LaTeX
htmlTable  = [('ä', '&auml;'), ('Ä', '&Auml;'),
              ('ö', '&ouml;'), ('Ö', '&Ouml;'),
              ('ü', '&uuml;'), ('Ü', '&Uuml;'),
              ('ß', '&szlig;'), ('---', '&mdash;'), ('--', '&ndash;') ]
latexTable = [('ä', '\\"{a}'), ('Ä', '\\"{A}'),
              ('ö', '\\"{o}'), ('Ö', '\\"{O}'),
              ('ü', '\\"{u}'), ('Ü', '\\"{U}'),
              ('ß', '\\ss{}') ]
tables = { 'html': htmlTable, 'latex': latexTable }

# Run script from command line
if __name__ == "__main__":
	import optparse, shutil

	# parse and check command line options
	parser = optparse.OptionParser("umlautescape.py [Options] File")
	parser.add_option("-m", "--mode", dest="mode", 
	                  help="mode; one from " + str(tables.keys()))
  	parser.add_option("-i", "--inverse", dest="inverse", action="store_true",
  					  help="reverse substitution?", default=False)
	(options, args) = parser.parse_args()
	if len(args) != 1:
		parser.error("no file given")
	if not options.mode:
		parser.error("no mode given")
	elif not options.mode in tables.keys():
		parser.error("unknown mode: " + options.mode)
	
	# read filename from command line and read file content
	fname = args[0]
	with  open(fname, 'r') as f:
		content= f.read()

	# create backup copy
	shutil.copyfile(fname, fname + '.bak')

	# replace umlauts in content
	content = replace(content, tables[options.mode], options.inverse)

	# write file
	with open(fname, 'w') as f:
		f.write(content)
