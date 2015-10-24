try:
	# Python 2
	import Tkinter as tkinter
	import tkFileDialog as filedialog
except:
	# Python 3
	import tkinter
	import tkinter.filedialog as filedialog
import picturerank
from PIL import Image, ImageTk

WIDTH, HEIGHT = 400, 400

class PictureRankUI(tkinter.Frame):
	
	
	def __init__(self, master, ranker):
		tkinter.Frame.__init__(self, master)
		self.master.title("Picture Rank")
		self.grid()
		self.ranker = ranker
		self.current = None
		self.images = {}

		self.label1 = tkinter.Label(self)
		self.label1.grid(row=0, column=0)
		self.label2 = tkinter.Label(self)
		self.label2.grid(row=0, column=1)
		
		self.bind_all("<KeyRelease>", self.handle_keys)
		
		self.load_images()
	
	def handle_keys(self, event):
		if event.keysym == "q":
			del self.ranker
			self.quit()
		if event.keysym == "Left":
			self.select(-1)
		if event.keysym == "Right":
			self.select(+1)
		if event.keysym in ("Up", "Down"):
			self.select(0)

	def select(self, pic):
		if self.current:
			p1, p2 = self.current
			self.ranker.update_rank(p1, p2, pic)
		print(pic)
		print(self.ranker.ranks)
		self.load_images()
		
	def load_images(self):
		p1, p2 = self.ranker.get_random_pair()
		self.label1.configure(image=self.load_image(p1))
		self.label2.configure(image=self.load_image(p2))
		self.current = p1, p2
		
	def load_image(self, pic):
		if pic not in self.images:
			path = self.ranker.path(pic)
			img = Image.open(path)
			img.thumbnail((WIDTH, HEIGHT))
			self.images[pic] = ImageTk.PhotoImage(img)
		return self.images[pic]
	

def main():
	root = tkinter.Tk()
	
	directory = "/home/tkuester/TEST"
	# directory = filedialog.askdirectory()
	ranker = picturerank.PictureRank(directory)

	PictureRankUI(root, ranker)
	root.mainloop()
	
if __name__ == "__main__":
	main()
	