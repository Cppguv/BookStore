# Для работы с Системой Управления Базой Данных (СУБД) типа SQLite нужно подключить библиотеку sqlite3. Можно и какую-
# либо другую типа MySQL, PostgreSQL, Oracle (она же FireBird, она же InterBase), Microsoft SQL Server, или подобные,
# но их в отличие от втроенной sqlite необходимо будет сначала отделно установить на компьютер и запустить
import sqlite3


#########################################################################
#	Создаем базу данных bookstore.db и в ней пять таблиц 
# (схема таблиц по ссылке: https://drive.google.com/file/d/1WY9vopgugv0zp88DGgOUXWoiYfp95mK0/view?usp=sharing , доступ к файлу разрешен пользователю khmylova03@gmail.com)
# для этого определим функцию init_db(), в которой будет проводится вся необходимая инициализация
# причем инициализация должна работать только один раз, если файл базы данных еще отсутствует, либо БД пуста
#########################################################################

def init_db():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    
    # создаем таблицу book, в которой будут храниться данные о книгах:
    # title - текстовое поле с названием книги, не может быть пустым
    # author - текстовое поле, в котором содержиться фамилия автора книги
    # year - целочисленное поле с годом издания книги
    # isbn - целочисленное поле с уникальным номером издания (Международный стандартный книжный номер (англ. International Standard Book Number, сокращённо — англ. ISBN) —
    #        уникальный номер книжного издания, необходимый для распространения книги в торговых сетях и автоматизации работы с изданием. Википедия)
    # total_quantity -  общее количество экземпляров конкретной книги, числящихся в библиотеке (равно сумме книг выданных на руки и книг доступных для выдачи)
    # available - оставшееся в библиотеке количество экземпляров конкретной книги, доступное для выдачи пользователям
    cur.execute("CREATE TABLE IF NOT EXISTS book (id INTEGER PRIMARY KEY, title TEXT NOT NULL, author TEXT, year INTEGER, isbn INTEGER UNIQUE, total_quantity INTEGER, available INTEGER)")
    
    # создаем таблицу role, в которой будут храниться данные о ролях пользователей нашей библиотеки:
    # role - текстовое поле с названием роли, например admin - администратор библиотеки, который будет обладать полными правами по работе с ней: может добавлять новые книги в базу,
    # редактировать их, выдавать книги обычным пользователям (добавлять их в корзину), добавлять, удалять, редактировать пользователей и прочее,
    # или например роль user - обычный пользователь, который может просматривать содержимое библиотеки, искать книги, а также редактировать свои учетные данные - пароль и e-mail
    # данное поле не может быть пустым и содержит уникальное значение, то есть не может в данной таблице содержаться более одной записи admin или user или например moderator
    # также по замыслу в данное поле может добавлять данные или редактировать их только администратор, поэтому его (администратора) будем создавать далее в программе в первую очередь
    cur.execute("CREATE TABLE IF NOT EXISTS role (id INTEGER PRIMARY KEY, role TEXT NOT NULL UNIQUE)")

    # создаем таблицу user, в которой будут храниться учетные данные пользователей библиотеки:
    # user - имя (логин) пользователя, текстовое поле, не может быть пустым, должно быть уникальным, то есть в таблице не может быть более одной записи с одинаковыми логинами
    # password - пароль, текстовое, не может быть пустым
    # email - адрес электронной почты пользователя, текстовое поле, не обязательно для заполнения, по идее должно быть уникальным, но оставим пока так
    # role_id - целочисленное поле внешнего ключа, связанного с полем id таблицы role
    cur.execute("CREATE TABLE IF NOT EXISTS user (id INTEGER PRIMARY KEY, user TEXT NOT NULL UNIQUE, password TEXT NOT NULL, email TEXT, role_id INTEGER REFERENCES role (id))")
    
    # создаем таблицу basket, в которой будут храниться данные о "корзине" пользователя библиотеки, при этом у каждого пользоватея только одна своя корзина:
    # user_id - целочисленное поле внешнего ключа, связанного с полем id таблицы user
    cur.execute("CREATE TABLE IF NOT EXISTS basket (id INTEGER PRIMARY KEY, user_id INTEGER UNIQUE REFERENCES user (id))")
    
    # создаем таблицу basket_book, в которой будут храниться данные о "корзинах" пользователя библиотеки и их содержимом:
    # book_id - целочисленное поле внешнего ключа, связанного с полем id таблицы book
    # quantity - количество экземпляров конкретной книги, выдаваемых пользователю из библиотеки (обычно одно), целочисленное поле, по идее не может быть больше значения разности
    # полей total_quantity - available из талицы book
    # date - дата выдачи книг на руки пользователю
    # basket_id - целочисленное поле внешнего ключа, связанного с полем id таблицы basket
    cur.execute("CREATE TABLE IF NOT EXISTS basket_book (id INTEGER PRIMARY KEY, book_id INTEGER REFERENCES book (id), "
                "quantity INTEGER NOT NULL, date DATE, basket_id INTEGER REFERENCES basket (id))")
    
    # сохраняем сделанные изменения в базу данных
    # conn.commit()

    # в первую очередь создаем роль admin, затем роль user и затем пользователя admin, если такие еще не созданы
    cur.execute("SELECT role FROM role WHERE role = ?", ("admin",))
    if not cur.fetchall():
        cur.execute("INSERT INTO role VALUES(NULL,?)", ("admin",))
    cur.execute("SELECT role FROM role WHERE role = ?", ("user",))
    if not cur.fetchall():
        cur.execute("INSERT INTO role VALUES(NULL,?)", ("user",))
    cur.execute("SELECT user FROM user WHERE user = ?", ("admin",))
    if not cur.fetchall():
        cur.execute("INSERT INTO user VALUES(NULL,?,?,?,?)", ("admin", "admin", "", 1))

    # сохраняем сделанные изменения в базу данных, а затем закрываем соединение с базой данных для экономии рессурсов компьютера
    conn.commit()
    conn.close()



