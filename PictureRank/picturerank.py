import glob
import os.path
import random
import collections

class PictureRank:
	
	def __init__(self, directory):
		self.directory = directory
		
		self.files = {}
		self.ranks = collections.defaultdict(lambda: 100)
		
		self.pictures = [os.path.split(p)[-1] for p in glob.glob(directory + "/*")]
		
		print(self.pictures)

	# def __del__(self):
		# for f in self.files:
			# f.close()
		
	def get_random_pair(self):
		return [random.choice(self.pictures) for _ in range(2)]

	def path(self, pic):
		return os.path.join(self.directory, pic)

	# def load(self, pic):
		# if pic not in self.files:
			# path = os.path.join(self.directory, pic)
			# self.files[pic] = open(path)
		# return self.files[pic]
		
	def rank(self, pic, value=None):
		if value:
			self.ranks[pic] = value
		return self.ranks[pic]

	def update_rank(self, pic1, pic2, outcome):
		self.ranks[pic1] -= outcome
		self.ranks[pic2] += outcome
		

def test():
	directory = "/home/tkuester/TEST"
	picrank = PictureRank(directory)
	
if __name__ == "__main__":
	test()