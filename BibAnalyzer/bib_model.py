# -*- coding: utf8 -*-

class BibItem:
	
	def __init__(self, authors, title, year):
		self.authors = tuple(authors)
		self.title = title
		self.year = year
		
	def __hash__(self):
		res = 1
		res *= 17 + hash(self.authors)
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


if __name__ == "__main__":
	b = BibItem(["Tobias Küster", "Marco Lützenberger"], "Bla bla titel", 2015)
	print b
	print repr(b)
	print eval(repr(b)) == b
	