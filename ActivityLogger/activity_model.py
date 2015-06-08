
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
		self.counts = None
	
	def __repr__(self):
		return "Activity(name=%r, description=%r, interval=%r, required=%r, history=%r)" \
				% (self.name, self.description, self.interval, self.required, self.history)
	
	def get_counts(self):
		if self.counts is None:
			pass #TODO populate counts
			# TODO timestamps in dates umwandeln; mit groupby nach interval
			# gruppieren, laenge bestimmen und in liste eintragen 
			# --> vorsicht mit leeren intervallen! nicht einfach vergessen
		return self.counts


def load_activities(filename):
	pass
	# TODO use JSON to losd list of activities from file


def store_activities(activities, filename):
	pass
	# TODO use JSON to store list of activities to file


if __name__ == "__main__":
	
	a1 = Activity("a1", "test activity 1", Interval.WEEK, 2)
	print a1	
	
