# from tkinter import *


# def exit_win(event):
#     root.destroy()


# def to_label(event):
#     t = ent.get()
#     lbl.configure(text=t)


# def select_all(event):
#     def select_all2(widget):
#         widget.selection_range(0, END)
#         widget.icursor(END)  # курсор в конец

#     root.after(10, select_all2, event.widget)


# root = Tk()

# ent = Entry(width=40)
# ent.focus_set()
# ent.pack()
# lbl = Label(height=3, fg='orange',
#             bg='darkgreen', font="Verdana 24")
# lbl.pack(fill=X)

# ent.bind('<Return>', to_label)
# ent.bind('<Control-a>', select_all)
# root.bind('<Control-q>', exit_win)

# root.mainloop()






#Import tkinter
from tkinter import*

 # Событие клавиатуры, соответствующая функция ответа
def printInfo(event):
         # Очистить запись2
    entry2.delete(0, END)
         # Вычислить площадь на основе входного радиуса
    R=int(entry1.get())
    S= 3.1415926*R*R
    entry2.insert(10, S)
         # Пустой элемент управления entry2
    entry1.delete(0, END)
 # Распечатать подсказку
def helpInfo():
    entry2.delete(0, END)
    entry2.insert(10, "Одновременно нажмите ctl + c, чтобы вычислить площадь \
                    круга")

 #Initialize Tk ()
myWindow = Tk()
 # Установить заголовок
myWindow.title('Python GUI Learning')
myWindow.geometry('300x70')

 #Label control layout
Label(myWindow, text="input").grid(row=0)
Label(myWindow, text="output").grid(row=1)

 #Entry Control Layout
entry1=Entry(myWindow)
entry2=Entry(myWindow)
entry1.grid(row=0, column=1)
entry2.grid(row=1, column=1)

 # Окно привязки событий клавиатуры
myWindow.bind('<Control-c>', printInfo)

 # Кнопка выхода для выхода; кнопка запуска для печати результатов расчета
Button(myWindow, text='Quit', command=myWindow.quit).grid(row=2, column=0, \
        sticky=W, padx=5,pady=5)
Button(myWindow, text='help', command=helpInfo).grid(row=2, column=1, \
        sticky=W, padx=5, pady=5)

 # Войдите в цикл сообщений
myWindow.mainloop()
