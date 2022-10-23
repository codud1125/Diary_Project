import tkinter
import os
import tkinter.ttk as ttk
import tkinter.messagebox as messagebox
from tkinter import *
from PIL import Image, ImageTk


# Step 1: Import Calendar Image
root = Tk()
root.title("한국 일정 여행 프로그램 - 날짜를 선택하세요")
root.geometry("640x480") # 가로 * 세로

calendar_image = Image.open('C:/Users/codud/OneDrive/Desktop/CL/Python/Py_Korea_Project/Calendar.jpg')
calendar_image = calendar_image.resize((640,480), Image.ANTIALIAS)
calendar = ImageTk.PhotoImage(calendar_image)

label1 = tkinter.Label(image=calendar)
label1.image = calendar
label1.place(x=0, y=0)

# Step 2: Import a button that selects a date that opens up a new window

def btncmd():
    global month
    global date 
    
    month = combobox_month.get()
    date = combobox_date.get()
    month = int(month[0])
    date = int(date[:date.find('일')])

    if (month == 4 and date > 8) or (month == 3 and date < 23):
        messagebox.showwarning("경고", "3월 24일과 4월 8일 이내의 날짜를 선택하세요.")
    else:
        newWindow_daily()

btn_date = Button(root, text="확인", command=btncmd)
btn_date.place(x=475, y=380)

month_value = [str(i) + "월" for i in [3,4]]
date_value = [str(i) + "일" for i in range(1,31)] # 1부터 31까지의 숫자를 반환 
combobox_month = ttk.Combobox(root, height=5, values=month_value, state="readonly",width=3)
combobox_date = ttk.Combobox(root, height=5, values=date_value, state="readonly",width=4)
combobox_month.place(x=450, y=350)
combobox_month.set("월")
combobox_date.place(x=500, y=350)
combobox_date.set("일")

# Step 3. 새로운 창 열기
def newWindow_daily():
    newWindow = Toplevel(root)
    newWindow.title(f'일정 - {month}월 {date}일')
    newWindow.geometry("640x480")

    newWindow.resizable(False, False)

    daily_image = Image.open('C:/Users/codud/OneDrive/Desktop/CL/Python/Py_Korea_Project/Daily.jpg')
    daily = ImageTk.PhotoImage(daily_image)

    label_daily = tkinter.Label(newWindow, image=daily)
    label_daily.image = daily
    label_daily.place(x=0, y=0)


root.resizable(False, False)
root.mainloop()

