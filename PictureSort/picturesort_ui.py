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
- make preview resizeable (and update cached images)
- show thumbnail in list
- scroll list to selection
- port to python 3
- merge with PictureRank to enable bulk-rename of ranked pictures
"""

import Tkinter as tkinter
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import tkMessageBox as messagebox
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
		self.images = {}
		self.size = size
		self.directory = None
		self.pattern = "Untitled"
		self.grid()
		
		# image preview
		self.preview = tkinter.Canvas(self, width=size, height=size)
		self.preview.grid(row=0, column=3, rowspan=3, sticky="nsew")
		
		# list of pictures, in scroll-frame
		frame = tkinter.Frame(self)
		frame.grid(row=0, column=0, columnspan=2, sticky="ns")
		scrollbar = tkinter.Scrollbar(frame, orient="vertical")
		self.piclist = tkinter.Listbox(frame, height='16', bg='white', 
				activestyle='dotbox', yscrollcommand=scrollbar.set)
		self.piclist.bind('<ButtonRelease-1>', self.show_preview)
		self.piclist.bind("<KeyRelease>", self.show_preview)
		self.piclist.pack(side="left", fill="both", expand=1)
		scrollbar.config(command=self.piclist.yview)
		scrollbar.pack(side="right", fill="y")

		# open directory button
		b_open = tkinter.Button(self, text="Open", command=self.open_directory)
		b_open.grid(row=1, column=0, sticky="nsew")
		
		# move up button
		b_up = tkinter.Button(self, text="Move up", command=lambda: self.move(-1))
		b_up.grid(row=1, column=1, sticky="nsew")
		
		# move down button
		b_down = tkinter.Button(self, text="Move down", command=lambda: self.move(+1))
		b_down.grid(row=2, column=1, sticky="nsew")
		
		# bulk rename button
		b_rename = tkinter.Button(self, text="Rename", command=self.bulk_rename)
		b_rename.grid(row=2, column=0, sticky="nsew")
		

	def move(self, direction):
		index = int(self.piclist.curselection()[0])
		other = index + direction
		both = (index, other)
		if 0 <= other < self.piclist.size():
			selection = self.piclist.get(index)
			other_pic = self.piclist.get(other)
			reverse = (selection, other_pic) if index > other else (other_pic, selection)

			self.piclist.delete(*sorted(both))
			self.piclist.insert(min(both), *reverse)
			self.piclist.select_set(other)
				
	def open_directory(self, ask=True):
		if ask:
			self.directory = filedialog.askdirectory()
		if self.directory:
			pictures = [pic for pic in next(os.walk(self.directory))[2]
							 if pic.split(".")[-1].lower() in IMG_EXTENSIONS]

			self.piclist.delete(0, self.piclist.size())
			for i, pic in enumerate(sorted(pictures)):
				self.piclist.insert(i, pic)

	def bulk_rename(self):
		# ask for pattern in generic input dialog
		pattern = simpledialog.askstring("Rename", "Name to use for bulk rename:",
				initialvalue=self.pattern)
		if pattern is not None:
			self.pattern = pattern
			pictures = self.piclist.get(0, self.piclist.size())
			temp_pics = ["~" + pic for pic in pictures]

			try:
				# rename in two passes to prevent name clashes
				for pic, temp in zip(pictures, temp_pics):
					os.rename(self.path(pic), self.path(temp))
				for i, pic in enumerate(temp_pics, start=1):
					name, ext = os.path.splitext(pic)
					new_name = "%s_%03d%s" % (self.pattern, i, ext)
					os.rename(self.path(pic), self.path(new_name))

				# reload directory
				self.open_directory(False)
			except Exception as e:
				messagebox.showerror(title="Error", message=str(e))

	def path(self, f):
		"""Get full path for given file, relative to parent directory."""
		return os.path.join(self.directory, f)
	
	def show_preview(self, event):
		index = self.piclist.curselection()
		if index:
			selection = self.piclist.get(index)
			self.preview.delete("all")
			x, y = self.preview.winfo_width() / 2, self.preview.winfo_height() / 2
			self.preview.create_image((x, y), image=self.load_image(selection))
			
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
	PictureSortUI(root, 500)
	root.mainloop()
	
if __name__ == "__main__":
	main()
	
