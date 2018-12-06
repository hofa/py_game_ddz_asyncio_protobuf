from tkinter import *

class Application(Frame):
    def say_hi(self):
        print("hi there, everyone!")

    def createWidgets(self):
        self.QUIT = Button(self)
        self.QUIT["text"] = "QUIT"
        self.QUIT["fg"]   = "red"
        self.QUIT["command"] =  self.quit

        self.QUIT.pack({"side": "left"})

        self.hi_there = Button(self)
        self.hi_there["text"] = "Hello",
        self.hi_there["command"] = self.say_hi

        self.hi_there.pack({"side": "left"})

    def loginCallback(self, event):
        print("登录")

    def registerCallback(self, event):
        print("注册")

    def gotoRegisterCallback(self, event):
        print("跳转注册")
        self.current_frame.destroy()
        self.current_frame = self.registerWidgets()

    def gotoLoginCallback(self, event):
        print("跳转登录")
        self.current_frame.destroy()
        self.current_frame = self.loginWidgets()

    def loginWidgets(self):
        frame = Frame(self)
        title = Label(self, text = '登录系统')
        title.pack()

        username = Entry(self, background = 'white')
        username.pack()
        username.focus_set()

        password = Entry(self, background = 'white')
        password.pack()

        login = Button(self, text = '登录')
        login.bind("<Button-1>", self.loginCallback)
        login.pack(side = LEFT)

        register = Button(self, text = '没有账号?')
        register.bind("<Button-1>", self.gotoRegisterCallback)
        register.pack(side = RIGHT)

        frame.pack()
        return frame

    def registerWidgets(self):
        frame = Frame(self)
        title = Label(self, text = '注册账号')
        title.pack()

        username = Entry(self, background = 'white')
        username.pack()
        username.focus_set()

        password = Entry(self, background = 'white')
        password.pack()

        register = Button(self, text = '注册')
        register.bind("<Button-1>", self.registerCallback)
        register.pack(side = LEFT)

        returnLogin = Button(self, text = '返回登录')
        returnLogin.bind("<Button-1>", self.gotoLoginCallback)
        returnLogin.pack(side = RIGHT)
        
        frame.pack()
        return frame

    def __init__(self, master=None):
        Frame.__init__(self, master)
        self.current_frame = self.loginWidgets()
        self.pack()
        # self.createWidgets()

root = Tk()
app = Application(master=root)
app.master.title("hi")
app.master.minsize(500, 300)
app.master.maxsize(600, 400)
app.mainloop()
root.destroy()