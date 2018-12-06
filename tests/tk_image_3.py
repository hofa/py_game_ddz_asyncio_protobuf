import tkinter
from PIL import Image, ImageTk
tk = tkinter.Tk()


# im = Image.open("/Users/tyleryang/mycode/python/tw1/client/images/277581-qZVAKd.jpg")
# img = tkinter.PhotoImage(im)

file_path = "/Users/tyleryang/mycode/python/tw1/client/images/ph.png"
im = Image.open(file_path)

im2 = im.crop((0, 0, 70, 96))




class Ph:
    def __init__(self):
        self.file_path = "/Users/tyleryang/mycode/python/tw1/client/images/ph.png"
        self.x_side = 7
        self.y_side = 13
        self.card_width = 65
        self.card_height = 92
        self.im = Image.open(self.file_path)
        self.max_colums = 14
        self.max_rows = 4
        self.x_j = 3.3
        self.y_j = 3.5

    def get(self, row=0, column=0):
        # return self.im.crop((
        #     self.x_side + row * (self.card_width + self.x_j),
        #     self.y_side + column * (self.card_width + self.y_j),
        #     self.card_width,
        #     self.card_height
        # ))

        return self.im.crop((
            self.x_side + row * (self.card_width + self.x_j),
            self.y_side + column * (self.card_height + self.y_j),
            self.x_side + self.card_width + row * (self.card_width + self.x_j),
            self.y_side + self.card_height + column * (self.card_height + self.y_j)
        ))

    def getb(self):
        x_side = 7
        y_side = 13
        card_width = 65
        card_height = 92
        max_colums = 14
        max_rows = 4
        x_j = 3.3
        y_j = 3.5
        row=13
        column=2
        im = self.im.crop((
            x_side + row * (card_width + x_j),
            y_side + column * (card_height + y_j),
            x_side + card_width + row * (card_width + x_j),
            y_side + card_height + column * (card_height + y_j)
        ))
        # im = im.resize((92, 65))
        im = im.rotate(90)
        im = im.resize((card_height, card_width))
        return im

    def fetch_all(self):
        pass

# w = tkinter.Canvas(tk, width=1024, height=800)
# w.create_rectangle(0, 0, 1024, 800, fill="#211f20")
# w.pack()

ph = Ph()
tk.configure(background='#211f20')
img = ImageTk.PhotoImage(ph.get(0, 0))
l = tkinter.Label(tk, image=img)
l.pack()
l.configure(background='#211f20')

img2 = ImageTk.PhotoImage(ph.get(1, 0))
l2 = tkinter.Label(tk, image=img2)
l2.pack()
l2.configure(background='#211f20')

img3 = ImageTk.PhotoImage(ph.get(2, 0))
l3 = tkinter.Label(tk, image=img3)
l3.pack()
l3.configure(background='#211f20')

img4 = ImageTk.PhotoImage(ph.get(3, 0))
l4 = tkinter.Label(tk, image=img4)
l4.pack()
l4.configure(background='#211f20')

img5 = ImageTk.PhotoImage(ph.get(0, 1))
l5 = tkinter.Label(tk, image=img5)
l5.pack()
l5.configure(background='#211f20')

# img5 = ImageTk.PhotoImage(ph.get(2, 2))
# l5 = tkinter.Label(tk, image=img5)
# l5.pack()


# img5 = ImageTk.PhotoImage(ph.get(10, 3))
# l5 = tkinter.Label(tk, image=img5)
# l5.pack()

img5 = ImageTk.PhotoImage(ph.getb())
l5 = tkinter.Label(tk, image=img5)
l5.pack()


l = tkinter.Label(tk, text="sb")
l.pack()
tk.minsize(1024, 800)
tk.mainloop()
