from tkinter import *
from login_page import *

BACKGROUND_COLOR = "#787296"
TEXT_COLOR = '#fcefe3'

root = Tk()
root.title("Diary by Chun")
root.config(padx=50, pady=50, background=BACKGROUND_COLOR)

canvas = Canvas(width = 300, height = 200)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.pack()

LoginPage = Login(root, canvas)

root.mainloop()