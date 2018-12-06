import tkinter as tk

class Popout(tk.Frame):
    def __init__(self, parent):
        tk.Frame.__init__(self, parent, background="black", padx=10, pady=10)
        title = tk.Label(self, text="How to play", font=("Helvetica", 16), anchor="w",
                         background="black", foreground="white")
        instructions = tk.Label(self, text="The goal of Klondike is to blah blah blah...",
                                background="black", foreground="white", anchor="w")
        cb = tk.Checkbutton(self, text="Do not show again", highlightthickness=0,
                            background="black", foreground="white")
        oneof = tk.Label(self, text="1 of 6", background="black", foreground="white")
        close_btn = tk.Button(self, text="Close", background="black", foreground="white")
        next_btn = tk.Button(self, text="Next", background="black", foreground="white")

        self.grid_columnconfigure(0, weight=1)
        self.grid_rowconfigure(1, weight=1)

        title.grid(row=0, column=0, columnspan=2, sticky="ew")
        oneof.grid(row=0, column=2, sticky="ne")
        instructions.grid(row=1, column=0, columnspan=3, sticky="nsew", pady=10)
        cb.grid(row=2, column=0, sticky="w")
        close_btn.grid(row=3, column=1, sticky="ew", padx=10)
        next_btn.grid(row=3, column=2, sticky="ew")

root = tk.Tk()
root.geometry("600x400")

p = Popout(root)
p.place(relx=.5, rely=.5, anchor="center")

root.mainloop()