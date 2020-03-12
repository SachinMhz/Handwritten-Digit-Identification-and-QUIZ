from tkinter import *
from tkinter.ttk import *
from tkinter import messagebox
from PIL import Image, ImageDraw, ImageTk
import glob
from os import path
import os
from functools import partial

from identify_and_segment import image_identification, image_segmentation
from numerical import LEVELS
from quiz import QUIZ


class PaintCanvas:
    def __init__(self,WINDOW):
        self.WINDOW = WINDOW
        self.old_x = None
        self.old_y = None
        self.penWidth = 10
        self.canvas_width = 400
        self.canvas_height = 150
        self.penColor = 'black'
        self.fg_color = (0,0,0) #for draw 
        self.bg_color = (255,255,255) #for draw
        self.createWidgets()

    def paint(self,e):
        if self.old_x and self.old_y:
            self.c.create_line(self.old_x,self.old_y,e.x,e.y,
                width=self.penWidth,fill=self.penColor,
                capstyle=ROUND,smooth=True
            )
            self.draw.line([self.old_x,self.old_y,e.x,e.y],self.fg_color, width=10)

        self.old_x = e.x
        self.old_y = e.y

    def reset(self,e):    #reseting or cleaning the canvas 
        self.old_x = None
        self.old_y = None 
    
    def createWidgets(self):
        white = (255,255,255)

        x,y = 100, 333
        
        ShowButton(self.WINDOW,"Pen",x,y,self.selectPen)
        ShowButton(self.WINDOW,"Eraser",x+100,y,self.selectEraser)
        ShowButton(self.WINDOW,"Clear",x+200,y,self.selectClear)
        ShowButton(self.WINDOW,"Save",x+300,y,self.saveImage)

        self.c = Canvas(self.WINDOW,width=self.canvas_width,height=self.canvas_height,bg='white')
        self.c.pack()
        self.c.place(x=100,y=365)

        self.c.bind('<B1-Motion>',self.paint)#drwaing the line 
        self.c.bind('<ButtonRelease-1>',self.reset)

        self.image1 = Image.new("RGB", (500, 150), self.bg_color)
        self.draw = ImageDraw.Draw(self.image1)
    
    def selectClear(self):
        self.c.delete("all")
        self.draw.line([0,0,500,500],self.bg_color, width=500)
    
    def selectPen(self):
        self.penWidth = 13
        self.penColor = "black"
        self.fg_color = (0,0,0)
    
    def selectEraser(self):
        self.penWidth = 30
        self.penColor = "white"
        self.fg_color = (255,255,255)
    
    def saveImage(self):
        global QUESTION, ANSWER, level
        Images_path = os.getcwd() + '\\Images\\'
        filename = Images_path+"answer.jpg"

        self.image1.save(filename)
        image_segmentation()
        answer, accuracy = image_identification()
        confirm = messagebox.askquestion('Confirm','Is your number '+str(answer) +' ? (with '+str("{0:.2f}".format(accuracy*100)+'% accuracy).'))
        self.selectClear()
        if confirm == 'no':
            return
        print("predicted number as :",answer)
        
        if int(answer) == int(ANSWER):
            level +=1
            if GAME_TYPE == "NUMERICAL":
                QUESTION  =  LEVELS[level]
                canvas.itemconfigure(label2, text=QUESTION+' =')
                ANSWER = eval(QUESTION.replace('x','*'))
                
            else:
                QUESTION, ANSWER= QUIZ[level]
                canvas.itemconfigure(label2, text=QUESTION)
        else:
            messagebox.showinfo('Wrong','Sorry, your answer is incorrect.\n Try again.')

def ShowButton(WINDOW,text,X,Y,Command):
    panel = Button(WINDOW, text=text,style='TButton',command=Command)
    panel.pack()
    panel.place(x=X,y=Y)

Images_path = os.getcwd() + '\\Images\\'
bg_img = Images_path + "background.jpg"
bg2_img = Images_path + "bg.jpg"

WINDOW = Tk()
WINDOW.geometry('+200+50') #show WINDOW starting from x-200 and y-50
WINDOW.geometry('600x600') #set the geomentry of WINDOW
WINDOW.title("Machine learning")
style = Style()  
style.configure('W.TButton', font =('calibri', 15, 'bold', 'underline'), 
                foreground = 'green', borderwidth = '4') 
style.configure('TButton', font =('calibri', 13, 'bold', 'underline'), 
                foreground = 'green', borderwidth = '4') 

def menu():
    global canvas1
    canvas1 = Canvas(WINDOW, width=600, height=600)
    canvas1.pack()

    img = Image.open((bg2_img))
    img = img.resize((600, 600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    bg_label = canvas1.create_image((0,0), image=img, anchor=N+W)
    canvas1.image = img 
    label1 = canvas1.create_text((300,150), text="     HandWritten Digit    \n Identification and QUIZ", font="MSGothic 30 bold", fill="green")

    Math_btn = Button(WINDOW,text='Math',style='W.TButton',command=partial(main,'NUMERICAL'))
    Math_button = canvas1.create_window(300,300,window=Math_btn)

    Quiz_btn = Button(WINDOW,text='Quiz',style='W.TButton',command=partial(main,'QUIZ'))
    Quiz_button = canvas1.create_window(300,350,window=Quiz_btn)

    Exit_btn = Button(WINDOW,text='Exit',style='W.TButton',command=quit)
    Exit_button = canvas1.create_window(300,400,window=Exit_btn)

def main(type):
    global canvas, QUESTION , ANSWER , GAME_TYPE , label2, level
    canvas1.delete('all')
    img = Image.open((bg_img))
    img = img.resize((600, 600), Image.ANTIALIAS)
    img = ImageTk.PhotoImage(img)
    canvas = Canvas(WINDOW, height=600, width=600)
    canvas.pack()
    canvas.place(x=0,y=0)

    bg_label = canvas.create_image((0,0), image=img, anchor=N+W)
    canvas.image = img 
    label1 = canvas.create_text((300,100), text="Write Your Answer", font="MSGothic 40 bold", fill="#652828")
    GAME_TYPE = type
    level = 0
    if GAME_TYPE == "NUMERICAL":
        QUESTION  =  LEVELS[level]
        ANSWER = eval(QUESTION)
        label2 = canvas.create_text((300,225), text= QUESTION+' =', font="MSGothic 75 bold", fill="#652828")
    else:
        QUESTION, ANSWER= QUIZ[level]
        label2 = canvas.create_text((300,225), text= QUESTION, font="MSGothic 18 bold", fill="#652828")

    PaintCanvas(WINDOW)

menu()
WINDOW.mainloop()