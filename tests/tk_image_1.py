''' tk_image_view_url_io.py
display an image from a URL using Tkinter, PIL and data_stream
tested with Python27 and Python33  by  vegaseat  01mar2013
'''
import io
# allows for image formats other than gif
from PIL import Image, ImageTk
try:
    # Python2
    import Tkinter as tk
    from urllib2 import urlopen
except ImportError:
    # Python3
    import tkinter as tk
    from urllib.request import urlopen
root = tk.Tk()
# find yourself a picture on an internet web page you like
# (right click on the picture, under properties copy the address)
#url = "http://www.google.com/intl/en/images/logo.gif"
# or use image previously downloaded to tinypic.com
#url = "http://i48.tinypic.com/w6sjn6.jpg"
url = "http://i50.tinypic.com/34g8vo5.jpg"
image_bytes = urlopen(url).read()
# internal data file
data_stream = io.BytesIO(image_bytes)
# open as a PIL image object
pil_image = Image.open(data_stream)
# optionally show image info
# get the size of the image
w, h = pil_image.size
# split off image file name
fname = url.split('/')[-1]
sf = "{} ({}x{})".format(fname, w, h)
root.title(sf)
# convert PIL image object to Tkinter PhotoImage object
tk_image = ImageTk.PhotoImage(pil_image)
# put the image on a typical widget
label = tk.Label(root, image=tk_image, bg='brown')
label.pack(padx=5, pady=5)
root.mainloop()