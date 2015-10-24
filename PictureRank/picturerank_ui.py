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
DELIMITER = " - "

class PictureRankUI(tkinter.Frame):
	
	def __init__(self, master, ranker):
		tkinter.Frame.__init__(self, master)
		self.master.title("Picture Rank")
		self.grid()
		self.ranker = ranker
		self.current = None
		self.images = {}

		self.label1 = tkinter.Label(self, width=WIDTH, height=HEIGHT)
		self.label1.grid(row=0, column=0)
		self.label2 = tkinter.Label(self, width=WIDTH, height=HEIGHT)
		self.label2.grid(row=0, column=1)
		
		self.bind_all("<KeyRelease>", self.handle_keys)

		self.ranking = tkinter.Listbox(self, height='25', selectmode='single')
		self.ranking.bind('<ButtonRelease>', self.from_ranking)
		self.ranking.grid(row=0, column=2)
		
		self.set_random_images()
		self.update_ranking()
	
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
		self.update_ranking()
		self.set_random_images()
		
	def update_ranking(self):
		ranking = self.ranker.get_best()
		self.ranking.delete(0, len(ranking))
		self.ranking.insert(0, *("%s%s%s" % (rank, DELIMITER, pic) for pic, rank in ranking))
		
	def from_ranking(self, event):
		p1, p2 = self.current
		selection = self.ranking.get(self.ranking.nearest(event.y))
		pic = selection.split(DELIMITER, 1)[1]
		if event.num == 1:
			self.set_images(pic, p2)
		if event.num == 3:
			self.set_images(p1, pic)
			
	def set_random_images(self):
		p1, p2 = self.ranker.get_random_pair()
		self.set_images(p1, p2)
		
	def set_images(self, p1, p2):
		self.label1.configure(image=self.load_image(p1))
		self.label2.configure(image=self.load_image(p2))
		self.current = p1, p2
		
	def load_image(self, pic):
		if pic not in self.images:
			path = self.ranker.path(pic)
			img = self.auto_rotate(Image.open(path))
			img.thumbnail((WIDTH, HEIGHT))
			self.images[pic] = ImageTk.PhotoImage(img)
		return self.images[pic]
		
	def auto_rotate(self, img):
		# http://www.lifl.fr/~damien.riquet/auto-rotating-pictures-using-pil.html
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
	
	directory = "/home/tkuester/TEST"
	# directory = filedialog.askdirectory()
	ranker = picturerank.PictureRank(directory)

	PictureRankUI(root, ranker)
	root.mainloop()
	
if __name__ == "__main__":
	main()
	