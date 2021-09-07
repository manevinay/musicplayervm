import threading
from tkinter import *
from pygame import *
from tkinter import filedialog
from tkinter import messagebox
import os
from mutagen.mp3 import MP3
import time

root = Tk()
mixer.init()
root.state('zoomed')
root.minsize(500, 500)
root.iconbitmap(r'sound (1).ico')
frameButton = Frame(root, pady=30)
frameButton.pack()

statusbar = Label(root, text="MUSIC", relief=SUNKEN)
statusbar.pack(side=BOTTOM, fill=X)

bottomframe = Frame(root, pady=30)
bottomframe.pack(side=BOTTOM)

timeframe = Label(root, text=":")
timeframe.pack()

paused = False
mute = False


def details():
    global detail
    detail = os.path.splitext(filename)
    print(details)


def sound():
    global mute
    if mute:
        photo_sound_button.config(image=photo_sound)
        mixer.music.set_volume(0.7)
        scale.set(70)
        mute = False

    else:
        mixer.music.set_volume(0)
        photo_sound_button.config(image=photo_no_sound)
        scale.set(0)
        mute = True


def play_button():
    global paused
    if paused:
        try:
            statusbar['text'] = filename
            mixer.music.unpause()
            play_button.config(image=photo)
            paused = False
        except:
            messagebox.showerror('music not loaded', 'MUSIC NOT FOUND') or messagebox.showerror("Couldn't open",
                                                                                                'MUSIC NOT FOUND')

    else:
        pause_button()
        paused = True


def rewind():
    try:
        statusbar['text'] = "REWIND TIME"
        mixer.music.play()
    except:
        messagebox.showerror('music not loaded', 'TO REWIND FIRST CHOOSE A TRACK ') or messagebox.showerror(
            "Couldn't open", 'TO REWIND FIRST CHOOSE A TRACK')


def pause_button():
    try:
        if filename != True:
            statusbar['text'] = "NO FILES"
    except:
        messagebox.showerror('music not loaded', 'TO Pause FIRST CHOOSE A TRACK ') or messagebox.showerror(
            "Couldn't open", 'TO REWIND FIRST CHOOSE A TRACK')

    else:
        statusbar['text'] = "STOPED FOR NOW"
        mixer.music.pause()
        play_button.config(image=photo1)


def pause_stop():
    mixer.music.stop()


def set_vol(val):
    volume = int(val) / 100
    mixer.music.set_volume(volume)
    if volume != 0:
        photo_sound_button.config(image=photo_sound)
    else:
        photo_sound_button.config(image=photo_no_sound)


def browse_file():
    global filename
    filename = filedialog.askopenfilename()
    try:
        file_extension = os.path.splitext(filename)
        if (file_extension[1] == ".mp3"):
            mixer.music.load(filename)
            mixer.music.play()
            time_filename()
            statusbar['text'] = filename
            t1 = threading.Thread(target=counter, args=(audiolenght,))
            t1.setDaemon(True)
            t1.start()



        else:
            messagebox.showerror(" Couldn't open", 'PLEASE SELECT A MUSIC TRACK MP3 only')
    except:
        messagebox.showerror(" Couldn't open", 'PLEASE SELECT A MUSIC TRACK ')


def time_filename():
    audio = MP3(filename)
    global audiolenght
    audiolenght =int( audio.info.length)
    min, sec = divmod(audiolenght, 60)
    min_a = round(min)
    sec_a = round(sec)
    print(min_a, sec_a)
def counter(t):
    while t and mixer.music.get_busy():
        min, sec = divmod(t,60)
        min_a = round(min)
        sec_a = round(sec)
        timeformat = '{}:{}'.format(min_a, sec_a)
        timeframe['text'] = timeformat
        time.sleep(1.0)
        t -=1

photo = PhotoImage(file=r'python_play() (1).png')
play_button = Button(frameButton, image=photo, command=play_button)
play_button.grid(row=0, column=0, padx=10)

photo1 = PhotoImage(file=r'pythonpause() (1).png')
pause = Button(frameButton, image=photo1, command=pause_button)
pause.grid(row=0, column=1, padx=10)

photo2 = PhotoImage(file=r'stop-button (1).png')
stop = Button(frameButton, image=photo2, command=pause_stop)
stop.grid(row=0, column=2, padx=10)

photo_rewind = PhotoImage(file=r'rewind64.png')
rewind_button = Button(bottomframe, image=photo_rewind, command=rewind)
rewind_button.grid(row=1, column=0, padx=10)

photo_sound = PhotoImage(file=r'sound.png')
photo_no_sound = PhotoImage(file=r'no-sound.png')
photo_sound_button = Button(bottomframe, image=photo_sound, command=sound)
photo_sound_button.grid(row=1, column=1, padx=10)

file = Button(root, command=browse_file)
file.pack()

scale = Scale(bottomframe, from_=0, to_=100, orient=HORIZONTAL, command=set_vol, len=500)
scale.set(50)
scale.grid(row=0, column=1)

root.mainloop()
