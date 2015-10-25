"""Picture Rank model.
by Tobias Kuester, 2015

UI independent parts of the Picture Rank util: Finding all the pictures in a
given directory and, most importantly, the algorithms for randomly selecting
pairs of pictures and for ranking the pictures against each other, as well as
the data structures holding the pictures and their ranking itself.
"""

import os.path
import random
import json

JSON_FILENAME = "picture-rank.json"
IMG_EXTENSIONS = "jpg", "jpeg", "png", "gif"
DEFAULT_RANK = 1200

class PictureRank:
	"""Picture Rank class.
	
	This class contains the data structure holding the current rankings and the
	algorithms for selecting the next tournament pair and for updating ranks.
	"""
	
	def __init__(self, directory):
		"""Get all image files from given directory and initialize ranking. If
		exists, update ranking with those from previous execution.
		"""
		self.directory = directory
		self.pictures = dict((pic, DEFAULT_RANK) for pic in next(os.walk(directory))[2]
		                 if pic.split(".")[-1].lower() in IMG_EXTENSIONS)
		# load previous rankings from file, if they exist
		if os.path.exists(self.path(JSON_FILENAME)):
			with open(self.path(JSON_FILENAME), "r") as f:
				old_ranks = json.load(f)
				self.pictures.update(old_ranks)

	def __del__(self):
		"""On exit, write current rankings to file."""
		if self.pictures:
			with open(self.path(JSON_FILENAME), "w") as f:
				json.dump(self.pictures, f)
		
	def get_random_pair(self):
		"""Get random pair of pictures for next tournament."""
		return [random.choice(self.pictures.keys()) for _ in range(2)]

	def path(self, f):
		"""Get full path for given file, relative to parent directory."""
		return os.path.join(self.directory, f)

	def rank(self, pic, value=None):
		"""Get or set the rank for the given pictures."""
		if value:
			self.pictures[pic] = value
		return self.pictures[pic]

	def update_rank(self, pic1, pic2, outcome):
		"""Update the ranks for the given two pictures, based on the outcome.
		Outcome relative to pic1: 1.0: won; 0.5: draw; 0.0: lost.
		Based on formula from https://de.wikipedia.org/wiki/Elo-Zahl#Berechnung
		"""
		K = 20
		r1, r2 = self.pictures[pic1], self.pictures[pic2]
		e1 = 1. / (1 + 10**((r2 - r1)/400))
		s1 = outcome
		self.pictures[pic1] += K * (s1 - e1)
		self.pictures[pic2] += K * (e1 - s1)
		
	def get_best(self, number=None):
		"""Get N best pictures, sorted by their rank."""
		ranking = sorted(self.pictures.items(), key=lambda x: x[1], reverse=True)
		return ranking[slice(number)]
