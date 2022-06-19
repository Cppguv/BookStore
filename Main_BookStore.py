############################################################################################
#   Программа на тему №36 : "Разработка электронного каталога библиотеки."
#   Предмет: Технологии программирования
#   Преподаватель:     Назаров
#
#   Автор : М.Ю. Хмылова, студент 1 курса КубГУ, факультет "Математика и компьютерные науки",
#   май 2022 года
#
############################################################################################


import tkinter as tki
from tkinter import ttk
#from tkinter.constants import *
from tkinter import *
from tkinter.ttk import Treeview, Button
#import db_actions   # импортируем созданные нами функции доступа к нашей базе данных
from db_actions import *


main_wnd = tki.Tk()                 # создаем главное окно программы
main_wnd.title("Book's e-library")  # Заголовок главного окна
main_wnd.geometry("800x600")        # размер главного окна
# main_wnd.resizable(width=False, height=False)
main_wnd.minsize(width="800", height="600") # установим минимальный размер окна 800х600, чтобы не заморачиваться с
                                            # горизонтальной полосой прокрутки при уменьшении

# скрываем созданное главное окно и создаем дочернее окно для аутентификации пользователя
main_wnd.withdraw()
auth_wnd = tki.Toplevel()
auth_wnd.title("Аутентификация")
auth_wnd.geometry("350x165+300+300")
tki.Label(auth_wnd, text="Логин").grid(row=0, column=0)
login_entry = tki.Entry(auth_wnd, width=30)
login_entry.grid(row=0, column=1, padx=10, pady=15)
tki.Label(auth_wnd, text="Пароль").grid(row=1, column=0)
password_entry = tki.Entry(auth_wnd, width=30)
password_entry.grid(row=1, column=1, padx=10, pady=0)

# теперь обработчик для кнопки "Зарегистрироваться"
def reg(login, password):
    reg_wnd = tki.Toplevel()
    auth_wnd.withdraw()
    reg_wnd.title("Регистрация")
    reg_wnd.geometry("350x165+300+300")
    tki.Label(reg_wnd, text="Логин").grid(row=0, column=0)
    reg_login_entry = tki.Entry(reg_wnd, width=30)
    reg_login_entry.grid(row=0, column=1, padx=10, pady=15)
    reg_login_entry.insert(0, login)
    tki.Label(reg_wnd, text="Пароль").grid(row=1, column=0)
    reg_password_entry = tki.Entry(reg_wnd, width=30)
    reg_password_entry.grid(row=1, column=1, padx=10, pady=0)
    reg_password_entry.insert(0, password)
    tki.Label(reg_wnd, text="E-mail").grid(row=2, column=0)
    reg_email_entry = tki.Entry(reg_wnd, width=30)
    reg_email_entry.grid(row=2, column=1, padx=10, pady=15)
    reg_btn_cancel = tki.Button(reg_wnd, text="Отмена", command=quit).grid(row=3, column=1, ipadx=30, padx=10, pady=10,
                                                                        sticky='e')
    reg_btn_reg = tki.Button(reg_wnd, text="Регистрация", command=lambda: (insert_user(reg_login_entry.get(), \
                  reg_password_entry.get(), reg_email_entry.get(), 2) or reg_wnd.destroy() or auth_wnd.destroy() or \
                  main_wnd.iconify())).grid(row=3, column=0, ipadx=20, padx=10, pady=10)
    # reg_btn_reg = tki.Button(reg_wnd, text="Регистрация", command=lambda: insert_user(reg_login_entry,
    #                          reg_password_entry, reg_email_entry, 2)).grid(row=3, column=0, ipadx=20, padx=10, pady=10)
    reg_wnd.grab_set()  # эта команда заставляет это окно прехватывать все события (делает окно модальным)
    #reg_wnd.focus_set()
    reg_email_entry.focus_set()  # эта команда устанавливает фокус ввода на это окно
    return

