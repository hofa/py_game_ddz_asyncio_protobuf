'''Proof of concept integrating asyncio and tk loops.

Terry Jan Reedy
Run with 'python -i' or from IDLE editor to keep tk window alive.
'''

import asyncio
import datetime as dt
import tkinter as tk

loop = asyncio.get_event_loop()
root = tk.Tk()

# Combine 2 event loop examples from BaseEventLoop doc.
# Add button to prove that gui remain responsive between time updates.
# Prints statements are only for testing.

def flipbg(widget, color):
    bg = widget['bg']
    print('click', bg, loop.time())
    widget['bg'] = color if bg == 'white' else 'white'

hello = tk.Label(root)
flipper = tk.Button(root, text='Change hello background', bg='yellow',
                    command=lambda: flipbg(hello, 'red'))
time = tk.Label(root)
hello.pack()
flipper.pack()
time.pack()

def hello_world(loop):
    hello['text'] = 'Hello World'
loop.call_soon(hello_world, loop)

def display_date(end_time, loop):
    print(dt.datetime.now())
    time['text'] = dt.datetime.now()
    if (loop.time() + 1.0) < end_time:
        loop.call_later(1, display_date, end_time, loop)
    else:
        loop.stop()

end_time = loop.time() + 10.1
loop.call_soon(display_date, end_time, loop)

# Replace root.mainloop with these 4 lines.
def tk_update():
    root.update()
    loop.call_soon(tk_update)  # or loop.call_later(delay, tk_update)
# Initialize loop before each run_forever or run_until_complete call    
tk_update() 
loop.run_forever()