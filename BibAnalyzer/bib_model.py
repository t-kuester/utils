# -*- coding: utf8 -*-

"""Domain model for Bibliography Analyzer Utility.
by Tobias Küster, 2015

- simple representation for bibliography item
"""

class BibItem:
	"""Class representing a bibliography item.
	
	This is intentionally held simple, with just the very basic attributes, such
	as title of the publication, a list of authors, and the year.
	"""
	
	def __init__(self, authors, title, year):
		self.authors = tuple(authors)
		self.title = title
		self.year = year
		
	def __hash__(self):
		res = 17 + hash(self.authors)
		res *= 23 + hash(self.title)
		res *= 31 + hash(self.year)
		return res
		
	def __eq__(self, other):
		return (isinstance(other, BibItem) and
				self.authors == other.authors and
				self.title == other.title and
				self.year == other.year)
		
	def __str__(self):
		return "{0}: {1}; {2}".format(", ".join(self.authors), self.title, self.year)
		
	def __repr__(self):
		return "BibItem(authors=%r, title=%r, year=%r)" % (self.authors, self.title, self.year)
