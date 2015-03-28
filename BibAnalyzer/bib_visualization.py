# -*- coding: utf8 -*-

"""Visualization module for Bibliography Analyzer Utility.
by Tobias Küster, 2015

- create GraphViz graph showing co-author relationships
"""

import bib_analyzer
import subprocess

def create_authors_graph(bibitems, call_graphviz=False):
	"""Create a graph representing the co-author relationsships, using GraphViz.
	"""
	coauthors = bib_analyzer.get_coauthors(bibitems)
	with open("authors_graph.dot", "w") as g:
		g.write('graph "Co-Authors" {')
		for a1, a2 in coauthors:
			n = coauthors[(a1, a2)]
			style = (' [style="bold" label="x%d"]' % n) if n > 1 else ''
			g.write('\n\t "%s" -- "%s" %s;' % (a1, a2, style))
		g.write("}")
	if call_graphviz:
		subprocess.call("dot -Tps -o autoren.ps authors_graph.dot".split())


if __name__ == "__main__":
	import bib_parser
	items = bib_parser.parse_bib_from_bibtex("literature.bib")
	create_authors_graph(items, True)
