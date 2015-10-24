import os.path
import random
import collections
import json

JSON_FILENAME = "picture-rank.json"
IMG_EXTENSIONS = "jpg", "jpeg", "png", "gif"
DEFAULT_RANK = 100

class PictureRank:
	
	def __init__(self, directory):
		self.directory = directory
		self.pictures = [pic for pic in next(os.walk(directory))[2]
		                 if pic.split(".")[-1].lower() in IMG_EXTENSIONS]
		self.ranks = collections.defaultdict(lambda: DEFAULT_RANK)
		if os.path.exists(self.path(JSON_FILENAME)):
			with open(self.path(JSON_FILENAME), "r") as f:
				old_ranks = json.load(f)
				self.ranks.update(old_ranks)

	def __del__(self):
		if self.ranks:
			with open(self.path(JSON_FILENAME), "w") as f:
				json.dump(self.ranks, f)
		
	def get_random_pair(self):
		return [random.choice(self.pictures) for _ in range(2)]

	def path(self, f):
		return os.path.join(self.directory, f)

	def rank(self, pic, value=None):
		if value:
			self.ranks[pic] = value
		return self.ranks[pic]

	def update_rank(self, pic1, pic2, outcome):
		self.ranks[pic1] -= outcome
		self.ranks[pic2] += outcome
		
	def get_best(self, number=None):
		ranking = sorted(self.ranks.items(), key=lambda x: x[1], reverse=True)
		return ranking[slice(number)]
		

def test():
	directory = "/home/tkuester/TEST"
	picrank = PictureRank(directory)
	
if __name__ == "__main__":
	test()