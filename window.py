from tkinter import *
import tkinter.messagebox as box

testwindow = Tk()
testwindow.title('Yes')
button = Button(testwindow, text='Yes', command=exit)
button.pack(padx=5,pady=2)
testwindow.mainloop()