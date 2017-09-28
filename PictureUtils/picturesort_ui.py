#!/usr/bin/env python
# -*- coding: utf8 -*-

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
- show thumbnail in tooltip on mouseover
- port to python 3
- merge with PictureRank to enable bulk-rename of ranked pictures
"""

import Tkinter as tkinter
import tkFileDialog as filedialog
import tkSimpleDialog as simpledialog
import tkMessageBox as messagebox
from PIL import Image, ImageTk
import os
from pictureutil import auto_rotate

IMG_EXTENSIONS = "jpg", "jpeg", "png", "gif"


class PictureSortUI(tkinter.Frame):
	"""Picture Sort Frame.
	
	Simple UI for sorting pictures. Shows list of pictures in current
	directory, button for selecting the directory, button for renaming
	pictures, and a large preview of the currently selected picture.
	"""
	
	def __init__(self, master, size, directory=None):
		"""Create PictureSortUI instance, containing list of image files,
		large preview, and some buttons for re-ordering and renaming.
		"""
		tkinter.Frame.__init__(self, master)
		self.master.title("Picture Sorter")
		self.images = {}
		self.size = size
		self.directory = directory
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
				activestyle='dotbox', selectmode="extended",
				yscrollcommand=scrollbar.set)
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

		self.bind_all("<KeyRelease-q>", lambda e: self.quit())
		self.open_directory(False)

	def move(self, delta):
		"""Move selected list elements by delta positions (positive means
		down) and sets selection to the new positions.
		"""
		index = self.piclist.curselection()
		if index:
			first, last = int(index[0]), int(index[-1])  # could be the same
			if 0 <= first + delta and last + delta < self.piclist.size():
				selection = self.piclist.get(first, last)
				self.piclist.delete(first, last)
				self.piclist.insert(first + delta, *selection)
				self.piclist.select_set(first + delta, last + delta)

	def open_directory(self, ask=True):
		"""Ask user for directory and show all the image files within in
		the list, replacing any that were there before.
		"""
		if ask:
			self.directory = filedialog.askdirectory() or self.directory
			self.images.clear()
		if self.directory:
			pictures = [pic for pic in next(os.walk(self.directory))[2]
							 if pic.split(".")[-1].lower() in IMG_EXTENSIONS]

			self.piclist.delete(0, "end")
			for i, pic in enumerate(sorted(pictures)):
				self.piclist.insert(i, pic)

	def bulk_rename(self):
		"""Ask for pictures' common name, then bulk-rename all the files
		to "<name>_%03d.<ext>". This renames all the files twice, first
		using some temp names in the form "~<current-name>" to avoid name
		clashes. If multiple files are selected in the list, there's also
		the option to bulk-rename only those selected files.
		"""
		# get selection before dialog clears it
		sel = self.piclist.curselection()
		# ask for pattern in generic input dialog
		pattern = simpledialog.askstring("Rename", "Name to use for bulk rename:",
				initialvalue=self.pattern)
		if pattern is not None:
			self.pattern = pattern

			# rename all pictures or just selected?
			all_pictures = self.piclist.get(0, "end")
			if len(sel) > 1 and messagebox.askyesno("Rename", "Rename selected files only?"):
				pictures = self.piclist.get(sel[0], sel[-1])
				keep = set(all_pictures) - set(pictures)
			else:
				pictures, keep = all_pictures, set()

			temp_pics = ["~" + pic for pic in pictures]
			new_names = ["%s_%03d%s" % (pattern, i, os.path.splitext(pic)[1])
			             for i, pic in enumerate(temp_pics, start=1)]

			try:
				if any(x in keep for x in temp_pics) or any(x in keep for x in new_names):
					raise Exception("Bulk-Rename would result in duplicate names.")

				# rename in two passes to prevent name clashes
				for pic, temp in zip(pictures, temp_pics):
					os.rename(self.path(pic), self.path(temp))
				for temp, new_pic in zip(temp_pics, new_names):
					os.rename(self.path(temp), self.path(new_pic))

				# reload directory
				self.open_directory(False)
			except Exception as e:
				messagebox.showerror(title="Error", message=str(e))

	def path(self, f):
		"""Get full path for given file, relative to parent directory.
		"""
		return os.path.join(self.directory, f)
	
	def show_preview(self, event):
		"""Get currently selected picture from list, if any, and show it
		in the preview.
		"""
		index = self.piclist.curselection()
		if index:
			selection = self.piclist.get(index[0])
			self.preview.delete("all")
			x, y = self.preview.winfo_width() / 2, self.preview.winfo_height() / 2
			self.preview.create_image((x, y), image=self.load_image(selection))
			
	def load_image(self, pic):
		"""Load the given picture using imaging library. Images are cached.
		"""
		if pic not in self.images:
			path = self.path(pic)
			img = auto_rotate(Image.open(path))
			img.thumbnail((self.size, self.size))
			self.images[pic] = ImageTk.PhotoImage(img)
		return self.images[pic]


def main():
	import optparse
	root = tkinter.Tk()

	# parse and check command line options
	parser = optparse.OptionParser("picturesort_ui.py [Options] [Directory]")
	parser.add_option("-s", "--size", dest="size",
					  help="size of image previews")
	(options, args) = parser.parse_args()

	size = int(options.size or 500)
	directory = args[0] if args else None

	PictureSortUI(root, size, directory)
	root.mainloop()
	
if __name__ == "__main__":
	main()

