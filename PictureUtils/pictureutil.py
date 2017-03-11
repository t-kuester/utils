"""Picture Utils
by Tobias Kuester, 2017

Utility class for functions and classes used by both, Picture Rank and
Picture Sort programs.
"""

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
