import socket
import tkinter as tk
from tkinter import font
import pickle
import webbrowser

Response = []
# Class to create vertical scrollable frame to show urls to the user.
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
        # canvas.place(x=2,y=200)
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


# Destroy the current result frame and create a new frame.
def frame_clear():
    scframe.destroy()
    create()

# Create a scrollable frame to show to the user.
def create():
    global scframe
    scframe = VerticalScrolledFrame(root)
    scframe.pack(side='bottom', pady=30)

def openlink(x):
    webbrowser.open_new(x)

def getquery():
    frame_clear()
    e = user_query.get()
    ClientSocket.send(str.encode(e))
    Response = ClientSocket.recv(2048)
    Response = pickle.loads(Response)
    for i, x in enumerate(Response):

        btn = tk.Button(scframe.interior, height=1, width=100, relief=tk.FLAT, bg="gray99", fg="blue", font="Dosis",
                        text=f"{Response[i]}", command=lambda i=i, x=x: openlink(x))
        btn.pack(padx=10, pady=5, side=tk.TOP)
    Response.clear()
    if e == 'end':
        ClientSocket.close()


print('** Ready to connect **')
while True:
    host = input('Enter server IP:\t')
    port = 95

    ClientSocket = socket.socket()

    try:
        ClientSocket.connect((host, port))
        print('\t** Connected to server **')
        break
    except socket.error as e:
        print("Incorrect IP or server is not running")

root = tk.Tk()
root.title("Search Engine")
root.geometry('800x500')
root['bg'] = '#FFFFFF'
root.minsize(800, 500)
root.maxsize(800, 500)
# lis = []
user_query = tk.StringVar()
# logo_path = tk.PhotoImage(file="BG.ppm")
# logo = Label(root, image=logo_path).pack()
button_font = font.Font(family='Calibri', size=8)
text_entry = tk.Entry(root, textvariable=user_query, width=55, bg='#C0C0C0').place(x=230, y=120)
search_button = tk.Button(root, text="Search", font=button_font, padx=1, pady=1, command=getquery).place(x=375, y=150)
scframe = VerticalScrolledFrame(root)
scframe.pack(side='bottom', pady=30)

root.mainloop()
