from activity_model import *
from Tkinter import *
import tkFont


class ActivityFrame(Frame):
	""" Simple Tkinter Frame for displaying and interacting with activity list.
	"""
	
	def __init__(self, activities, master=None):
		Frame.__init__(self, master)
		self.activities = activities
		for act in self.activities:
			panel = ActivityPanel(self, act)
			panel.pack(side=TOP)
		self.pack()
		self.bind_all("<KeyPress-q>", lambda e: self.quit())


class ActivityPanel(Canvas):
	""" Panel for showing, editing and logging an individual activity.
	"""

	def __init__(self, parent, activity):
		Canvas.__init__(self, parent)
		self.activity = activity
		
		self.canvas = Canvas(self, width=200, height=50)
		self.canvas.pack(side=LEFT)
		
		#TODO button 'stats'
		#TODO button 'edit'
		
		self.log_button = Button(self, text="LOG", relief=FLAT, command=self.log_now)
		self.log_button.pack(side=RIGHT)
		
		self.font_name = tkFont.Font(family="Helvetica", size=12)
		self.font_desc = tkFont.Font(family="Helvetica", size=8)
		
		self.update_visuals()
		
	def update_visuals(self):
		""" Update the information displayed on the canvas.
		"""
		self.activity.name = "aaaaaaaaaaaa"
		self.canvas.delete("all")
		self.canvas.create_text(2, 2, text=self.activity.name, font=self.font_name, anchor=NW)
		self.canvas.create_text(2, 20, text=self.activity.description, font=self.font_desc, anchor=NW)
		counts = self.activity.get_counts()
		for i, c in enumerate(reversed(counts[-20:]), 1):
			x = 200 - i * 10
			color = "#00ff00" if c > self.activity.required else "#ff0000"
			self.canvas.create_rectangle(x, 40, x + 6, 46, outline=color, fill=color)
		
	def log_now(self):
		""" Log this activity as having been performed right now.
		"""
		self.activity.log_now()
		self.update_visuals()



if __name__ == "__main__":
	activities = load_activities("test.json")
	frame = ActivityFrame(activities)
	frame.mainloop()
	store_activities(activities, "test.json")
