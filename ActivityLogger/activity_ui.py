from Tkinter import *
from activity_model import *

class ActivityFrame(Frame):
	
	def __init__(self, activities, master=None):
		Frame.__init__(self, master)
		self.activities = activities
		for act in self.activities:
			panel = ActivityPanel(self, act)
			panel.pack(side=TOP)
		self.pack()


class ActivityPanel(Canvas):
	
	def __init__(self, parent, activity):
		Canvas.__init__(self, parent)
		self.activity = activity
		
		self.canvas = Canvas(self, width=200, height=50)
		self.canvas.pack(side=LEFT)
		
		self.log_button = Button(self, text="LOG", relief=FLAT, command=self.log_now)
		self.log_button.pack(side=RIGHT)
		
	def log_now(self):
		self.activity.log_now()


if __name__ == "__main__":
	activities = load_activities("test.json")
	frame = ActivityFrame(activities)
	frame.mainloop()
	store_activities(activities, "test.json")
