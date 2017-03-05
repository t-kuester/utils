#!/usr/bin/env python

"""Picture Sort UI
by Tobias Kuester, 2017

Simple utility program for sorting and bulk-renaming pictures in a folder.
Usually, pictures are already sorted in order of time taken by the camera,
but in some cases they are not, e.g. when having a large body of scanned
paper images, or when merging pictures taken with different digital cameras
(possibly with diverging date/time settings).

Pictures are shown in a list and can be rearanged freely in that list
(which is often not possible in file managers). Then, all the pictures
can be renamed consistently.

TODO
- improve UI layout
- make preview resizeable (and update cached images)
- show thumbnail in list
- show scrollbars in list
- ask for common name/pattern
- keyboard control for moving pictures
- keep selection in list when moving pictures
- port to python 3
- merge with PictureRank to enable bulk-rename of ranked pictures
"""

import Tkinter as tkinter
import tkFileDialog as filedialog
from PIL import Image, ImageTk
import os

IMG_EXTENSIONS = "jpg", "jpeg", "png", "gif"


class PictureSortUI(tkinter.Frame):
	"""Picture Sort Frame.
	
	Simple UI for sorting pictures. Shows list of pictures in current
	directory, button for selecting the directory, button for renaming
	pictures, and a large preview of the currently selected picture.
	"""
	
	def __init__(self, master, size):
		tkinter.Frame.__init__(self, master)
		self.master.title("Picture Sorter")
		self.current = None
		self.images = {}
		self.size = size
		self.directory = None
		self.pattern = "Untitled_%03d"
		#~ self.grid()
		self.pack()
		
		# image preview
		self.preview = tkinter.Label(self, text="PREVIEW", width=size, height=size)
		#~ self.preview.grid(row=0, column=3, rowspan=4)
		self.preview.pack(side="right", fill="both")
		
		# list of pictures
		self.piclist = tkinter.Listbox(self, height='16', bg='white', activestyle='dotbox')
		self.piclist.bind('<ButtonRelease-1>', self.show_preview)
		#~ self.piclist.grid(row=1, column=0, columnspan=2)
		self.piclist.pack(side="top", fill="x")

		# open directory button
		b_open = tkinter.Button(self, text="Open", command=self.open_directory)
		#~ b_open.grid(row=0, column=0, columnspan=2)
		b_open.pack(fill="y")
		
		# move up button
		b_up = tkinter.Button(self, text="Move up", command=lambda: self.move(-1))
		#~ b_up.grid(row=3, column=0)
		b_up.pack(fill="y")
		
		# move down button
		b_down = tkinter.Button(self, text="Move down", command=lambda: self.move(+1))
		#~ b_down.grid(row=3, column=1)
		b_down.pack(fill="y")
		
		# bulk rename button
		b_rename = tkinter.Button(self, text="Rename", command=self.bulk_rename)
		#~ b_rename.grid(row=4, column=0, columnspan=2)
		b_rename.pack(fill="y")
		
		self.bind_all("<KeyRelease>", self.handle_keys)
		
	def handle_keys(self, event):
		if event.keysym == "q":
			self.quit()
		if event.keysym == "Up":
			self.move(-1)
		if event.keysym == "Down":
			self.move(+1)

	def move(self, direction):
		index = int(self.piclist.curselection()[0])
		other = index + direction
		both = (index, other)
		selection = self.piclist.get(index)
		other_pic = self.piclist.get(other)
		reverse = (selection, other_pic) if index > other else (other_pic, selection)
		
		self.piclist.delete(*sorted(both))
		self.piclist.insert(min(both), *reverse)
				
	def open_directory(self, ask=True):
		if ask:
			self.directory = filedialog.askdirectory()
		if self.directory:
			pictures = [pic for pic in next(os.walk(self.directory))[2]
							 if pic.split(".")[-1].lower() in IMG_EXTENSIONS]
							 
			for i, pic in enumerate(sorted(pictures)):
				self.piclist.insert(i, pic)
							 

	def bulk_rename(self):
		# TODO ask for pattern in generic input dialog
		
		pictures = self.piclist.get(0, self.piclist.size())
		temp_pics = ["~" + pic for pic in pictures]

		path = self.path
		
		for pic, temp in zip(pictures, temp_pics):
			os.rename(path(pic), path(temp))
		
		# rename in two passes to prevent name clashes
		for i, pic in enumerate(temp_pics, start=1):
			_, ext = os.path.splitext(pic)
			new_name = (self.pattern % i) + ext
			os.rename(path(pic), path(new_name))

		self.open_directory(False)
			

	def path(self, f):
		"""Get full path for given file, relative to parent directory."""
		return os.path.join(self.directory, f)
	
	def show_preview(self, event):
		selection = self.piclist.get(self.piclist.nearest(event.y))
		self.preview.configure(image=self.load_image(selection))
			
	def load_image(self, pic):
		"""Load the given picture using imaging library. Images are cached."""
		if pic not in self.images:
			path = self.path(pic)
			img = auto_rotate(Image.open(path))
			img.thumbnail((self.size, self.size))
			self.images[pic] = ImageTk.PhotoImage(img)
		return self.images[pic]


def auto_rotate(img):
	"""Auto-rotate image based on EXIF information; adapted from
	http://www.lifl.fr/~damien.riquet/auto-rotating-pictures-using-pil.html
	"""
	try:
		exif = img._getexif()
		orientation_key = 274 # cf ExifTags
		orientation = exif[orientation_key]
		rotate_values = {3: 180, 6: 270, 8: 90}
		img = img.rotate(rotate_values[orientation])
	finally:
		return img


def main():
	root = tkinter.Tk()
	PictureSortUI(root, 40)
	root.mainloop()
	
if __name__ == "__main__":
	main()
	
