from sqlite3 import Date
from tkinter import *
from tkinter import ttk
from tkinter import messagebox
import tkcalendar
from tkcalendar import Calendar
from PIL import Image, ImageTk
import random
import pandas
import json
import datetime
import os
import calendar


# ---------------------------- Button Command setup ------------------------------- #


def main_page():

    root.config(bg=TEXT_COLOR)

    canvas.config(width=480, height=200, bg = TEXT_COLOR)
    canvas.itemconfig(welcome_label, text='')
    canvas.itemconfig(ID_label, text='')
    canvas.itemconfig(password_label, text='')

    for child in canvas.winfo_children():
        child.destroy()

    c = calendar.TextCalendar(calendar.SUNDAY)
    str = c.formatmonth(2023, 3)

    def redraw(year, month):
        
        def openlist():
            wd = os.getcwd()

            listwindow = Toplevel(root)
            listwindow.title('Diary by Chun')
            listwindow.config(width=130, height=150, bg=TEXT_COLOR)
            listwindow.resizable(False, False)

            label_list = Label(listwindow, text=f"{Id}'s diary list")
            label_list.config(font = ("Courier", 10, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, anchor='w')
            label_list.grid(row=0,column=0)

            listbox = Listbox(listwindow)
            listbox.config(font = ("Courier"), bg = TEXT_COLOR, fg = BACKGROUND_COLOR)
            listbox.grid(row=1, column=0)

            with open(wd + "/Py_Korea_Project/user_data.json", "r") as file:
                data = json.load(file) 
                entry = data[Id]
                len_journal = len(data[Id])
                if len_journal > 1:
                    for i in range(1, len_journal):
                        listbox.insert(END, list(entry.keys())[i])

            button_list = Button(listwindow, text="Select")
            button_list.config(font = ("Courier", 10, "italic"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, borderwidth = 0)
            button_list.grid(row=3, column=0)

        global Id

        '''Redraws the calendar for the given year and month'''
        label_user = Label(canvas, text=f"{Id}'s diary")
        label_user.config(font = ("Courier", 15, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, anchor='w')
        label_user.grid(row=1,column=0)

        label_placeholder = Label(canvas, text=f" ")
        label_placeholder.config(font = ("Courier", 30), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, anchor='w')
        label_placeholder.grid(row=0,column=1)

        left_arrow = Button(canvas, text="<", command=lambda: redraw(year, month-1))
        left_arrow.config(font = ("Courier", 15, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, borderwidth = 0)
        left_arrow.grid(row=0, column=2, sticky="nsew")

        right_arrow = Button(canvas, text=">", command=lambda: redraw(year, month+1))
        right_arrow.config(font = ("Courier", 15, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, borderwidth = 0)
        right_arrow.grid(row=0, column=3, sticky="nsew")

        if year == 2023 and (month == 3 or month==4):
            label_month_year = Label(canvas, text=f"{month}/{year}")
            label_month_year.config(font = ("Courier", 30, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR)
            label_month_year.grid(row=0,column=0)

                # day of the week headings
            for col, day in enumerate(("Mo", "Tu", "We", "Th", "Fr", "Sa", "Su")):
                label = Label(canvas, text=day)
                label.config(font = ("Courier", 15, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR)
                label.grid(row=1, column=col+2, sticky="nsew")

                # buttons for each day
            cal = calendar.monthcalendar(year, month)
            for row, week in enumerate(cal):
                for col, day in enumerate(week):
                    text = "" if day == 0 else day
                    state = "normal" if day > 0 else "disabled"
                    cell = Button(canvas, text=text, state=state, command=lambda day=day: set_day(month, day))
                    cell.config(font = ("Courier", 15, "bold"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, borderwidth = 0)
                    if col == 6:
                        cell.config(fg='#e6394d')
                    cell.grid(row=row+2, column=col+2, sticky="nsew")
                    
        elif month>4:
            month = 4
        elif month<3:
            month = 3


        button_list = Button(canvas, text="View your list", command=openlist)
        button_list.config(font = ("Courier", 10, "bold", "italic"), fg = BACKGROUND_COLOR, bg = TEXT_COLOR, borderwidth = 0)
        button_list.grid(row=6, column=0, columnspan=1, sticky='W')

        canvas.pack()


    def set_day(month, day):
        wd = os.getcwd()

        for child in canvas.winfo_children():
            child.destroy()
        
        root.config(bg=BACKGROUND_COLOR)
        canvas.config(width=480, height=200, bg = BACKGROUND_COLOR)

        go_back_btn = Button(canvas, text="<", command=main_page)
        go_back_btn.config(font = ("Courier", 15, "bold"), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0)
        go_back_btn.grid(row=0, column=0)

        label_date = Label(canvas, text=f'{calendar.month_name[month]} {day}, 2023♥')
        label_date.config(font = ("Courier", 15, "bold"), fg = TEXT_COLOR, bg = BACKGROUND_COLOR)
        label_date.grid(row=0, column=1, sticky='w')

        txt = Text(canvas, bg=BACKGROUND_COLOR, width= 40, height=20, borderwidth=2, relief='ridge')
        txt.grid(row=1, column=0, rowspan=2, columnspan=2)

        date = f"2023-{month}-{day}"

        try:
            with open(wd + "/Py_Korea_Project/user_data.json", "r") as file:
                data = json.load(file) 
                content = data[Id][date]
        except KeyError:
            pass
        else:
            txt.insert(END, content)

        save_btn = Button(canvas, text="Save", command=lambda: save_diary(date))
        save_btn.config(font = ("Courier", 15, "bold"), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0)
        save_btn.grid(row=4, column=1, sticky='e')

        def save_diary(date):
            global Id
            global password 

            wd = os.getcwd()
            entry = txt.get("1.0", END)

            main_page()

            with open(wd + "/Py_Korea_Project/user_data.json", "r") as jsonFile:
                data = json.load(jsonFile)

            data[Id][date] = entry

            with open(wd + "/Py_Korea_Project/user_data.json", "w") as jsonFile:
                json.dump(data, jsonFile)            
            
            return

    redraw(2023, 3)
    return

def login():
    global Id
    global password
    Id = ID_textbox.get()
    password = password_textbox.get()
    wd = os.getcwd()
    
    if Id == '' or password == '':
        messagebox.showwarning("Warning", "Please enter all fields")
    else:
        try:
            with open(wd + "/Py_Korea_Project/user_data.json", "r") as file:
                data = json.load(file) 
                user_password = data[Id]['password']
        except FileNotFoundError:
            messagebox.showerror("Error", "There is no user associated with the login.")
            return
        except KeyError:
            messagebox.showerror("Error", "There is no user associated with the login.")
            return
        else:
            if user_password != password:
                messagebox.showerror("Error", "Double check your password.")
                ID_textbox.delete(0, END)
                password_textbox.delete(0, END)
                return
            else:
                main_page()
    return()

def signup():
    def login_ui():
        ID_textbox.delete(0, END)
        password_textbox.delete(0, END)

        canvas.itemconfig(welcome_label, text='Welcome to your diary!')

        button_login.config(text = "Login", font = ("Courier", 15), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0, command = login)
        button_login.place(x=40, y=170)
        button_signup.config(text = "Signup", font = ("Courier", 15), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0, command = signup)
        button_signup.place(x=180, y=170)
        
        return()

    def add_user_data():
        global Id
        global password

        Id = ID_textbox.get()
        password = password_textbox.get()
        wd = os.getcwd()

        if Id == '' or password == '':
            messagebox.showwarning("Warning", "Please enter all fields")
            return()
        
        new_data = {
            Id: {
                "password": password
            }
        }
        
        try:
            with open(wd + "/Py_Korea_Project/user_data.json", "r") as file:
                data = json.load(file)
        except FileNotFoundError:
            with open(wd +"/Py_Korea_Project/user_data.json", "w") as file:
                json.dump(new_data, file, indent=4)
            messagebox.showinfo("Info", "Signup was successful")
        else:
            if Id in data.keys():
                messagebox.showwarning("Warning", "Username is already taken. Please choose another username")
                ID_textbox.delete(0, END)
                password_textbox.delete(0, END)
                return()
            else:
                data.update(new_data)
                messagebox.showinfo("Info", "Signup was successful")

                with open(wd +"/Py_Korea_Project/user_data.json", "w") as file:
                    json.dump(data, file, indent=4)

        finally:
            ID_textbox.delete(0, END)
            password_textbox.delete(0, END)
            login_ui()

        return()

    ID_textbox.delete(0, END)
    password_textbox.delete(0, END)

    canvas.itemconfig(welcome_label, text='Signup Page')

    button_login.config(text = "Login Page", font = ("Courier", 15), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0, command = login_ui)
    button_login.place(x=20, y=170)
    button_signup.config(text = "Signup", font = ("Courier", 15), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0, command = add_user_data)
    button_signup.place(x=180, y=170)

    return()
# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#787296"
TEXT_COLOR = '#fcefe3'

root = Tk()
root.title("Diary by Chun")
root.config(padx=50, pady=50, background=BACKGROUND_COLOR)

canvas = Canvas(width = 300, height = 200)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.pack()

#Labels:

welcome_label = canvas.create_text(20, 0, text="Welcome to your diary!", font = ("Courier", 15, "bold"), fill = TEXT_COLOR, anchor='nw')
ID_label = canvas.create_text(20, 80, text="ID: ", font = ("Courier", 15, "italic"), fill = TEXT_COLOR, anchor='nw')
password_label = canvas.create_text(20, 110, text="Password: ", font = ("Courier", 15, "italic"), fill = TEXT_COLOR, anchor='nw')

#Textbox:
ID_textbox = Entry(canvas, width=20, bg = TEXT_COLOR)
ID_textbox.place(x=150, y=80)
ID_textbox.focus()
password_textbox = Entry(canvas, width=20, show="*", bg = TEXT_COLOR)
password_textbox.place(x=150, y=110)

#Buttons:
button_login = Button(canvas, text="Login", command=login)
button_login.config(font = ("Courier", 15, "italic"), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0)
button_login.place(x=40, y=170)
button_signup = Button(canvas, text="Signup", command=signup)
button_signup.config(font = ("Courier", 15, "italic"), fg = TEXT_COLOR, bg = BACKGROUND_COLOR, borderwidth = 0)
button_signup.place(x=180, y=170)


root.mainloop()

 