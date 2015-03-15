#!/usr/bin/python

"""Evolution Strategy based Color Chooser Application
by Tobias Kuester, 2010

The idea behind this program is to use a very simple form of Evolution Strategy
for modifying a color sample until it fits ones needs without having to care
about what exact hue, saturation, or whatever the desired color needs to have.

Usage:
- start application
- select starting color
- click the color that best matches your expectation
- repeat until desired colour appears
"""

import Tkinter, tkColorChooser, random

class ESColorChooserFrame(Tkinter.Frame):
	"""Application Frame for ES Color Chooser
	
	The Frame consists mainly of a matrix of colored panels. By clicking on
	one of the panels a new set of colors is generated by randomly modifying
	the selected color. A side panel provides some additional widgets.
	"""
	
	def __init__(self, master=None):
		""" create Color Chooser Application Frame """
		Tkinter.Frame.__init__(self, master)
		self.master.title('ES Color Chooser')
		self.grid()
		
		# create central block of color samples
		self.labels = [ [ None for x in range(0,3)] for y in range(0,3)]
		for (x, y) in [ (x, y) for x in range(0,3) for y in range(0,3)]:
			label = Tkinter.Label(self, width=20, height=10, bg='#FFFFFF')
			label.bind('<ButtonRelease-1>', self.clicked)
			label.grid(column=x, row=y, padx=1, pady=1)
			self.labels[y][x] = label
		self.center = self.labels[1][1]
		
		# create side pane with buttons and history
		side = Tkinter.Frame(self)
		side.grid(row=0, column=3, rowspan=3)
		Tkinter.Button(side, text='Select new Color', command=self.select_color).pack(side='top')
		self.sigma = Tkinter.Scale(side, label='Sigma', orient='horizontal', from_=1, to=25)
		self.sigma.pack(side='top')
		self.sigma.set(10)
		Tkinter.Label(side, text='Current color').pack(side='top')
		self.current = Tkinter.StringVar()
		current = Tkinter.Entry(side, justify='center', textvariable=self.current)
		current.pack(side='top')
		Tkinter.Label(side, text='History').pack(side='top')
		self.history = Tkinter.Listbox(side, height='16', bg='white', activestyle='dotbox')
		self.history.bind('<ButtonRelease-1>', self.clicked)
		self.history.pack(side='top')
			
	def select_color(self):
		""" ask for new color and assign it to the central panel """
		result = tkColorChooser.askcolor(self.center['bg'])
		if result:
			# 2nd part of result is the color object
			self.center['bg'] = result[1]

	def next_generation(self, color):
		""" calculate next generation with given color and set new panel colors """
		# add color to history
		self.current.set(color)
		if not color in self.history.get(0, self.history.size()):
			self.history.insert(0, color)
			self.history.itemconfig(0, background=color)
		# calculate new generation of colors
		for (x, y) in [ (x, y) for x in range(0,3) for y in range(0,3)]:
			label = self.labels[y][x]
			label['bg'] = modify_color(color, self.sigma.get())
		self.center['bg'] = color

	def clicked(self, event=None):
		""" handle mouse click events, deledate to specialized methods """
		if event.widget == self.history:
			selection = self.history.curselection()
			if selection:
				self.next_generation(self.history.get(selection))
		else:
			self.next_generation(event.widget['bg'] )


def vary(n, sigma):
	""" vary number with given sigma, return integer between 0 and 255 """
	v= random.gauss(n, sigma)
	return min(255, max(0, v))	
	
def modify_color(color, sigma):
	""" modify color given in HTML notation with sigma """
	# get values of individual colors, convert to hex integers
	r, g, b = color[1:3], color[3:5], color[5:]
	r, g, b = int(r, 16), int(g, 16), int(b, 16)
	# modify color using light evolution strategy
	r, g, b = vary(r, sigma), vary(g, sigma), vary(b, sigma)
	# return combined hex representation of new color values
	return '#%02X%02X%02X' % ( r, g, b )


# start application
if __name__ == '__main__':
	app = ESColorChooserFrame()
	app.mainloop()

