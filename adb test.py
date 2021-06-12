import subprocess
import threading
from tkinter import *
from tkinter.ttk import *
import sys
import os
from datetime import datetime
import io
from doctest import master

# create root window
root = Tk()
root.geometry('400x350')
root.title("Phone and Devices toolkit")
bg = PhotoImage(file="dark_BG.png")
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# desktop_path
desktop_path = desktop_path.replace('\\', "\\\\")

# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

label2 = Label(root, text="Phone and devices toolkit", foreground="black")
label3 = Label(root, text="Android Tools:", foreground="black").place(x=5, y=40, width=100)

frame = Frame(root)

# geometry method
frame.pack()

devList = []

devices_check_list = []


def CheckboxCreate(devList):
    for item in devices_check_list:
        item.destroy()
    for index, devsList in enumerate(devList):
        c = Checkbutton(root, text=devsList)
        c.place(x=5, y=160 + (index * 20), width=150)
        devices_check_list.append(c)


def helloCallBack():
    dev_list = subprocess.check_output("adb devices", shell=True).decode(sys.stdout.encoding)
    lines = io.StringIO(dev_list)
    lines.readline()
    devList = []

    for line in lines:
        if line and line.strip() != '':
            split_up = line.split()
            devList.append(split_up[0])

    CheckboxCreate(devList)


label2.place(x=150, y=10)
devices_list = Button(root, text="List Devices", command=helloCallBack).place(x=5, y=70, width=100)

pid_list = []


def logProcess():
    pid_list = []
    for device in devices_check_list:
        if device.instate(['selected']):
            deviceid = device.cget('text')
            subprocess.check_output("adb -s " + deviceid + " logcat -c", shell=True).decode(sys.stdout.encoding)
            logcat = ['adb', '-s', deviceid, 'logcat', '-v', 'threadtime']
            logfile = open(
                desktop_path + '\\' + deviceid + " " + str(datetime.now().strftime("%Y-%m-%d_%H-%M")) + '.txt', 'w')

            proc = subprocess.Popen(logcat, stdout=logfile, stderr=subprocess.STDOUT)
            # print("pass" + deviceid, proc.pid)

            pid_list.append(proc)


def stop_logs():
    subprocess.check_output("adb kill-server", shell=True).decode(sys.stdout.encoding)


start_logs = Button(text="Capture Logs", command=logProcess).place(x=5, y=100, width=100)

stop_logs = Button(root, text="Stop Logs", command=stop_logs).place(x=5, y=130, width=100)

# Tkinter event loop
root.mainloop()
