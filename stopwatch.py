import study_calc
from tkinter import *
from tkinter.ttk import *
from time import sleep, strftime
import os
import sys

sys.path.append("/home/bibhav/Documents/Startup")


def stop():
    global running
    running = False


def pause():
    global Pause, root2, label2
    if Pause == False:
        Pause = True
        root2 = Tk()
       # root2.iconbitmap("Alarm_Clock.ico")
        root2.title("Time Wasted")
        label2 = Label(root2, font=("ds-digital bold", 100),
                       background="black", foreground="cyan")
        label2.pack(anchor='center')
        status2 = Button(root2, text="Pause", command=pause)
        status2.pack(padx=10)
    else:
        Pause = False
        root2.destroy()
        # print(f'{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}')


# msg
window = Tk()
# window.iconbitmap("Alarm_Clock.ico")
window.title("Alarm Clock")
window.resizable(0, 0)
msg = Label(window, font=("Algerian", 70), background="dark orange",
            foreground="dark blue", text='Exit this window\n        to start')
msg.pack(anchor='center')
window.mainloop()


# main window
root = Tk()
# root.iconbitmap("Alarm_Clock.ico")
root.title("Stop Watch")

label = Label(root, font=("ds-digital bold", 100),
              background="black", foreground="cyan")
label.pack(anchor='center')
stop = Button(root, text="Stop", command=stop)
stop.pack(padx=10)
status = Button(root, text="Pause", command=pause)
status.pack(padx=10)


time_sec = 0
time_sec2 = 0
running = True
Pause = False
root2 = ""
label2 = ""
start = strftime("%I:%M:%S %p")

while running:
    if Pause:
        sleep(1)
        time_sec2 += 1
        h, m = divmod(time_sec2, 3600)
        m, s = divmod(m, 60)
        label2.config(
            text=f'{str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}')
        status.config(text="Play")
        root2.update()
        root.update()
        continue
    status.config(text="Pause")
    sleep(1)
    time_sec += 1
    H, M = divmod(time_sec, 3600)
    M, S = divmod(M, 60)
    label.config(text=f'{str(H).zfill(2)}:{str(M).zfill(2)}:{str(S).zfill(2)}')
    root.update()
print(f'Time taken: {str(H).zfill(2)}:{str(M).zfill(2)}:{str(S).zfill(2)}')
if not ('h' in globals() or 's' in globals() or 'm' in globals()):
    h = m = s = 0
print(f'Time wasted: {str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}')

root.destroy()

with open("Study_Time.txt", "a" if os.path.isfile("Study_Time.txt") else "w") as f:
    print(strftime(f"%d %B, %Y ({start} - %I:%M:%S %p):-"), file=f)
    print(
        f'Study Time: {str(H).zfill(2)}:{str(M).zfill(2)}:{str(S).zfill(2)}', file=f)
    print(
        f'Other Time: {str(h).zfill(2)}:{str(m).zfill(2)}:{str(s).zfill(2)}'+"\n", file=f)

study_calc.func()
