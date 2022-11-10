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

db = sqlite3.connect("Chunbae_Diary.db")
cursor = db.cursor()

try:
    cursor.execute("CREATE TABLE users (user_id varchar(250) PRIMARY KEY, password varchar(250))")
    cursor.execute("CREATE TABLE diary (user_id varchar(250), date varchar(250), content varchar(2500), PRIMARY KEY (user_id, date))")
    db.commit()
except:
    pass

LoginPage = Login(root, canvas, db, cursor)

root.mainloop()