from tkinter import *
import time
from PIL import Image, ImageTk
t = Tk()
t.title('与python聊天中')
       
  #创建frame容器
# frmLT = Frame(width=500, height=320, bg='white')
# frmLC = Frame(width=500, height=150, bg='red')
# frmLB = Frame(width=500, height=30)
# frmRT = Frame(width=200, height=500)

# frmLT.grid(row=0, column=0,padx=1,pady=3)
# frmLC.grid(row=1, column=0,padx=1,pady=3)
# frmLB.grid(row=2, column=0)
# frmRT.grid(row=0, column=1, rowspan=3,padx=2,pady=3)

'''
sticky=N/S/E//W:顶端对齐/底端对齐/右对齐/左对齐

　　sticky=N+S：拉伸高度，使其在水平方向上顶端和底端都对齐

　　sticky=E+W，拉伸宽度，使其在垂直方向上左边界和右边界都对齐

　　sticky=N+S+E:拉伸高度，使其在水平方向上对齐，并将控件放在右边（当两个控件放在同一行同一列时效果明显）
'''

master_width = 1024
master_height = 800

a = Frame(t, width=1024, height=800)
a.pack()

top = Frame(a, width=master_width, height=50, bg='black')
left = Frame(a, width=200, height=master_height  - 50 - 200, bg='white')
center = Frame(a, width=master_width  - 2 * 200, height=master_height - 50 - 200, bg='gray')
right = Frame(a, width=200, height=master_height  - 50 - 200, bg='white')
bottom = Frame(a, width=master_width, height=200, bg='white')

#---------------------- 底部 -----------------------
# ll1 = Frame(bottom, width=200, height=200, bg='green')
# l = Label(ll1, text="image")
# l2 = Label(ll1, text="liuweilong")
# l.grid(row=0)
# l2.grid(row=1)
# ll1.grid(row=0, column=0, rowspan=3, columnspan=3)
# ll1.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=E + W)

# ll2 = Frame(bottom, width=master_width  - 2 * 200, height=200, bg='gray')
# l = Button(ll2, text="A")
# l.grid(column=0)

# l = Button(ll2, text="B")
# l.grid(column=1)
# ll2.grid(row=0, column=1, rowspan=3, columnspan=3)

# ll3 = Frame(bottom, width=200, height=200, bg='black')
# l1 = Button(ll3, text="出牌")
# l2 = Button(ll3, text="提示")
# l3 = Button(ll3, text="托管")
# l1.grid(row=0)
# l2.grid(row=1)
# l3.grid(row=2)
# ll3.grid(row=0, column=2, rowspan=3, columnspan=3)
#----------------------- 底部 ----------------------


# top.pack(side=TOP)
# left.pack(side=LEFT, expand=YES)
# center.pack(side=LEFT, expand=YES)
# right.pack(side=RIGHT, expand=YES)x
# bottom.pack(side=BOTTOM)
top.place(x=0, y=0)
left.place(x=0, y=50)
center.place(x=200, y=50)
right.place(x=824, y=50)
bottom.place(x=0, y=600)
t.minsize(1024, 800)
t.geometry("1024x800")



# left
username = Label(left, text = "xxxx")
username.place(x=10, y=0)
button = Button(left, text = "", width=10)
button.place(x=20, y=20)
button = Button(left, text = "", width=10)
button.place(x=20, y=50)

# right
username = Label(right, text = "xxxx2")
username.place(x=10, y=0)
button = Button(right, text = "", width=10)
button.place(x=20, y=20)
button = Button(right, text = "", width=10)
button.place(x=20, y=50)


# bottom
username = Label(bottom, text = "xxxx3")
username.place(x=10, y=0)
button = Button(bottom, text = "A", width=6)
button.place(x=20, y=60)
button = Button(bottom, text = "B", width=6)
button.place(x=80, y=60)
button = Button(bottom, text = "C", width=6)
button.place(x=220, y=60)
button = Button(bottom, text = "D", width=6)
button.place(x=320, y=60)

button = Button(bottom, text = "出牌", width=6)
button.place(x=930, y=20)

button = Button(bottom, text = "提示", width=6)
button.place(x=930, y=60)

button = Button(bottom, text = "托管", width=6)
button.place(x=930, y=100)

# center
button = Label(center, text = "A", width=4, bg="gray")
button.place(x=0, y=0)
button = Label(center, text = "B", width=4, bg="gray")
button.place(x=30, y=0)
t.mainloop()