import json
import time
import random
import itertools
import datetime

class Interval:
	""" 'Enumeration' of different time intervals
	"""
	DAY = "DAY"
	WEEK = "WEEK"
	MONTH = "MONTH"
	YEAR = "YEAR"

FORMATS = {Interval.YEAR: "%Y", Interval.MONTH: "%Y-%m", 
		   Interval.WEEK: "%Y-%W", Interval.DAY: "%Y-%j"}


class Activity:
	""" Class describing an activity. This includes some information about the
	activity as well as how many instances of this activity to perform in what
	time interval, and when this activity has actually been carried out.
	"""
	
	def __init__(self, name, description, created, interval, required=1, history=None):
		self.name = name
		self.description = description
		self.created = created
		self.interval = interval
		self.required = required
		self.history = history or []
	
	def __repr__(self):
		return "Activity(name=%r, description=%r, created=%r, interval=%r, required=%r, history=%r)" \
				% (self.name, self.description, self.created, self.interval, self.required, self.history)
	
	def log_now(self):
		""" Add the current date and time to the activity's history.
		"""
		t = time.time()
		print "logged", time.ctime(t)
		self.history.append(t)

	def format_interval(self, date):
		return date.strftime(FORMATS[self.interval])

	def group_intervals(self):
		get_interval = lambda t: self.format_interval(datetime.date.fromtimestamp(t))
		return [(k, map(time.ctime, g)) for k, g in itertools.groupby(self.history, get_interval)]

	def all_intervals(self):
		all_intervals = set()
		t = datetime.date.fromtimestamp(self.created)
		tomorrow = datetime.date.today() + datetime.timedelta(days=1)
		while t < tomorrow:
			all_intervals.add(self.format_interval(t))
			t += datetime.timedelta(days=1)
		return all_intervals
	
	def get_counts(self):
		""" Calculate how often this activity has been performed in each time
		interval based on the timestamps from the history.
		"""
		groups_map = dict((k, len(g)) for k, g in self.group_intervals())
		return [groups_map.get(i, 0) for i in sorted(self.all_intervals())]
	

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
	created = time.time() - 2000000
	a1 = Activity("Some activity 1", "Description for activity 1", created, Interval.WEEK, 2)
	a2 = Activity("Some other activity 2", "Some bla bla about activity 2", created, Interval.DAY, 1)
	print a1
	print a2
	
	t = time.time()
	a1.history.extend(sorted([t - 60 * 60 * 24 * random.randint(1, 100) for i in range(20)]))
	
	store_activities([a1, a2], "test.json")
	a3, a4 = load_activities("test.json")
	print a3
	print a4

	for c in a3.get_counts():
		print c