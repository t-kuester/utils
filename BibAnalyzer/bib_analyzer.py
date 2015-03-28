# -*- coding: utf8 -*-

"""Analyzer module for Bibliography Analyzer Utility.
by Tobias Küster, 2015

- get co-author relationships
- get frequently used title words and n-grams
- get number of papers per author
"""

from itertools import combinations
from collections import defaultdict
import Stemmer
import re

# some words that are not interesting for common title words, n-grams, etc.
BAD_WORDS = set(["a", "at", "the", "with", "and", "of", "in", "for", "from",
				 "to", "on", "an", "when", "using", "how", "under", "as", 
				 "new", "be", "or", "via", "no", "by", "over", "can", "here",
				 "about" "what", "who", "why", "into", "do", "towards", "between",
				 "is", "are"])

# regular expression for finding words in titles
WORDS_PATTERN = re.compile(r"[a-z0-9-_]*[a-z][a-z0-9-_]*")

# the stemmer used for normalizing the words
STEMMER = Stemmer.Stemmer("english")

def get_coauthors(bibitems):
	"""Get number of papers co-authored together for each pair of co-authors.
	"""
	coauthors = defaultdict(int)
	for item in bibitems:
		for pair in combinations(item.authors, 2):
			coauthors[tuple(sorted(pair))] += 1
	return dict(coauthors)
	
def get_papers_per_author(bibitems, min_num=1):
	"""Get the number of papers each author has written.
	"""
	papers = defaultdict(int)
	for item in bibitems:
		for author in item.authors:
			papers[author] += 1
	return dict((author, num) for author, num in papers.iteritems() if num >= min_num)

def get_title_ngrams(bibitems, n, min_num=1, stemming=False):
	"""Get get all n-grams from 1 up to n for the title words in the papers.
	"""
	stem = STEMMER.stemWord if stemming else str
	ngrams = defaultdict(int)
	for item in bibitems:
		title_words = map(stem, WORDS_PATTERN.findall(item.title.lower()))
		proper_title_words = [word for word in title_words if word not in BAD_WORDS]
		for k in range(len(proper_title_words) - n):
			ngrams[" ".join(proper_title_words[k:k+n])] += 1
	return dict((key, val) for key, val in ngrams.iteritems() if val >= min_num)
	

# testing
if __name__ == "__main__":
	from pprint import pprint
	import bib_parser
	items = bib_parser.parse_bib_from_bibtex("literature.bib")
	pprint(get_coauthors(items))
	pprint(sorted(get_title_ngrams(items, 1, 1).items(), key=lambda x: x[1]))
	pprint(get_papers_per_author(items, 5))