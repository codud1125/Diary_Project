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
    print("Entering main page...")

    canvas.config(width=300, height=500)
    canvas.itemconfig(welcome_label, text='')
    canvas.itemconfig(ID_label, text='')
    canvas.itemconfig(password_label, text='')

    ID_textbox.place_forget()
    password_textbox.place_forget()
    button_login.place_forget()
    button_signup.place_forget()

    c = calendar.TextCalendar(calendar.SUNDAY)
    str = c.formatmonth(2023, 3)

    calendar_label = canvas.create_text(0, 0, text=str, font = ("Courier", 15, "bold"), fill = 'white', anchor='nw')


    # cal = Calendar(canvas, selectmode='day',
    # year=2023, month=3, day=24)

    # cal.pack(pady=20)

    return

def login():
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

        canvas.itemconfig(welcome_label, text='Welcome to Korea trip planner!')

        button_login.config(text = "Login", font = ("Courier", 15), fg = 'white', bg = BACKGROUND_COLOR, borderwidth = 0, command = login)
        button_login.place(x=160, y=150)
        button_signup.config(text = "Signup", font = ("Courier", 15), fg = 'white', bg = BACKGROUND_COLOR, borderwidth = 0, command = signup)
        button_signup.place(x=240, y=150)
        
        return()

    def add_user_data():
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

    button_login.config(text = "Go back to Login Page", font = ("Courier", 15), fg = 'white', bg = BACKGROUND_COLOR, borderwidth = 0, command = login_ui)
    button_login.place(x=50, y=150)
    button_signup.config(text = "Signup", font = ("Courier", 15), fg = 'white', bg = BACKGROUND_COLOR, borderwidth = 0, command = add_user_data)
    button_signup.place(x=350, y=150)

    return()
# ---------------------------- UI SETUP ------------------------------- #
BACKGROUND_COLOR = "#a474ad"

root = Tk()
root.title("Korea Planner")
root.config(padx=50, pady=50, background=BACKGROUND_COLOR)

canvas = Canvas(width = 480, height = 200)
canvas.config(bg=BACKGROUND_COLOR, highlightthickness=0)
canvas.pack()

#Labels:

welcome_label = canvas.create_text(0, 0, text="Welcome to Korea trip planner!", font = ("Courier", 20, "bold"), fill = 'white', anchor='nw')
ID_label = canvas.create_text(100, 80, text="ID: ", font = ("Courier", 10), fill = 'white', anchor='nw')
password_label = canvas.create_text(100, 110, text="Password: ", font = ("Courier", 10), fill = 'white', anchor='nw')

#Textbox:
ID_textbox = Entry(canvas, width=20)
ID_textbox.place(x=250, y=80)
ID_textbox.focus()
password_textbox = Entry(canvas, width=20, show="*")
password_textbox.place(x=250, y=110)

#Buttons:
button_login = Button(canvas, text="Login", command=login)
button_login.config(font = ("Courier", 15), fg = 'white', bg = BACKGROUND_COLOR, borderwidth = 0)
button_login.place(x=160, y=150)
button_signup = Button(canvas, text="Signup", command=signup)
button_signup.config(font = ("Courier", 15), fg = 'white', bg = BACKGROUND_COLOR, borderwidth = 0)
button_signup.place(x=240, y=150)


root.mainloop()

 
