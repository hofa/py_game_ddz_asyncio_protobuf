import tkinter
from PIL import Image, ImageTk
tk = tkinter.Tk()


# im = Image.open("/Users/tyleryang/mycode/python/tw1/client/images/277581-qZVAKd.jpg")
# img = tkinter.PhotoImage(im)


img = ImageTk.PhotoImage(file="/Users/tyleryang/mycode/python/tw1/client/images/277581-qZVAKd.jpg")
l = tkinter.Label(tk, image=img)
l.pack()

tk.mainloop()
