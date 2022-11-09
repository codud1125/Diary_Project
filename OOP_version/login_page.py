from tkinter import *
from tkinter import messagebox
from create_diary import *
import json
import os

class Login:

    BACKGROUND_COLOR = "#787296"
    TEXT_COLOR = '#fcefe3'

    def __init__(self, root, canvas):

        for child in canvas.winfo_children():
            child.destroy()

        root.config(padx=50, pady=50, background=self.BACKGROUND_COLOR)
        canvas.config(width = 300, height = 200, bg=self.BACKGROUND_COLOR, highlightthickness=0)

        #Labels:
        self.welcome_label = canvas.create_text(20, 0, text="Welcome to your diary!", font = ("Courier", 15, "bold"), fill = self.TEXT_COLOR, anchor='nw')
        self.ID_label = canvas.create_text(20, 80, text="ID: ", font = ("Courier", 15, "italic"), fill = self.TEXT_COLOR, anchor='nw')
        self.password_label = canvas.create_text(20, 110, text="Password: ", font = ("Courier", 15, "italic"), fill = self.TEXT_COLOR, anchor='nw')

        #Textbox:
        self.ID_textbox = Entry(canvas, width=20, bg = self.TEXT_COLOR)
        self.ID_textbox.place(x=150, y=80)
        self.ID_textbox.focus()
        self.password_textbox = Entry(canvas, width=20, show="*", bg = self.TEXT_COLOR)
        self.password_textbox.place(x=150, y=110)

        #Buttons:
        self.button_login = Button(canvas, text="Login", command=lambda:self.login(root, canvas))
        self.button_login.config(font = ("Courier", 15, "italic"), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0)
        self.button_login.place(x=40, y=170)
        self.button_signup = Button(canvas, text="Signup", command=lambda: self.signup(root, canvas))
        self.button_signup.config(font = ("Courier", 15, "italic"), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0)
        self.button_signup.place(x=180, y=170)

    def login(self, root, canvas):
        self.Id = self.ID_textbox.get()
        self.password = self.password_textbox.get()
        wd = os.getcwd()
        
        if self.Id == '' or self.password == '':
            messagebox.showwarning("Warning", "Please enter all fields")
        else:
            try:
                with open(wd + "/Py_Korea_Project/user_data.json", "r") as file:
                    data = json.load(file) 
                    user_password = data[self.Id]['password']
            except FileNotFoundError:
                messagebox.showerror("Error", "There is no user associated with the login.")
                return(False)
            except KeyError:
                messagebox.showerror("Error", "There is no user associated with the login.")
                return(False)
            else:
                if user_password != self.password:
                    messagebox.showerror("Error", "Double check your password.")
                    self.ID_textbox.delete(0, END)
                    self.password_textbox.delete(0, END)
                    return(False)
                else:
                    main_page = MainPage(root, canvas, self.Id)
                    canvas.itemconfig(self.welcome_label, text="")

    def signup(self, root, canvas):
        self.ID_textbox.delete(0, END)
        self.password_textbox.delete(0, END)

        canvas.itemconfig(self.welcome_label, text='Signup Page')

        self.button_login.config(text = "Login Page", font = ("Courier", 15), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0, command = lambda:self.login_ui(root, canvas))
        self.button_login.place(x=20, y=170)
        self.button_signup.config(text = "Signup", font = ("Courier", 15), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0, command = lambda:self.add_user_data(root, canvas))
        self.button_signup.place(x=180, y=170)
        
    def login_ui(self, root, canvas):
        self.ID_textbox.delete(0, END)
        self.password_textbox.delete(0, END)

        canvas.itemconfig(self.welcome_label, text='Welcome to your diary!')

        self.button_login.config(text = "Login", font = ("Courier", 15), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0, command = lambda:self.login(root, canvas))
        self.button_login.place(x=40, y=170)
        self.button_signup.config(text = "Signup", font = ("Courier", 15), fg = self.TEXT_COLOR, bg = self.BACKGROUND_COLOR, borderwidth = 0, command = lambda:self.signup(root, canvas))
        self.button_signup.place(x=180, y=170)
        
        return()


    def add_user_data(self, root, canvas):
        self.Id = self.ID_textbox.get()
        self.password = self.password_textbox.get()
        wd = os.getcwd()

        if self.Id == '' or self.password == '':
            messagebox.showwarning("Warning", "Please enter all fields")
            return()
        
        new_data = {
            self.Id: {
                "password": self.password
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
            if self.Id in data.keys():
                messagebox.showwarning("Warning", "Username is already taken. Please choose another username")
                self.ID_textbox.delete(0, END)
                self.password_textbox.delete(0, END)
                return()
            else:
                data.update(new_data)
                messagebox.showinfo("Info", "Signup was successful")

                with open(wd +"/Py_Korea_Project/user_data.json", "w") as file:
                    json.dump(data, file, indent=4)

        finally:
            self.ID_textbox.delete(0, END)
            self.password_textbox.delete(0, END)
            self.login_ui(root, canvas)
        return()