#########################################################################
#	Функции доступа к данным таблицы book
#########################################################################

# вставка новой записи в таблицу book
def insert_book(title, author, year, isbn, total_quantity):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    # указание параметра NULL означает, что поле id будет автоматически инкрементироваться (увеличиваться на один)
    # изначально при добавлении данных о новой книге поле available равно общему количеству книг total_quantity, так как еще ни одной книги не выдано пользователям
    cur.execute("INSERT INTO book VALUES(NULL,?,?,?,?,?,?)", (title,author,year,isbn,total_quantity,total_quantity))
    conn.commit()
    conn.close()

# функция, возвращающая все имеющиеся записи в таблице book для последующего отображения их в окне программы (ну или в терминале (консоли) с помощью команды print)
def view_book():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book")
    rows = cur.fetchall()
    conn.close()
    return rows

# поиск записей в таблице book, удовлетаоряющих запросу по названию книги, автору, году издания или номеру ISBN
def search_book(title="", author="", year="", isbn=""):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM book WHERE title = ? OR author = ? OR year = ? "
                "OR isbn = ?", (title, author, year, isbn))
    rows = cur.fetchall()
    conn.close()
    return rows

# удаление записи с указанным полем id из таблицы book
def delete_book(id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM book WHERE id = ?", (id,))
    conn.commit()
    conn.close()

# обновление (редактирование) записи с указанным полем id в таблице book
def update_book(id, title, author, year, isbn, total_quantity):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    # находим значение поля quantity таблицы basket_book, в котором содержится значение количества выданных экземпляров данной книги
    cur.execute("SELECT quantity FROM basket_book WHERE book_id = ?", (id))
    # теперь находим новое значение оставшихся в хранилище доступных для выдачи книг
    available = total_quantity - cur.fetchall()
    if available < 0:
        print("Указанное общее количество книг в библиотеке не может быть меньше количества находящихся на руках у пользователей: ", cur.fetchall(), "книг.")
        print("Все изменения будут проигнорированы.")
        conn.close()
        return
    cur.execute("UPDATE book SET title = ?, author = ?, year = ?, isbn = ?, total_quantity = ? WHERE id = ?", (title, author, year, isbn, total_quantity, available, id))
    conn.commit()
    conn.close()



#########################################################################
#	Функции доступа к данным таблицы role (хотя в принципе эту таблицу мы уже заполнили в процессе инициализации БД, но пусть будут на всякий случай - вдруг потом пригодятся)
#########################################################################

def insert_role(role):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    # указание параметра NULL означает, что поле id будет автоматически инкрементироваться (увеличиваться на один)
    cur.execute("INSERT INTO role VALUES(NULL,?)", (role))
    conn.commit()
    conn.close()

def view_role():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM role")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_role(role=""):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM role WHERE role = ?", (role))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_role(id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM role WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_role(id, role):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("UPDATE role SET role = ? WHERE id = ?", (role, id))
    conn.commit()
    conn.close()
	
	
	
#########################################################################
#	Функции доступа к данным таблицы user (по аналогии с функциями для работы с таблицей book)
#########################################################################

def insert_user(user, password, email, role_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    # указание параметра NULL означает, что поле id будет автоматически инкрементироваться (увеличиваться на один)
    cur.execute("INSERT INTO user VALUES(NULL,?,?,?,?)", (user, password, email, role_id))
    conn.commit()
    conn.close()

def view_user():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_user(user=""):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM user WHERE user = ?", (user,))
    rows = cur.fetchall()
    conn.close()
    return rows

# def search_email(email=""):
#     conn = sqlite3.connect("bookstore.db")
#     cur = conn.cursor()
#     cur.execute("SELECT * FROM user WHERE email = ?", (email,))
#     rows = cur.fetchall()
#     conn.close()
#     return rows

def auth_user(user="", password=""):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT user, password FROM user WHERE user = ? AND password = ?", (user, password))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_user(id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM user WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_user(id, password, email, role_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("UPDATE user SET password = ?, email = ?, role_id = ? WHERE id = ?", (password, email, role_id))
    conn.commit()
    conn.close()



#########################################################################
#	Функции доступа к данным таблицы basket
#########################################################################

def insert_basket(user_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    #the NULL parameter is for the auto-incremented id
    cur.execute("INSERT INTO basket VALUES(NULL,?)", (user_id))
    conn.commit()
    conn.close()

def search_basket(user_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket WHERE user_id = ?", (user_id))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_basket(id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM basket WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_basket(id, user_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("UPDATE basket SET user_id = ? WHERE id = ?", (user_id, id))
    conn.commit()
    conn.close()



#########################################################################
#	Функции доступа к данным таблицы basket_book
#########################################################################

def insert_basket_book(book_id, quantity, date, basket_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    # указание параметра NULL означает, что поле id будет автоматически инкрементироваться (увеличиваться на один)
    cur.execute("INSERT INTO basket_book VALUES(NULL,?,?,?,?)", (book_id, quantity, date, basket_id))
    conn.commit()
    conn.close()

def view_basket_book():
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket_book")
    rows = cur.fetchall()
    conn.close()
    return rows

def search_basket_book(book_id=0, date="", basket_id=0):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("SELECT * FROM basket_book WHERE book_id = ? OR date = ? OR basket_id = ?", (book_id, date, basket_id))
    rows = cur.fetchall()
    conn.close()
    return rows

def delete_basket_book(id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("DELETE FROM basket_book WHERE id = ?", (id,))
    conn.commit()
    conn.close()

def update_basket_book(id, book_id, quantity, date, basket_id):
    conn = sqlite3.connect("bookstore.db")
    cur = conn.cursor()
    cur.execute("UPDATE basket_book SET book_id = ?, quantity = ?, date = ?, basket_id = ? WHERE id = ?", (book_id, quantity, date, basket_id, id))
    conn.commit()
    conn.close()



# теперь проверим работоспособность вышесозданных наших функций
if __name__ == "__main__":
    init_db()
    #insert_book("another novel", "James W.", 2017, 1234, 2)
    #update(2, title = "new book", author= "DH", year= 2005, isbn= 5555)
    print(view_book())
    print(view_role())
    print(view_user())
    print(auth_user('admin', 'admin'))

# Конечно код еще сыроват, нужно будет осуществить обработку исключений при работе с запросами к БД (базе данных), проверку корректности вводимых данных
# в наши формы ввода данных, возможно добавить еще какие-нибудь фичи (возможности) в программу, для умощнения ее функционала, а после произвести рефакторинг кода
# (совершенствование) для улучшение читаемости кода, его оптимизации, исключения повторяемости некоторых фрагментов кода, и сделать это, наверное, 
# лучше всего с использованием классов.
#