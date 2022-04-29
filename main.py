from ast import Global
from asyncio.windows_events import NULL
from csv import reader, writer
import os
from faulthandler import enable
from tkinter import filedialog
import random
from tkinter import *
from idna import check_label

from pyparsing import WordStart


global index

myWords = []
global filename
filename =""
root = Tk()
root.title("Flash cards app")
root.geometry("550x410")
frame = Frame(root)
frame.pack(side="top", expand=True, fill= "both")






def begin_test():
    random.shuffle(myWords)
    global index
    clear_frame()
    def next():
        if(index  == len(myWords)):
            #TODO: Add number of correct and incorrect to the final screen
            #Make each tuple check how many times that word has been answered correctly or incorrectly(possibly show graphs afterwards)
            #make the words be read off of a csv file
            #Make a home landing screen that allows you to add more words, select the csv file you would like to practice with, etc
            answer_label.config(text="Congrats you have finished")
            submit_button.config(state = DISABLED)
            next_button.config(state = DISABLED)    
        answer_label.config(text="")
        entry.delete(0,END)
        submit_button.config(state = ACTIVE)
        next_button.config(state = DISABLED)
        language_words.config(text=myWords[index][0])


    def answer():
        global index
        if(entry.get().upper() == myWords[index][1].upper()):
            answer_label.config(text=f"Correct!")
        else:
            answer_label.config(text=f"Incorrect. Translation:{myWords[index][1]}")
        submit_button.config(state = DISABLED)
        index += 1
        next_button.config(state = ACTIVE)

    language_words = Label(frame, text="", font=("Helvetica",36))
    language_words.pack(pady=50)

    answer_label = Label(frame, text="")
    answer_label.pack(pady=20)
    entry = Entry(frame,font=("Helvetica",18))
    entry.pack(pady=20)


    button_frame = Frame(frame)
    button_frame.pack(pady=20)

    submit_button = Button(button_frame, text="Submit", command=answer)
    submit_button.grid(row=0,column=0,padx=20)

    next_button = Button(button_frame, text="Next Word",state= DISABLED, command=next)
    next_button.grid(row=0,column=1,padx=20)

    leave_button = Button(button_frame, text="Leave Practice", command=home_screen)
    leave_button.grid(row=0,column=2,padx=20)
    index = 0
    next()


def home_screen():
    def browse_files():
        global filename
        print(os.getcwd())
        filename = filedialog.askopenfilename(initialdir = os.getcwd(),title = "Select a File")
        init_words()
        
    def init_words():
        global myWords
        start_button.config(state = DISABLED)
        add_words.config(state=ACTIVE)
        with open(filename, 'r', encoding='utf-8') as read_obj:
            csv_reader = reader(read_obj)
            myWords = list(csv_reader)
            if(len(myWords) > 0):
                start_button.config(state = ACTIVE)
                print(myWords)
    
    def new_words():
        clear_frame()
        
        def add():
            with open(filename, "w",encoding='utf-8', newline='') as write_obj:
                file_writer = writer(write_obj)
                myWords.append([original_entry.get(),translated_entry.get()])
                file_writer.writerows(myWords)
                out_label.config(text=f"Successfully added {original_entry.get()}, {translated_entry.get()}")
                original_entry.delete(0,END)
                translated_entry.delete(0,END)

           
        label1 = Label(frame, text="Original word:", font=("Helvetica",18))
        label1.grid(row = 0, column=0,padx=20)
        original_entry = Entry(frame,font=("Helvetica",18))
        original_entry.grid(row = 0, column= 1)
        label1 = Label(frame, text="Translated word:", font=("Helvetica",18))
        label1.grid(row = 1, column=0,padx=20)
        translated_entry = Entry(frame,font=("Helvetica",18))
        translated_entry.grid(row = 1, column= 1)
        out_label = Label(frame, text="", font=("Helvetica",18))
        out_label.grid(row=2,pady=20,padx=20)
        button_frame = Frame(frame)
        button_frame.grid(row = 3, pady=20)
        leave_button = Button(button_frame, text="return to Home Screen", command=home_screen)
        leave_button.grid(row=0,column=0,padx=20)
        add_button = Button(button_frame, text="Add word", command=add)
        add_button.grid(row=0,column=1,padx=20)


        
        


            
    clear_frame()
    title_label = Label(frame, text="Flash Cards App", font=("Helvetica",36))
    title_label.pack(pady=20)
    button_frame = Frame(frame)
    button_frame.pack(pady=20)

    start_button = Button(button_frame, text="Start Practice", command=begin_test, state = DISABLED)
    start_button.grid(row=0,column=0,padx=20)

    file_button = Button(button_frame, text="Select file", command=browse_files)
    file_button.grid(row=0,column=1,padx=20)

    add_words = Button(button_frame, text="Add words", command=new_words, state = DISABLED)
    add_words.grid(row =0, column= 2, padx=20)
    global filename
    if(filename != ""):
        init_words()
        print(myWords)





def clear_frame():
    for widgets in frame.winfo_children():
      widgets.destroy()

home_screen()
root.mainloop()