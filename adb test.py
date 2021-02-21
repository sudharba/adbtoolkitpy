import subprocess
import threading
from tkinter import *
from tkinter.ttk import *
import sys
import os
from datetime import datetime
from doctest import master

# create root window
root = Tk()
root.geometry('400x300')
root.title("Phone and Devices toolkit")
bg = PhotoImage(file="dark_BG.png")
desktop_path = os.path.join(os.path.join(os.environ['USERPROFILE']), 'Desktop')
# print(desktop_path)
desktop_path = desktop_path.replace('\\', "\\\\")
# print(desktop_path)
# Show image using label
label1 = Label(root, image=bg)
label1.place(x=0, y=0)

label2 = Label(root, text="Phone and devices toolkit", foreground="black")
label3 = Label(root, text="Android Tools:", foreground="black").place(x=5, y=40, width=100)
device_text = Label(root, text="List of devices", foreground="black")
# frame inside root window
frame = Frame(root)

# geometry method
frame.pack()

dev_list = subprocess.check_output("adb devices", shell=True).decode(sys.stdout.encoding).strip()


def helloCallBack():
    device_text.config(text="")
    device_text.config(text=str(dev_list))
    device_text.config(state='disabled')


label2.place(x=150, y=10)
device_text.place(x=5, y=230, width=390, height=60)

devices_list = Button(root, text="List Devices", command=helloCallBack).place(x=5, y=70, width=100)


def logProcess():
    logfile = open(desktop_path + '\\' + str(datetime.now().strftime("%Y%m%d-%H%M%S")) + '.txt', 'w')
    subprocess.call("adb logcat -c", shell=True)
    proc = subprocess.Popen(['adb', 'logcat', '-v', 'threadtime'], stdout=subprocess.PIPE, stderr=subprocess.STDOUT)
    for line in proc.stdout:
        # sys.stdout.write(str(line))
        logfile.write(str(line.decode('utf-8')))
    proc.wait()

    def stop():
        proc.kill()


start_logs = Button(text="Capture Logs", command=logProcess).place(x=5, y=100, width=100)

stop_logs = Button(root, text="Stop Logs", command=None).place(x=5, y=130, width=100)

# Tkinter event loop
root.mainloop()

# with open('out-file.txt', 'w') as f:
#     subprocess.call(['adb','logcat', '-v', 'threadtime'], stdout=f)
