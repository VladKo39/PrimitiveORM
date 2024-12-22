import sqlite3
import create_data
import re

disc_prod = create_data.create_data_bot()

def initiate_db():
    # создаёт таблицы Products,Users если онb ещё не созданы при помощи SQL запроса.
    connection = sqlite3.connect('data_bot.db')
    # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
    cursor = connection.cursor()
    # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.

    #########Products###########################################################
    cursor.execute('''                            
    CREATE TABLE IF NOT EXISTS Products(
    id INTEGER PRIMARY KEY ,
    title TEXT NOT NULL,
    description TEXT ,
    price INTEGER NOT NULL
    );
    ''')
    #Создание таблицы Products

    cursor.execute('''       
            DELETE FROM Products
            ''')
    # для заполнения данных таблицы Products очищаю её
    create_data.create_data_bot()
    # вызываю функцию подготовки данных для загрузки в таблицу Products

    for key, value in disc_prod.items():
        # для перебора элементов словаря disc_prod с данными
        title_ = value[0]
        description_ = value[1]
        price_ = value[2]
        cursor.execute('INSERT INTO Products('
                       'title,'
                       'description,'
                       'price) '
                       ' VALUES(?,?,?)',
                       (title_,
                        description_,
                        price_
                        )
                       )
        # заполняю таблицу Products данными из словаря

    connection.commit()
    # сохраняем изменения
    #########Users###########################################################
    cursor.execute('''                            
        CREATE TABLE IF NOT EXISTS Users(
        id INTEGER PRIMARY KEY ,
        username TEXT NOT NULL,
        email TEXT NOT NULL,
        age INTEGER NOT NULL,
        balance INTEGER NOT NULL
        );
        ''')

    connection.commit()
    #сохраняем значения
    connection.close()
    # отключаем подключение

def add_user(username, email, age):
    '''
    функция добавляет в таблицу Users вашей БД запись с переданными данными.
    Баланс у новых пользователей всегда равен 1000.
    :param username: имя пользователя
    :param email:    email пользователя
    :param age:      возраст
    :return:
    '''
    connection = sqlite3.connect('data_bot.db')
    # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
    cursor = connection.cursor()
    # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.
    cursor.execute("SELECT MAX(id) FROM Users")
    total_max = cursor.fetchone()[0]
    total_max+=1

    cursor.execute(f'''
            INSERT INTO Users VALUES ('{total_max}','{username}','{email}','{age}',1000)
            ''')
    connection.commit()
    # сохраняем значения
    connection.close()
    # отключаем подключение

def is_included(username):
    '''
    # принимает имя пользователя и возвращает True,
    # если такой пользователь есть в таблице Users, в противном случае False.
    # :param username: имя пользователя
    # :return: if username present in the table = True else =False
    '''
    check_list='[а-я~`{}!"#№%:^?&*()-+/|\?><,:;]'
    #Символы запрещеннные для ввода пользователя
    if re.search(check_list, username.lower()):
        return True
    else:
        connection = sqlite3.connect('data_bot.db')
        # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
        cursor = connection.cursor()
        # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.
        check_user = cursor.execute('SELECT * FROM Users WHERE username=?',
                                    (username,))
        if check_user.fetchone() is None:
            return False
        else:
            return True
        connection.close()
        # отключаем подключение


def is_includ_email(email):
    '''
    принимает email пользователя и возвращает True,
    если такой пользователь есть в таблице Users, в противном случае False.
    :param email: email пользователя
    :return: if email present in the table = True else =False
    '''
    check_list = '[а-я~`{}!"#№%:^?&*()+/|\?><,:;]'
    #Символы запрещеннные для ввода email
    if re.search(check_list, email.lower()):
        return True
    else:
        connection = sqlite3.connect('data_bot.db')
        # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
        cursor = connection.cursor()
        # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.
        check_email = cursor.execute('SELECT * FROM Users WHERE email=?',
                                    (email,))
        if check_email.fetchone() is None:
            return False
        else:
            return True
        connection.close()
        # отключаем подключение


def get_all_products():
    connection = sqlite3.connect('data_bot.db')
    # # подключение к базе данных not_telegram.db с помощью библиотеки sqlite3
    cursor = connection.cursor()
    # # создаю объект cursor для выполнения SQL-запросов и операций с базой данных.

    cursor.execute("SELECT * FROM Products")
    return cursor.fetchall()
    connection.close()
    # отключаем подключение
if __name__ == '__main__':
    initiate_db()
    get_all_products()



