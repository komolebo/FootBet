from tkinter import *
from display_info import Display

import tkinter.messagebox

root = Tk()
root.title("Footbet technology")

# Layout parameters
topFrame = Frame(root)
topFrame.pack()
middleFrame = Frame(root)
middleFrame.pack(side=BOTTOM)

labelMain = Label(topFrame, text="Footbet")
labelMain.pack()

# Content setting
for league in Display.leagues:
    labelLeague = Label(middleFrame, text=league)
    labelLeague.pack(side=RIGHT)
# topFrame.

middleFrame.configure(background='pink')


root.mainloop()
