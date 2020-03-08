from tkinter import *
from functools import partial

WINDOW = Tk()
WINDOW.title("HandWritten Digit Identification and Quiz")
WINDOW.geometry('600x600+200+50')

def saveVariable(value):
    with open('Game_Option.txt','w') as file:
        file.write(value)
    import interface as Game
    Game.mainloop()
    WINDOW.destroy()


Math_btn = Button(WINDOW,text='Math Problem',command=partial(saveVariable,'NUMERICAL'))
Math_btn.place(x=250,y=150)
Math_btn.pack()

Quiz_btn = Button(WINDOW,text='Quiz',command=partial(saveVariable,'QUIZ'))
Quiz_btn.place(x=250,y=250)
Quiz_btn.pack()

Exit_btn = Button(WINDOW,text='Exit',command=quit)
Exit_btn.place(x=250,y=350)
Exit_btn.pack()

WINDOW.mainloop()