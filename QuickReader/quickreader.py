#!/usr/bin/python

"""Quick Reader.
by Tobias Kuester, 2010

A screen reader for quickly 'scanning' long texts by briefly flashing the single
words on the screen.

Not really sure how well this works. Newer really tried on a longer text...
"""

import Tkinter
import ScrolledText
import tkFont
import time
import math


class QuickReaderFrame(Tkinter.Frame):
	"""QuickReader Frame.
	
	This frame consists of a large text area for copying text into (can also be
	populated by command line parameter), a label for flashing the current word
	in a large font, and some basic controlls for starting and stopping and for
	setting the speed.
	"""

	def __init__(self, master=None, text=None):
		"""Create instance of QuickReaderFrame displaying the given text.
		"""
		Tkinter.Frame.__init__(self, master)
		self.master.title('Quick Reader')
		self.bind_all('<Control-q>', quit)
		self.grid()

		# Label showing the current word
		font = tkFont.Font(family="Arial", size="24")
		self.label = Tkinter.Label(self, font=font)
		self.label.grid(row=1, column=1, rowspan=2, sticky="NSEW")

		# Start Button
		self.button_start = Tkinter.Button(self, text='Scan!', command=self.toggle_scan)
		self.button_start.grid(row=1, column=2, sticky="E")
		self.do_scan = False

		# Speed Scale
		self.speed = Tkinter.Scale(self, label='Speed', orient='horizontal', from_=1, to=10)
		self.speed.grid(row=2, column=2, sticky="E")
		self.speed.set(5)

		# Text Field
		self.textfield = ScrolledText.ScrolledText(self, wrap=Tkinter.WORD, bg="white")
		self.textfield.grid(row=3, column=1, columnspan=2)
		if text:
			self.textfield.insert("0.0", text)

	def toggle_scan(self):
		"""Start / Stop scanning words.
		"""
		self.do_scan = not self.do_scan
		self.button_start["text"] = "Stop!" if self.do_scan else "Scan!"
		if self.do_scan:
			self.scan()

	def scan(self):
		"""This iterates the words in the text and one after another flashed 
		them in a large font on the top label and also highlights them in the 
		text. The time a word is flashed depends on its length.
		in the text.
		"""
		# get and split text from Text widget
		try:
			text = self.textfield.get("sel.first", "sel.last")
			first = "sel.first"
		except Tkinter.TclError:
			text = self.textfield.get("0.0", "end")
			first = "0.0"
		words = text.split()

		# prepare tracking of current position
		self.textfield.tag_config("current", background="yellow")
		index = lambda i: "%s + %d chars" % (first, i)
		on, off = 0, 0

		i, s = 0, 0
		# iterate over words
		for word in words:

			# flash current word on label
			self.label["text"] = word
			self.label.update()

			# highlight current word in text
			self.textfield.tag_remove("current", index(on), index(off))
			on  = text.index(word, off)
			off = on + len(word)
			self.textfield.tag_add("current", index(on), index(off))
			self.textfield.update()

			# wait and continue, or abort scanning
			if self.do_scan:
				t = get_display_time(word) / self.speed.get()
				i, s = i + 1, s + t
				time.sleep(t)
			else:
				break

		# remove tracking mark
		self.textfield.tag_delete("current")
		print "Read %d words in %f seconds (~%d WpM)" % (i, s, i*60/s)

	
def get_display_time(word):
	"""Calculate and return the display time allocated to the given word. The
	display time is based on a default time of 1.0 and factors derived from the
	word's length and its context, e.g. if it stands at the end of the sentence.
	"""
	# take word's length into account
	t = math.log(len(word), 10)
	# wait longer, if word ends with punctuation
	if word[-1] == ".":	
		t *= 1.5
	if word[-1] == ",":	
		t *= 1.25
	print "%10f %s" % (t, word)
	return t


# start application
if __name__ == '__main__':
	def main():
		"""Parse command line options and start application.
		"""
		import optparse

		# parse and check command line options
		parser = optparse.OptionParser("quickreader.py [File]")
		(_, args) = parser.parse_args()

		# read filename from command line and read file content
		text = None
		if len(args) >= 1:
			fname = args[0]
			with open(fname, 'r') as f:
				text = f.read()

		# start application
		QuickReaderFrame(text=text).mainloop()
	main()
