import re
from bib_model import BibItem


def parse_bib(filename, entry_regex, authors_regex, title_regex, year_regex, author_sep=","):
	with open(filename) as f:

		items = []
		for item in re.finditer(entry_regex, f.read()):
			item = item.group()

			extract = lambda regex: re.search(regex, item).group(1) if regex else None

			authors = extract(authors_regex)
			title = extract(title_regex)
			year = extract(year_regex)

			author_list = [author.strip() for author in authors.split(author_sep)]

			items.append(BibItem(author_list, title, year))
		
		return items


def parse_bib_from_list(filename):
	entry_regex   = r"TITEL: .*\s+AUTOR: .*"
	authors_regex = r"AUTOR: (.*)"
	title_regex   = r"TITEL: (.*)"
	year_regex    = None
	return parse_bib(filename, entry_regex, authors_regex, title_regex, year_regex)


def parse_bib_from_bibtex(filename):
	entry_regex   = r""
	authors_regex = r""
	title_regex   = r""
	year_regex    = r""
	return parse_bib(filename, entry_regex, authors_regex, title_regex, year_regex)


if __name__ == "__main__":
	items = parse_bib_from_list("AAMAS 2013.txt")
	for item in items:
		print item
