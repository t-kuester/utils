# -*- coding: utf8 -*-

"""Module for parsing bibliography files in different formats.
by Tobias Küster, 2015
"""

import re
from bib_model import BibItem


def parse_bib(filename, entry_regex, parse_func):
	"""Read file and parse bibliography items.
	- filename is the name of the file
	- entry_regex is a regular expression matching a single bibliography item
	- parse_func is a function mapping that item (a string) to a BibItem
	- returns an according list of BibItems
	"""
	with open(filename) as f:
		return filter(None, (parse_func(item.group()) 
		                     for item in re.finditer(entry_regex, f.read())))

def make_parse_func(authors_regex, title_regex, year_regex, author_sep=","):
	"""Create and return a function creating BibItems using regular expressions
	for title, author and year.
	"""
	def func(item):
		"""function parsing item (a string) to BibItem object.
		"""
		extract = lambda regex: re.search(regex, item).group(1) if regex else None
		try:
			authors = extract(authors_regex)
			title = extract(title_regex)
			year = extract(year_regex)
			author_list = [author.strip() for author in authors.split(author_sep)]
			return BibItem(author_list, title, year)
		except:
			print "WARNING: Could not parse item: \n" + item
			
	return func

def parse_bib_from_list(filename):
	"""Parse list of bibliography items from simple text file, assuming format
	TITEL: <the title>
	AUTOR: <list of authors>
	"""
	entry_regex   = r"TITEL: .*\s*AUTOR: .*"
	parse_func = make_parse_func(r"AUTOR: (.*)", r"TITEL: (.*)", None)
	return parse_bib(filename, entry_regex, parse_func)

def parse_bib_from_bibtex(filename):
	"""Parse list of bibliography items from Bibtex file. Bibtex is not a 
	regular language, but assuming that each entry starts and ends at the 
	beginning of a line, we can still get some good results with a regex.
	"""
	entry_regex = r'''
			(?msx)    # flags: multi-line, dot-match-all, verbose
			^@\w+\{   # start of line, item type
			.*?       # content, can span multiple lines, non-greedy
			^\}       # start of line, closing parens
			'''
	attr_regex = r'''
			(?ix)     # flags: ignore-case, verbose
			\s*       # leading space
			%s        # what to match: author, title, or year
			\s*=\s*   # space and equals
			[{\"']    # opening parens
			(.*)      # the actual author, title, or year
			[}\"']    # closing parens or quote
			\,?       # optional comma
			'''
	parse_func = make_parse_func(attr_regex % "author", attr_regex % "title", 
	                             attr_regex % "year", " and ")
	return parse_bib(filename, entry_regex, parse_func)


# just for testing...
if __name__ == "__main__":
	# items = parse_bib_from_list("AAMAS 2013.txt")
	items = parse_bib_from_bibtex("literature.bib")
	for item in items:
		print item
