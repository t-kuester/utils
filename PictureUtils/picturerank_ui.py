#!/usr/bin/env python

"""Picture Rank UI
by Tobias Kuester, 2015

UI-specific parts of the Picture Rank util: A simple GUI showing two pictures
next to each other and the current ranking of allpictures, with keyboard and
mouse controls. Also stuff for starting the application.
"""

import Tkinter as tkinter
import tkFileDialog as filedialog
import picturerank
from PIL import Image, ImageTk
from pictureutil import auto_rotate

DELIMITER = " - "

class PictureRankUI(tkinter.Frame):
	"""Picture Rank Frame.
	
	Simple UI for the picture ranking util, showing two pictures side-by-side, a
	list showing the current rankings and providing keyboard and mouse controls.
	"""
	
	def __init__(self, master, ranker, size):
		"""Create picture ranking frame instance, creating two labels for the
		pictures and a listbox for the ranking. The UI is controlled via arrow
		keys, and pictures can be selected from the list using the mouse.
		"""
		tkinter.Frame.__init__(self, master)
		self.master.title("Picture Rank")
		self.grid()
		self.ranker = ranker
		self.current = None
		self.images = {}
		self.size = size

		self.label1 = tkinter.Label(self, width=size, height=size)
		self.label1.bind("<ButtonRelease>", lambda e: self.select(1.0))
		self.label1.grid(row=0, column=0)
		
		self.label2 = tkinter.Label(self, width=size, height=size)
		self.label2.bind("<ButtonRelease>", lambda e: self.select(0.0))
		self.label2.grid(row=0, column=1)
		
		self.bind_all("<KeyRelease>", self.handle_keys)

		self.ranking = tkinter.Listbox(self, height='25', selectmode='single')
		self.ranking.bind('<ButtonRelease>', self.from_ranking)
		self.ranking.grid(row=0, column=2)
		
		self.set_random_images()
		self.update_ranking()
	
	def handle_keys(self, event):
		"""Handle key events for advancing the tournament and other stuff.
		Left/Right: select better picture; Up/Down: skip (draw); q: quit
		"""
		if event.keysym == "q":
			del self.ranker
			self.quit()
		if event.keysym == "Left":
			self.select(1.0)
		if event.keysym == "Right":
			self.select(0.0)
		if event.keysym in ("Up", "Down"):
			self.select(0.5)

	def select(self, outcome):
		"""Callback for when one of the pictures has been selected. Updates the
		ranks and ranking list and loads the next pair of pictures.
		"""
		if self.current:
			pic1, pic2 = self.current
			self.ranker.update_rank(pic1, pic2, outcome)
		self.set_random_images()
		self.update_ranking()
		
	def update_ranking(self):
		"""Update the ranking list showing the current ranks, sorted from best
		to worst. The two pictures currently shown are highlighted.
		"""
		ranking = self.ranker.get_best()
		self.ranking.delete(0, len(ranking))
		for i, (pic, rank) in enumerate(ranking):
			self.ranking.insert(i, "%d%s%s" % (rank, DELIMITER, pic))
			if pic in self.current:
				self.ranking.itemconfigure(i, bg="yellow")
		
	def from_ranking(self, event):
		"""Callback for showing pictures from the rankings list. LMB will show
		the picture in the left label, and RMB will show it in the right label.
		"""
		pic1, pic2 = self.current
		selection = self.ranking.get(self.ranking.nearest(event.y))
		pic_sel = selection.split(DELIMITER, 1)[1]
		if event.num == 1:
			self.set_images(pic_sel, pic2)
		if event.num == 3:
			self.set_images(pic1, pic_sel)
			
	def set_random_images(self):
		"""Get random pair of images for next tournament and show them."""
		pic1, pic2 = self.ranker.get_random_pair()
		self.set_images(pic1, pic2)
		
	def set_images(self, pic1, pic2):
		"""Show the given pictures in the two labels."""
		self.label1.configure(image=self.load_image(pic1))
		self.label2.configure(image=self.load_image(pic2))
		self.current = pic1, pic2
		
	def load_image(self, pic):
		"""Load the given picture using imaging library. Images are cached."""
		if pic not in self.images:
			path = self.ranker.path(pic)
			img = auto_rotate(Image.open(path))
			img.thumbnail((self.size, self.size))
			self.images[pic] = ImageTk.PhotoImage(img)
		return self.images[pic]


def main():
	"""Parse command line parameters and run application.
	"""
	import optparse
	root = tkinter.Tk()

	# parse and check command line options
	parser = optparse.OptionParser("picturerank_ui.py [Options] [Directory]")
	parser.add_option("-s", "--size", dest="size", 
					  help="size of image previews")
	(options, args) = parser.parse_args()
	
	size = int(options.size) if options.size else 400
	directory = args[0] if args else filedialog.askdirectory()

	ranker = picturerank.PictureRank(directory)
	PictureRankUI(root, ranker, size)
	root.mainloop()
	
if __name__ == "__main__":
	main()
