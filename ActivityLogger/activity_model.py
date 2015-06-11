import json
import time


class Interval:
	""" 'Enumeration' of different time intervals
	"""
	DAY = "DAY"
	WEEK = "WEEK"
	MONTH = "MONTH"
	YEAR = "YEAR"


class Activity:
	""" Class describing an activity. This includes some information about the
	activity as well as how many instances of this activity to perform in what
	time interval, and when this activity has actually been carried out.
	"""
	
	def __init__(self, name, description, interval, required=1, history=None):
		self.name = name
		self.description = description
		self.interval = interval
		self.required = required
		self.history = history or []
	
	def __repr__(self):
		return "Activity(name=%r, description=%r, interval=%r, required=%r, history=%r)" \
				% (self.name, self.description, self.interval, self.required, self.history)
	
	def log_now(self):
		""" Add the current date and time to the activity's history.
		"""
		t = time.time()
		print "logged", time.ctime(t)
		self.history.append(t)
	
	def get_counts(self):
		""" Calculate how often this activity has been performed in each time
		interval based on the timestamps from the history.
		"""
		import random
		return [random.randint(0, self.required * 2) for i in range(random.randint(10, 30))]
		# TODO timestamps in dates umwandeln; mit groupby nach interval
		# gruppieren, laenge bestimmen und in liste eintragen 
		# --> vorsicht mit leeren intervallen! nicht einfach vergessen


def load_activities(filename):
	""" Load activities from JSON file.
	"""
	with open(filename) as f:
		lst = json.load(f)
		return [Activity(**d) for d in lst]


def store_activities(activities, filename):
	""" Stora activities in JSON file.
	"""
	with open(filename, "w") as f:
		lst = [act.__dict__ for act in activities]
		json.dump(lst, f)
	


if __name__ == "__main__":
	
	a1 = Activity("Some activity 1", "Description for activity 1", Interval.WEEK, 2)
	a2 = Activity("Some other activity 2", "Some bla bla about activity 2", Interval.DAY, 1)
	print a1
	print a2
	
	store_activities([a1, a2], "test.json")
	a3, a4 = load_activities("test.json")
	print a3
	print a4
