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
top = Frame(t, width=master_width, height=50, bg='black')
left = Frame(t, width=200, height=master_height  - 50 - 200, bg='blue')
center = Frame(t, width=master_width  - 2 * 200, height=master_height - 50 - 200, bg='gray')
right = Frame(t, width=200, height=master_height  - 50 - 200, bg='red')
bottom = Frame(t, width=master_width, height=200, bg='red')



#---------------------- 底部 -----------------------
ll1 = Frame(bottom, width=200, height=200, bg='green')
l = Label(ll1, text="image")
l2 = Label(ll1, text="liuweilong")
# l.grid(row=0)
# l2.grid(row=1)
# ll1.grid(row=0, column=0, rowspan=3, columnspan=3)
ll1.grid(row=0, column=0, rowspan=3, columnspan=3, sticky=E + W)

ll2 = Frame(bottom, width=master_width  - 2 * 200, height=200, bg='gray')
# l = Button(ll2, text="A")
# l.grid(column=0)

# l = Button(ll2, text="B")
# l.grid(column=1)
ll2.grid(row=0, column=1, rowspan=3, columnspan=3)

ll3 = Frame(bottom, width=200, height=200, bg='black')
# l1 = Button(ll3, text="出牌")
# l2 = Button(ll3, text="提示")
# l3 = Button(ll3, text="托管")
# l1.grid(row=0)
# l2.grid(row=1)
# l3.grid(row=2)
ll3.grid(row=0, column=2, rowspan=3, columnspan=3)
#----------------------- 底部 ----------------------


top.grid(row=0, column=0, columnspan=3)
left.grid(row=1, column=0)
center.grid(row=1, column=1)
right.grid(row=1, column=2)
bottom.grid(row=2, column=0, columnspan=3)


t.minsize(1024, 800)
t.geometry("1024x800")
t.mainloop()