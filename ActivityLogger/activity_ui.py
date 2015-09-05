from activity_model import *
import tkinter
import tkinter.font as font


class ActivityFrame(tkinter.Frame):
	""" Simple Tkinter Frame for displaying and interacting with activity list.
	"""
	
	def __init__(self, activities, master=None):
		tkinter.Frame.__init__(self, master)
		self.activities = activities
		for act in self.activities:
			panel = ActivityPanel(self, act)
			panel.pack(side=tkinter.TOP)
		self.pack()
		self.bind_all("<KeyPress-q>", lambda e: self.quit())


class ActivityPanel(tkinter.Canvas):
	""" Panel for showing, editing and logging an individual activity.
	"""

	def __init__(self, parent, activity):
		tkinter.Canvas.__init__(self, parent)
		self.activity = activity
		
		self.canvas = tkinter.Canvas(self, width=200, height=50)
		self.canvas.pack(side=tkinter.LEFT)
		
		#TODO button 'stats'
		#TODO button 'edit'
		
		self.log_button = tkinter.Button(self, text="LOG", relief=tkinter.FLAT, command=self.log_now)
		self.log_button.pack(side=tkinter.RIGHT)
		
		self.font_name = font.Font(family="Helvetica", size=12)
		self.font_desc = font.Font(family="Helvetica", size=8)
		
		self.update_visuals()
		
	def update_visuals(self):
		""" Update the information displayed on the canvas.
		"""
		self.canvas.delete("all")
		self.canvas.create_text(2, 2, text=self.activity.name, font=self.font_name, anchor=tkinter.NW)
		self.canvas.create_text(200, 2, text="%d/%s" % (self.activity.required, self.activity.interval.title()), font=self.font_desc, anchor=tkinter.NE)
		self.canvas.create_text(2, 20, text=self.activity.description, font=self.font_desc, anchor=tkinter.NW)
		counts = self.activity.get_counts()
		for i, c in enumerate(reversed(counts[-20:]), 1):
			x = 200 - i * 10
			color = "#00ff00" if c >= self.activity.required else ("#ff0000" if i > 1 else "#ffff00")
			self.canvas.create_rectangle(x, 40, x + 6, 46, outline=color, fill=color)
		
	def log_now(self):
		""" Log this activity as having been performed right now.
		"""
		self.activity.log_now()
		self.update_visuals()


class EditActivityDialog:
	""" Dialog for editing the details of an activity.
	"""
	# TODO
	pass


if __name__ == "__main__":
	activities = load_activities("test.json")
	frame = ActivityFrame(activities)
	frame.mainloop()
	# store_activities(activities, "test.json")
