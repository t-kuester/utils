
import json
import time


class Interval:
	DAY = "DAY"
	WEEK = "WEEK"
	MONTH = "MONTH"
	YEAR = "YEAR"


class Activity:
	
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
		t = time.time()
		print "logged", time.ctime(t)
		self.history.append(t)
	
	def get_counts(self):
		pass
		# TODO timestamps in dates umwandeln; mit groupby nach interval
		# gruppieren, laenge bestimmen und in liste eintragen 
		# --> vorsicht mit leeren intervallen! nicht einfach vergessen


def load_activities(filename):
	with open(filename) as f:
		lst = json.load(f)
		return [Activity(**d) for d in lst]


def store_activities(activities, filename):
	with open(filename, "w") as f:
		lst = [act.__dict__ for act in activities]
		json.dump(lst, f)
	

if __name__ == "__main__":
	
	a1 = Activity("a1", "test activity 1", Interval.WEEK, 2)
	a2 = Activity("a2", "test activity 2", Interval.DAY, 1)
	print a1
	print a2
	
	store_activities([a1, a2], "test.json")
	a3, a4 = load_activities("test.json")
	print a3
	print a4
