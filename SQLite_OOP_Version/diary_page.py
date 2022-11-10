from tkinter import *
import create_diary
import json
import calendar
import os
import sqlite3

class Diary:

    BACKGROUND_COLOR = "#787296"
    TEXT_COLOR = '#fcefe3'

    def __init__(self, root, canvas, year, month, day, Id, cursor, db):

        wd = os.getcwd()

        for child in canvas.winfo_children():
            child.destroy()
        
        root.config(bg=self.BACKGROUND_COLOR)
        canvas.config(width=480, height=200, bg = self.BACKGROUND_COLOR)

        self.go_back_btn = Button(canvas, text="<", command=lambda: self.main_page(root, canvas, Id, db, cursor, year, month))
        self.go_back_btn.config(font = ("Courier", 15, "bold"), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0)
        self.go_back_btn.grid(row=0, column=0)

        self.label_date = Label(canvas, text=f'{calendar.month_name[month]} {day}, {year}♥')
        self.label_date.config(font = ("Courier", 15, "bold"), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR)
        self.label_date.grid(row=0, column=1, sticky='w')

        self.txt = Text(canvas, bg=self.BACKGROUND_COLOR, width= 40, height=20, borderwidth=2, relief='ridge')
        self.txt.grid(row=1, column=0, rowspan=2, columnspan=2)

        self.date = f"{year}-{month}-{day}"

        try:
            cursor.execute("SELECT content FROM diary WHERE user_id = ? AND date = ?", (Id, self.date))
            content = cursor.fetchone()[0]
            db.commit()
        except:
            pass 
        else:
            self.txt.insert(END, content)

        save_btn = Button(canvas, text="Save", command=lambda: self.save_diary(root, canvas, Id, db, cursor, self.date, year, month))
        save_btn.config(font = ("Courier", 15, "bold"), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0)
        save_btn.grid(row=4, column=1, sticky='e')

    def main_page(self, root, canvas, Id, db, cursor, year, month):
        main_page = create_diary.MainPage(root, canvas, Id, db, cursor, year, month)

    def save_diary(self, root, canvas, Id, db, cursor, date, year, month):
        wd = os.getcwd()
        entry = self.txt.get("1.0", END)

        main_page = create_diary.MainPage(root, canvas, Id, db, cursor, year, month)
        cursor.execute("INSERT INTO diary VALUES(?, ?, ?)", (Id, self.date, entry,))
        db.commit()
