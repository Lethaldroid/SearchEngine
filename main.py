import tkinter as tk
import webbrowser
from tkinter import font
from PIL import ImageTk, Image
from tkinter import *

class VerticalScrolledFrame(tk.Frame):
    """A pure Tkinter scrollable frame that actually works!

    * Use the 'interior' attribute to place widgets inside the scrollable frame
    * Construct and pack/place/grid normally
    * This frame only allows vertical scrolling
    """
    def __init__(self, parent, *args, **kw):
        tk.Frame.__init__(self, parent, *args, **kw)

        # create a canvas object and a vertical scrollbar for scrolling it
        vscrollbar = tk.Scrollbar(self, orient=tk.VERTICAL)
        vscrollbar.pack(fill=tk.Y, side=tk.RIGHT, expand=tk.FALSE)
        canvas = tk.Canvas(self, bd=0, highlightthickness=0,
                        yscrollcommand=vscrollbar.set)
        #canvas.place(x=2,y=200)
        canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=tk.TRUE)
        vscrollbar.config(command=canvas.yview)

        # reset the view
        canvas.xview_moveto(0)
        canvas.yview_moveto(0)

        # create a frame inside the canvas which will be scrolled with it
        self.interior = interior = tk.Frame(canvas)
        interior_id = canvas.create_window(0, 0, window=interior,
                                           anchor=tk.NW)

        # track changes to the canvas and frame width and sync them,
        # also updating the scrollbar
        def _configure_interior(event):
            # update the scrollbars to match the size of the inner frame
            size = (interior.winfo_reqwidth(), interior.winfo_reqheight())
            canvas.config(scrollregion="0 0 %s %s" % size)
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the canvas's width to fit the inner frame
                canvas.config(width=interior.winfo_reqwidth())

        interior.bind('<Configure>', _configure_interior)

        def _configure_canvas(event):
            if interior.winfo_reqwidth() != canvas.winfo_width():
                # update the inner frame's width to fill the canvas
                canvas.itemconfigure(interior_id, width=canvas.winfo_width())
        canvas.bind('<Configure>', _configure_canvas)

def clear():
    scframe.destroy()
    create()
    #global scframe=VerticalScrolledFrame(root)
    #scframe.pack(side='bottom', pady=30)
    #for widget in scframe.winfo_children():
    #    widget.destroy()

def getquery():
    clear()
    lis.clear()
    e = user_query.get()
    for k in range (1,10):
        lis.append(str(e))
    for i, x in enumerate(lis):
        btn = tk.Button(scframe.interior, height=1, width=73, relief=tk.FLAT, bg="gray99", fg="blue", font="Dosis", text=f"{lis[i]}", command=lambda i=i, x=x: openlink(i))
        btn.pack(padx=10, pady=5, side=tk.TOP)

def create():
    global scframe
    scframe = VerticalScrolledFrame(root)
    scframe.pack(side='bottom', pady=30)


def openlink(i):
    webbrowser.open_new(lis[i])

root = tk.Tk()
root.title("Search Engine")
root.geometry('800x500')
root['bg'] = '#FFFFFF'
root.minsize(800, 500)
root.maxsize(800, 500)
lis = []
user_query = tk.StringVar()
#load = Image.open("C:\Users\dell\Pictures\BG.JPG")
#logo_path = ImageTk.PhotoImage(load)

#logo = Label(root, image=logo_path).place(x=175, y=10)
button_font = font.Font(family='Arial', size=8)
text_entry = tk.Entry(root, textvariable=user_query, width=55, bg='#C0C0C0').place(x=220, y=100)
search_button = tk.Button(root, text="search", font=button_font, padx=1, pady=1, command=getquery).place(x=370, y=130)
#clear_button = tk.Button(root, text="clear", font=button_font, padx=1, pady=1, command=clear).place(x=400, y=130)
#box = tk.Text(root, bg="silver", width=90, height=17).place(x=39, y=200)

scframe = VerticalScrolledFrame(root)
scframe.pack(side='bottom', pady=30)


# for k in range (1,10):
#     lis=[]
#
# for i, x in enumerate(lis):
#     btn = tk.Button(scframe.interior, height=1, width=73, relief=tk.FLAT,
#         bg="gray99", fg="blue",
#         font="Dosis", text=f"{lis[i]}",
#         command=lambda i=i, x=x: openlink(i))
#     btn.pack(padx=10, pady=5, side=tk.BOTTOM)

root.mainloop()