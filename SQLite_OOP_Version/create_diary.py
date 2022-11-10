from tkinter import *
import login_page
import diary_page
from tkinter import messagebox
import calendar
import datetime
import sqlite3

class MainPage:
    BACKGROUND_COLOR = "#787296"
    TEXT_COLOR = '#fcefe3'

    today = datetime.datetime.now()
    year = int(today.strftime('%Y'))
    month = int(today.strftime('%m').lstrip("0"))

    def __init__(self, root, canvas, Id, db, cursor, year=year, month=month):
        root.config(bg=self.TEXT_COLOR)
        canvas.config(width=480, height=200, bg = self.TEXT_COLOR)

        for child in canvas.winfo_children():
            child.destroy()

        self.draw_calendar(root, canvas, year, month, Id, db, cursor)

    def draw_calendar(self, root, canvas, year, month, Id, db, cursor, direction='start'):
        for child in canvas.winfo_children():
            child.destroy()

        if direction == 'left':
            month -= 1
            if month ==0:
                month =12
                year -= 1

        if direction == 'right':
            month += 1
            if month == 13:
                month = 1
                year += 1

        '''Redraws the calendar for the given year and month'''
        self.label_user = Label(canvas, text=f"{Id}'s diary")
        self.label_user.config(font = ("Courier", 15, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, anchor='w')
        self.label_user.grid(row=1,column=0)

        self.label_placeholder = Label(canvas, text=f" ")
        self.label_placeholder.config(font = ("Courier", 30), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, anchor='w')
        self.label_placeholder.grid(row=0,column=1)

        self.left_arrow = Button(canvas, text="<", command=lambda: self.draw_calendar(root, canvas, year, month, Id, db, cursor, 'left'))
        self.left_arrow.config(font = ("Courier", 15, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, borderwidth = 0)
        self.left_arrow.grid(row=0, column=2, sticky="nsew")

        self.right_arrow = Button(canvas, text=">", command=lambda: self.draw_calendar(root, canvas, year, month, Id, db, cursor, 'right'))
        self.right_arrow.config(font = ("Courier", 15, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, borderwidth = 0)
        self.right_arrow.grid(row=0, column=3, sticky="nsew")

        self.label_month_year = Label(canvas, text=f"{month}/{year}")
        self.label_month_year.config(font = ("Courier", 30, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR)
        self.label_month_year.grid(row=0,column=0)

        # day of the week headings
        for col, day in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
            self.label = Label(canvas, text=day)
            self.label.config(font = ("Courier", 15, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR)
            self.label.grid(row=1, column=col+2, sticky="nsew")

        # buttons for each day
        cal = calendar.monthcalendar(year, month)
        for row, week in enumerate(cal):
            for col, day in enumerate(week):
                text = "" if day == 0 else day
                state = "normal" if day > 0 else "disabled"
                cell = Button(canvas, text=text, state=state, command=lambda day=day: self.diary_page(root, canvas, year, month, day, Id, cursor, db))
                cell.config(font = ("Courier", 15, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, borderwidth = 0)
                if col == 6:
                    cell.config(fg='#e6394d')
                if month == int(datetime.datetime.now().strftime('%m').lstrip("0")) and day == int(datetime.datetime.now().strftime('%d').lstrip("0")):
                    cell.config(fg='#636ee6')
                cell.grid(row=row+2, column=col+2, sticky="nsew")

        self.button_list = Button(canvas, text="View your list", command=lambda: self.openlist(root, canvas, Id, cursor, db))
        self.button_list.config(font = ("Courier", 10, "bold", "italic"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, borderwidth = 0)
        self.button_list.grid(row=5, column=0, columnspan=1, sticky='W')

        self.button_list = Button(canvas, text="Logout", command=lambda: self.logout(root, canvas, db, cursor))
        self.button_list.config(font = ("Courier", 10, "bold", "italic"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, borderwidth = 0)
        self.button_list.grid(row=6, column=0, columnspan=1, sticky='W')

        canvas.pack()

    def openlist(self, root, canvas, Id, cursor, db):
        self.listwindow = Toplevel(root)
        self.listwindow.title('Diary by Chun')
        self.listwindow.config(width=130, height=150, bg=self.TEXT_COLOR)
        self.listwindow.resizable(False, False)

        self.label_list = Label(self.listwindow, text=f"{Id}'s diary list")
        self.label_list.config(font = ("Courier", 10, "bold"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, anchor='w')
        self.label_list.grid(row=0,column=0)

        self.listbox = Listbox(self.listwindow)
        self.listbox.config(font = ("Courier"), bg = self.TEXT_COLOR, fg = self.BACKGROUND_COLOR)
        self.listbox.grid(row=1, column=0)

        cursor.execute("SELECT date FROM diary WHERE user_id = ?", (Id, ))
        dates = cursor.fetchall()

        self.datelist = []

        for date in dates:
            self.listbox.insert(END, date)
            self.datelist.append(date)

        self.button_list = Button(self.listwindow, text="Select", command=lambda: self.openpage(root, canvas, Id, cursor, db))
        self.button_list.config(font = ("Courier", 10, "italic"), fg = self.BACKGROUND_COLOR, bg = self.TEXT_COLOR, borderwidth = 0)
        self.button_list.grid(row=3, column=0)

    def openpage(self, root, canvas, Id, cursor, db):
        self.date = self.datelist[self.listbox.curselection()[0]][0]
        
        self.first_dash = self.date.find('-')
        self.second_dash = self.date.rfind('-')

        self.year = int(self.date[:self.first_dash])
        self.month = int(self.date[self.first_dash+1:self.second_dash])
        self.day = int(self.date[self.second_dash+1:])

        diary_page.Diary(root, canvas, self.year, self.month, self.day, Id, cursor, db)

        self.listwindow.destroy()

    def logout(self, root, canvas, db, cursor):
        LoginPage = login_page.Login(root, canvas, db, cursor)

    def diary_page(self, root, canvas, year, month, day, Id, cursor, db):
        Diary = diary_page.Diary(root, canvas, year, month, day, Id, cursor, db)

