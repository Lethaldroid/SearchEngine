import tkinter as tk
import webbrowser
import tkinter.font as font

root = tk.Tk()
root.title("Search Engine")
root.geometry('800x500')
root['bg'] = '#FFFFFF'
root.minsize(800, 500)
root.maxsize(800, 500)
scrollbar = tk.Scrollbar(root)
scrollbar.pack(side="right", fill="y")
bottomframe = tk.Frame(root)
bottomframe.pack(side="bottom",pady=10,padx=10)
user_query = tk.StringVar()


def getquery():
    e = user_query.get()
    print(e)


def callback(event):
    webbrowser.open_new(event.widget.cget(mylist,"text"))


def makelabel(url):
    lbl = tk.Label(mylist, text=f"{url}", fg="blue", cursor="hand2")
    lbl.pack(padx=10,pady=5)
    lbl.bind("<Button-1>", callback)

button_font = font.Font(family='Arial', size=8)
text_entry = tk.Entry(root, textvariable=user_query, width=55, bg='#C0C0C0').place(x=220, y=100)
search_button = tk.Button(root, text="search", font=button_font, padx=1, pady=1, command=getquery()).place(x=370, y=130)
# box = tk.Text(root, bg="silver", width=90, height=17).place(x=40, y=200)
# for i in range(1, 5):
#     makelabel("https://www.google.com")
#     makelabel("https://www.instagram.com")
mylist = tk.Listbox(bottomframe, height=15, width= 50, yscrollcommand=scrollbar.set)
for i in range(1, 50):
    mylist.insert("end", makelabel("wuhuhu.com"))
mylist.pack(side="left", fill="both")
scrollbar.config(command=mylist.yview)
root.mainloop()