# определяем функции обработчиков кнопок в окне аутентификации
# сначала для кнопки "Войти"
def login(login: tki.Entry, password: tki.Entry):
    st = auth_user(login.get(), password.get())
    if st == []:
        st_user = search_user(login.get())
        if st_user == []:
            print("Нет такого пользователя, хотите зарегистрироваться?")
            reg(login.get(), password.get())
        else:
            print("Не верный пароль!")
        return
    st = list(st[0])
    if (st[0] == "admin") & (st[1] == password.get()):
        print("Здорова, администратор!")
        pass
        auth_wnd.destroy()
        main_wnd.iconify()
    else:
        print("Не верный пароль!")
    return

btn_login = tki.Button(auth_wnd, text="Войти", command=lambda: login(login_entry, password_entry)).\
            grid(row=2, column=0, columnspan=2,  ipadx=50, pady=10)
btn_cancel = tki.Button(auth_wnd, text="Отмена", command=quit).grid(row=3, column=1, ipadx=40, padx=10, pady=10,
                                                                    sticky='e')
btn_reg = tki.Button(auth_wnd, text="Зарегистрироваться", command=lambda: reg(login_entry, password_entry)).\
            grid(row=3, column=0,  padx=10, pady=10)
auth_wnd.grab_set()         # эта команда заставляет это окно прехватывать все события (делает окно модальным)
login_entry.focus_set()     # эта команда устанавливает фокус ввода на это окно


# frame_1 = tki.Frame(main_wnd, width=150, height=150, bg='green')
# frame_2 = tki.Frame(main_wnd, width=150, height=150, bg='yellow')
# frame_3 = tki.Frame(main_wnd, width=300, height=150, bg='blue')
#
# frame_1.place(relx=0, rely=0, relwidth=0.5, relheight=0.5)
# frame_2.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)
# frame_3.place(relx=0, rely=0.5, relwidth=1, relheight=0.2)


# создаем контейнер для таблицы и контейнер для кнопок, оба контейнера размещаем на главном окне
frame_table = tki.Frame(main_wnd, bg='gray') #, width=590)
frame_buttons = tki.Frame(main_wnd, width=150)

# создаем таблицу с колонками с соответствующими названиями столбцов
columns = ("id", "Title", "Author", "Year", "ISBN", "Total quantity", "Available quantity")
treeview: Treeview = ttk.Treeview(frame_table, height=18, show="headings", columns=columns)
treeview.column("id", width=20, anchor="center")  # обозначает столбец, не отображаемый
treeview.column("Title", width=240, anchor="center")
treeview.column("Author", width=160, anchor="center")
treeview.column("Year", width=40, anchor="center")
treeview.column("ISBN", width=90, anchor="center")
treeview.column("Total quantity", width=70, anchor="center")
treeview.column("Available quantity", width=70, anchor="center")
treeview.heading("id", text="id")                   # показать заголовок таблицы
treeview.heading("Title", text="Название")
treeview.heading("Author", text="Автор")
treeview.heading("Year", text="Год")
treeview.heading("ISBN", text="ISBN")
treeview.heading("Total quantity", text="Всего")
treeview.heading("Available quantity", text="В наличии")

# размещаем (пакуем) в контейнере таблицы саму таблицу, полосу вертикальной прокурутки, а затем и сам контейнер
scroll_pane = ttk.Scrollbar(frame_table, command=treeview.yview())
treeview.configure(yscrollcommand=scroll_pane.set)
scroll_pane.pack(side=RIGHT, fill=Y)
treeview.pack(side=LEFT, fill=Y)
frame_table.pack(side=LEFT, fill=BOTH)
# treeview.place(relx=0, rely=0, relwidth=0.8, relheight=1)
#frame_table.place(relx=0, rely=0)


