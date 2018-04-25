#!/usr/bin/env python3
# -*- coding: utf8 -*-

"""User interface for simple Password Manager.
by Tobias Küster, 2018

- automatically decrypts on loading and encrypts on saving
- shows passwords in a list and with details
- provides edit fields for all attributes
- provides basic search/filter feature
- actions for copy to clipboard, open URL, and similar
"""

import tkinter, tkinter.messagebox, tkinter.filedialog
import pwdmgr_core, pwdmgr_model, config
import os


class PwdMgrFrame(tkinter.Frame):
	
	def __init__(self, root, conf, filename):
		super().__init__(root)
		self.conf = conf
		self.filename = filename
		self.grid()

		self.fltr = tkinter.StringVar()
		self.fltr.trace("w", self.filter_list)
		
		tkinter.Entry(self, textvariable=self.fltr).grid(row=0, column=0, sticky="EW")
		tkinter.Button(self, text="<<", command=self.clear_fltr).grid(row=0, column=1, sticky="EW")	
		tkinter.Button(self, text="+", command=self.add_password).grid(row=0, column=2, sticky="EW")
		tkinter.Button(self, text="-", command=self.remove_password).grid(row=0, column=3, sticky="EW")
		tkinter.Button(self, text="w!", command=self.save).grid(row=0, column=4, sticky="EW")

		self.table = PwdTable(self)
		self.table.grid(row=1, column=0, columnspan=5)
		self.table.show_passwords(self.conf.passwords)
		# TODO wrap table in scrollpane

	def clear_fltr(self):
		print("clearing fitler")
		self.fltr.set("")

	def filter_list(self, *args):
		print("filtering...")
		s = self.fltr.get()
		filtered = [p for p in self.conf.passwords if any(s in v for v in p if v)]
		self.table.show_passwords(filtered)
		return filtered
		
	def save(self):
		if tkinter.messagebox.askokcancel("Save", "Save changes?"):
			print("saving...")
			pwdmgr_core.save_encrypt(self.filename, self.conf)

	def add_password(self):
		print("adding password")
		p = pwdmgr_model.Password("", "", "", "", "", "")
		self.conf.passwords.append(p)
		self.filter_list()
		
	def remove_password(self):
		if tkinter.messagebox.askokcancel("Remove", "Remove all shown entries?"):
			print("removing password")
			for entry in self.filter_list():
				self.conf.passwords.remove(entry)
			self.clear_fltr()


class PwdTable(tkinter.Canvas):
	
	def __init__(self, parent):
		super().__init__(parent)
		self.grid()
		
	def show_passwords(self, passwords):
		# remove old children from grid
		for child in self.grid_slaves():
			child.grid_forget()
		# add row with the attribute names
		for col, attribute in enumerate(pwdmgr_model.Password._fields):
			tkinter.Label(self, text=attribute).grid(row=0, column=col, sticky="NW")
		# add rows with filtered passwords
		for row, pwd in enumerate(passwords, start=1):
			for col, value in enumerate(pwd):
				var = tkinter.StringVar()
				var.set(value)
				tkinter.Entry(self, textvariable=var).grid(row=row, column=col, sticky="W")
				var.trace("w", lambda *args, v=var, a=attribute, p=pwd: setattr(p, a, v.get()))


if __name__ == "__main__":
	filename = config.DEFAULT_PASSWORDS_FILE
	try:
		conf = pwdmgr_core.load_decrypt(filename)
	except IOError:
		conf = pwdmgr_model.create_test_config()

	root = tkinter.Tk()
	frame = PwdMgrFrame(root, conf, filename)
	root.title("Password Manager")
	root.mainloop()
