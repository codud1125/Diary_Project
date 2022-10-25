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

activitydic = {}

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

    activityentry(newWindow)
    return

def activityentry(newWindow):
    # Upper half configuration
    listbox = Listbox(newWindow, width = 63, height=10)

    listbox.place(x=250, y=10)

    def loadbtncommand():
        txt.delete("1.0", END)
        activityname.delete(0, END)

        combobox_starthour.set(str(activitydic[f'{month}/{date}'][listbox.curselection()[0]][0]) + "시")
        combobox_startmin.set(str(activitydic[f'{month}/{date}'][listbox.curselection()[0]][1]) + "분")
        combobox_durationhour.set(str(activitydic[f'{month}/{date}'][listbox.curselection()[0]][6]) + "시간")
        combobox_durationmin.set(str(activitydic[f'{month}/{date}'][listbox.curselection()[0]][7]) + "분동안")
        
        activityname.insert(0, activitydic[f'{month}/{date}'][listbox.curselection()[0]][4])
        txt.insert(END, activitydic[f'{month}/{date}'][listbox.curselection()[0]][5])

    def deletebtncommand():
        for index in reversed(listbox.curselection()):
            listbox.delete(index)
        print(activitydic)
        activitydic[f'{month}/{date}'].pop(index)

    btn_load = Button(newWindow, text="불러오기", command=loadbtncommand)
    btn_load.place(x=370, y=180)

    btn_delete = Button(newWindow, text="삭제하기", command=deletebtncommand)
    btn_delete.place(x=470, y=180)

    # Bottom half configuration
    hour_value = [str(i) + "시" for i in range(6,25)]
    minute_value = [str(i) + "분" for i in range(0,61)] 
    duration_minute_Value = [str(i) + "시간" for i in range(0,25)]
    duration_hour_value = [str(i) + "분동안" for i in range(0,61)]

    combobox_starthour = ttk.Combobox(newWindow, height=5, values=hour_value, width=4)
    combobox_startmin = ttk.Combobox(newWindow, height=5, values=minute_value, width=4)
    combobox_starthour.place(x=250, y=215)
    combobox_starthour.set("시")
    combobox_startmin.place(x=300, y=215)
    combobox_startmin.set("분")

    combobox_durationhour = ttk.Combobox(newWindow, height=5, values=duration_minute_Value, width=5)
    combobox_durationmin = ttk.Combobox(newWindow, height=5, values=duration_hour_value, width=7)
    combobox_durationhour.place(x=400, y=215)
    combobox_durationhour.set("시간")
    combobox_durationmin.place(x=460, y=215)
    combobox_durationmin.set("분동안")

    activityname = Entry(newWindow, width=47)
    activityname.place(x=250, y=240)
    activityname.insert(0, "시간을 선택하고 할 활동을 한 줄로 입력하세요")

    txt = Text(newWindow, width=47, height=10)
    txt.place(x=250, y=260)
    txt.insert(END, "활동에 관한 어떤 정보던 입력하세요")

    def infoadd(activitydic):
        print(activitydic)
        actlen = len(activitydic[f'{month}/{date}'])-1
        listbox.insert(END, str(activitydic[f'{month}/{date}'][actlen][0]) + '시 ' +
         str(activitydic[f'{month}/{date}'][actlen][1]) + '분 시작 ' +
         str(activitydic[f'{month}/{date}'][actlen][2]) + '시 ' +
         str(activitydic[f'{month}/{date}'][actlen][3]) + '분 종료: ' +
         activitydic[f'{month}/{date}'][actlen][4])

    def dailybtncommand():
        starthour = combobox_starthour.get()
        startmin = combobox_startmin.get()        
        durationhour = combobox_durationhour.get()
        durationminute = combobox_durationmin.get()

        aname = activityname.get()
        atxt = txt.get("1.0", END)
        print(aname)
        print(atxt)
        if starthour == '시' or startmin == '분' or durationhour == '시간' or durationminute == '분동안':
            messagebox.showwarning("경고", "모든 시간 항목을 선택하세요.")
            return

        starthour = int(starthour[:starthour.find('시')])
        startmin = int(startmin[:startmin.find('분')])
        durationhour = int(durationhour[:durationhour.find('시간')])
        durationminute = int(durationminute[:durationminute.find('분동안')])

        endhour = starthour + durationhour
        endminute = startmin + durationminute

        if endminute >= 60:
            endminute -=60
            endhour += 1
    
        if f'{month}/{date}' not in activitydic:
            activitydic[f'{month}/{date}'] = []
            activitydic[f'{month}/{date}'].append([starthour, startmin, endhour, endminute, aname, atxt, durationhour, durationminute])
        else:
            activitydic[f'{month}/{date}'].append([starthour, startmin, endhour, endminute, aname, atxt, durationhour, durationminute])
        
        infoadd(activitydic)

    btn_daily = Button(newWindow, text="저장하기", command=dailybtncommand)
    btn_daily.place(x=420, y=450)

    


root.resizable(False, False)
root.mainloop()