# создаем модальное окно "Форма для поиска книг", предназначенное для ввода данных для поиска интересующей книги
def create_search_wnd():

    # Функция, вызываемая при нажатии кнопки "Искать" в окне "Форма для поиска книг"
    def find_book(title: tki.Entry, author: tki.Entry, year: tki.Entry, isbn: tki.Entry):
        # year_str = year.get()
        # year_int = int(year_str) if year_str else -1
        # isbn_str = isbn.get()
        # isbn_int = int(isbn_str) if isbn_str else -1
        # print(db_actions.search_book(title.get(), author.get(), year_int, isbn_int))
        out_records = search_book(title.get(), author.get(), year.get(), isbn.get())
        print(out_records)  # после отладки программы эту строку удалить
        for i in range(len(out_records)):
            treeview.insert('', i, values=out_records[i])
        search_wnd.destroy()
        main_wnd.iconify() # снова показываем ранее скрытое главное окно
        # main_wnd.focus_set()
        return

    search_wnd = tki.Toplevel()
    main_wnd.withdraw() # скрываем главное (основное окно программы)
    search_wnd.title("Форма для поиска книг")
    search_wnd.geometry("600x220+300+300")
    tki.Label(search_wnd, text="Название книги").grid(row=0, column=0)
    title_entry = tki.Entry(search_wnd, width=80)
    title_entry.grid(row=0, column=1, padx=10, pady=20)
    tki.Label(search_wnd, text="Автор").grid(row=1, column=0)
    author_entry = tki.Entry(search_wnd, width=80)
    author_entry.grid(row=1, column=1, padx=10, pady=0)
    tki.Label(search_wnd, text="Год издания").grid(row=2, column=0)
    year_entry = tki.Entry(search_wnd, width=80)
    year_entry.grid(row=2, column=1, padx=10, pady=20)
    tki.Label(search_wnd, text="ISBN книги").grid(row=3, column=0)
    isbn_entry = tki.Entry(search_wnd, width=80)
    isbn_entry.grid(row=3, column=1, padx=10, pady=0)
    btn1 = tki.Button(search_wnd, text="Искать", width=46, command=lambda: find_book(title_entry, author_entry,
               year_entry, isbn_entry)).grid(row=4, column=1, padx=10, pady=20)
#    btn1.grid(row=4, column=1, padx=10, pady=20)
#    btn1.bind('<Return>', lambda q: search_wnd.destroy())
    search_wnd.grab_set()       # эта команда заставляет это окно прехватывать все события (делает окно модальным)
    search_wnd.focus_set()      # эта команда устанавливает фокус ввода на это окно
    return


def view_my_basket():
    print(view_basket_book())


# размещаем кнопки в контейнере кнопок
btn_search: Button = ttk.Button(frame_buttons, text="Поиск", command=create_search_wnd)
btn_add_to_basket: Button = ttk.Button(frame_buttons, text="Хочу") #, command=pass)
btn_view_basket: Button = ttk.Button(frame_buttons, text="Заказ", command=view_my_basket)
btn_exit: Button = ttk.Button(frame_buttons, text="Выход", command=exit)
btn_about: Button = ttk.Button(frame_buttons, text="О программе") #, command=pass)

btn_search.pack(pady="5")
btn_add_to_basket.pack()
btn_view_basket.pack(pady="5")
btn_exit.pack()
btn_about.pack(side=BOTTOM, pady=5)
# затем размещаем сам контейнер кнопок на главном окне
frame_buttons.pack(side=RIGHT, fill=Y)


# вносим бред в таблицу для проверки отображения
Title = ['Computer1', 'Server', 'Notebook']
Author = ['10.13.71.223', '10.25.61.186', '10.25.11.163']
Year = ['1990', '2000', '2002']
ISBN = ['9781234567897', '1234567890123', '3210987654321']
for i in range(3):  # запись данных
    treeview.insert('', i, values=(i, Title[i], Author[i], Year[i], ISBN[i]))

# далее в коде указываем, что программа может запускаться только напрямую, а не из какого-либо скрипта
if __name__ == "__main__":
    main_wnd.mainloop()  # войти в цикл сообщений главного окна
