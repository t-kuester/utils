# -*- coding: utf8 -*-

"""Analyzer module for Bibliography Analyzer Utility.
by Tobias Küster, 2015
"""

from itertools import combinations
from collections import defaultdict
import re

BAD_WORDS = set(["a", "at", "the", "with", "and", "of", "in", "for", "from",
				 "to", "on", "an", "when", "using", "how", "under", "as", 
				 "new", "be", "or", "via", "no", "by", "over", "can", "here",
				 "about" "what", "who", "why"])
WORDS_PATTERN = re.compile(r"[a-z0-9][a-z0-9-_]*")

def get_coauthors(bibitems):
	"""Get number of papers co-authored together for each pair of co-authors.
	"""
	coauthors = defaultdict(int)
	for item in bibitems:
		for pair in combinations(item.authors, 2):
			coauthors[tuple(sorted(pair))] += 1
	return dict(coauthors)

def get_title_ngrams(bibitems, n, min_num=1, stemming=True):
	"""Get get all n-grams from 1 up to n for the title words in the papers.
	"""
	stem = _stem if stemming else str
	ngrams = defaultdict(int)
	for item in bibitems:
		title_words = map(stem, WORDS_PATTERN.findall(item.title.lower()))
		proper_title_words = [word for word in title_words if word not in BAD_WORDS]
		for k in range(len(proper_title_words) - n):
			ngrams[tuple(proper_title_words[k:k+n])] += 1
	return dict((key, val) for key, val in ngrams.items() if val >= min_num)
	

def _stem(word):
	"""Return the word's stemmed form.
	"""
	# TODO
	print "stemming"
	return word	


# testing
if __name__ == "__main__":
	from pprint import pprint
	from bib_parser import parse_bib_from_bibtex, parse_bib_from_list
	# items = parse_bib_from_list("papers.txt")
	items = parse_bib_from_bibtex("literature.bib")
	pprint(get_coauthors(items))
	pprint(get_title_ngrams(items, 3, 2, False))

