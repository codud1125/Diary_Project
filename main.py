from sqlite3 import Date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk
import random
import pandas
import json
import datetime
import os

# ---------------------------- Button Command setup ------------------------------- #
def clickdate(date):
    global data
    datelist = str(date).split('-')
    # canvas_left.itemconfig(card_month, text=f'{date.month}')
    canvas_left.itemconfig(card_month, text=f'{datelist[1]}/')
    canvas_left.itemconfig(card_date, text=f'{datelist[2]}')
    canvas_left.itemconfig(card_day, text=f'{data[date]["day"]}')

# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#B1DDC6"

root = Tk()
root.title("Korea Planner")
root.config(padx=50, pady=50, background=BACKGROUND_COLOR)

start_date = datetime.date(2023, 3, 25)
end_date = datetime.date(2023, 4, 8)
delta = datetime.timedelta(days=1)
wd = os.getcwd()

try:
    with open("Korea_plan.json", "r") as file:
        data = json.load(file)
except:
    data = {}
    dayidx = 0 
    day = ['Saturday', 'Sunday', 'Monday', 'Tuesday', 'Wednesday', 'Thursday', 'Friday']
    while (start_date <= end_date):
        data[start_date] = {}
        data[start_date]['day'] = day[dayidx]
        dayidx += 1
        if dayidx > 6:
            dayidx = 0
        start_date += delta
print(data)

# Canvas (Left)
canvas_left = Canvas(width = 315, height = 480)
front_image = PhotoImage(file = wd + '/image/card_front.png')
canvas_image = canvas_left.create_image(155, 240, image = front_image)
canvas_left.config(bg =BACKGROUND_COLOR, highlightthickness=0)
canvas_left.grid(row=0, column=0, rowspan = 10, columnspan=3)

start_date = datetime.date(2023, 3, 25)
row = 5
column = 0

# Labels
card_month = canvas_left.create_text(100, 30, text='Month/', font=('Ariel', '40', 'italic'),fill=BACKGROUND_COLOR)
card_date = canvas_left.create_text(120, 60, text='Date', font=('Ariel', '40', 'italic'),fill=BACKGROUND_COLOR)
card_day = canvas_left.create_text(250, 70, text='Day', font=('Ariel', '15'),fill=BACKGROUND_COLOR)


while (start_date <= end_date):
    img = ImageTk.PhotoImage(file = wd + f'/image/{str(start_date)}.png')
    date_button = Button(root, padx=10, pady=10, image=img, highlightthickness=0, command= lambda date=start_date: clickdate(date))
    date_button.image = img
    date_button.grid(row=row, column=column, rowspan=1, columnspan=1)

    # if row > 2:
    #     date_button.grid(row=row, column=column, rowspan=1, columnspan=1, sticky='N')
    # else:
    #     date_button.grid(row=row, column=column, rowspan=1, columnspan=1)

    start_date += delta
    row += 1
    
    if row == 10:
        row = 5
        column += 1

# Canvas (Right)
canvas_right = Canvas(width = 315, height = 480)
canvas_right.config(bg =BACKGROUND_COLOR, highlightthickness=0)
canvas_right.grid(row=0, column=3, rowspan = 10, columnspan=3)

# # Loading Planner zone (Upper Right)
listbox = Listbox(canvas_right, width = 40, height = 10)
listbox.grid(row=0, column=3, rowspan=2, columnspan=3, padx = 5, pady=5)

# # Writing Planner zone (Lower Right)
txt = Text(canvas_right, width = 30, height = 15)
txt.grid(row=2, column=3, rowspan=2, columnspan=3, padx = 5, pady=5)
txt.insert(END, "활동에 관한 어떤 정보던 입력하세요")

# # # Button zone 
button_load = Button(canvas_right, text="불러오기", width=10, height=2)
button_load.grid(row=4, column=4, sticky='W')
button_save = Button(canvas_right, text="저장하기", width=10, height=2)
button_save.grid(row=4, column=5, sticky='W')

root.mainloop()

 
