# -*- coding: utf8 -*-

"""Analyzer module for Bibliography Analyzer Utility.
by Tobias Küster, 2015

- get co-author relationships
- get frequently used title words and n-grams
- get number of papers per author
- get authors writing about a certain topic
- TODO get frequent topics per author
"""

from itertools import combinations
from collections import defaultdict
import stemmer # http://tartarus.org/~martin/PorterStemmer/
import re

# some words that are not interesting for common title words, n-grams, etc.
BAD_WORDS = set(['a', 'about', 'an', 'and', 'are', 'as', 'at', 'be', 'between', 
                 'by', 'can', 'do', 'for', 'from', 'here', 'how', 'in', 'into', 
                 'is', 'new', 'no', 'of', 'on', 'or', 'over', 'the', 'to', 
                 'towards', 'under', 'using', 'via', 'what', 'when', 'who', 
                 'why', 'with']
)

# regular expression for finding words in titles
#TODO improve this regex
WORDS_PATTERN = re.compile(r"[a-z0-9-_]*[a-z][a-z0-9-_]*")

# the stemmer used for normalizing the words
STEMMER = stemmer.PorterStemmer()

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
	return {author: num for author, num in papers.items() if num >= min_num}

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
	return {key: val for key, val in ngrams.items() if val >= min_num}

def get_authors_for_topic(bibitems, topic):
	"""Get all authors writing about a certain topic.
	"""
	authors = set()
	for item in bibitems:
		#TODO use stemming, like above, maybe move to separate function
		title_words = WORDS_PATTERN.findall(item.title.lower())
		if topic in title_words:
			authors.update(item.authors)
	return authors

# testing
if __name__ == "__main__":
	from pprint import pprint
	import bib_parser
	items = bib_parser.parse_bib_from_bibtex("literature.bib")
	pprint(get_coauthors(items))
	pprint(sorted(get_title_ngrams(items, 1, 1).items(), key=lambda x: x[1]))
	pprint(get_papers_per_author(items, 5))
	pprint(get_authors_for_topic(items, "petri"))
