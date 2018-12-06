import tkinter as tk


class ExampleApp(tk.Frame):
    def __init__(self, master):
        tk.Frame.__init__(self, master)
        self.master = master
        self.master.geometry("400x150")
        self.main_frame = tk.Frame(self.master)
        self.main_frame.pack(expand=tk.YES, fill=tk.BOTH)
        self.master.protocol('<WM_LBUTTONDBLCLK>', self.motion)
        tk.Label(self.main_frame, text = "This is the main window").pack()
        tk.Button(self.main_frame, text = "Open 2 top level windows!", command = self.open_windows).pack()

    def motion(self, event):
        x, y = event.x, event.y
        print('{}, {}'.format(x, y))

    def open_windows(self):
        self.top1 = tk.Toplevel(self.master)
        self.top2 = tk.Toplevel(self.master)
        self.top1.geometry("100x100")
        self.top2.geometry("100x100")
        # ties the window close event to our customer close method for toplevel
        self.top1.protocol("WM_DELETE_WINDOW", self.close_toplevels)
        self.top2.protocol("WM_DELETE_WINDOW", self.close_toplevels)
        self.master.bind("<Unmap>", self.icon_all)
        self.top1.bind("<Unmap>", self.icon_all)
        self.top2.bind("<Unmap>", self.icon_all)
        self.master.bind("<Map>", self.de_icon_all)
        self.top1.bind("<Map>", self.de_icon_all)
        self.top2.bind("<Map>", self.de_icon_all)

        for child in self.main_frame.winfo_children():
            child.configure(state='disable')

        tk.Label(self.top1, text ="Topwindow 1").pack()
        tk.Label(self.top2, text ="Topwindow 2").pack()

        # sets the top windows to their initial locations
        self.lock_top_to_root()

        #keeps the top windows in the specified locations compared to root window
        self.master.bind("<Configure>", self.lock_top_to_root)

    def withdraw_tops(self, event=None):
        self.top1.withdraw()
        self.top2.withdraw()

    def de_icon_tops(self, event=None):
        self.top1.deiconify()
        self.top2.deiconify()

    def icon_all(self, event=None):
        self.withdraw_tops()
        self.master.iconify()

    def de_icon_all(self, event=None):
        self.de_icon_tops()
        self.master.deiconify()
        self.lock_top_to_root()

    def lock_top_to_root(self, event=None):
        self.top1.lift() # lift both toplevel windows about root
        self.top2.lift()
        # places each top level at each side
        # this is not set up to compensate for the root being resized but can be if you need it to.
        self.top1.geometry('+{}+{}'.format(self.master.winfo_x()+10, self.master.winfo_y()+30))
        self.top2.geometry('+{}+{}'.format(self.master.winfo_x()+275, self.master.winfo_y()+30))

    def close_toplevels(self):
        # customer close method to reset everything
        self.master.unbind('<Configure>')
        self.master.unbind("<Unmap>")
        self.master.unbind("<Map>")
        self.top1.destroy()
        self.top2.destroy()
        for child in self.main_frame.winfo_children():
            child.configure(state='active')

root = tk.Tk()
my_example = ExampleApp(root)
root.mainloop()