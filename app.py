import pyshorteners
import sqlite3
import hashlib
import time


# БД
conn = sqlite3.connect('db.db', check_same_thread=False)
cursor = conn.cursor()

# функции

def get_shortURL(url):
    return(pyshorteners.Shortener().tinyurl.short(url))


# регистрация
def reg(log,pas):
    heLog = hashlib.md5(log.encode()).hexdigest()
    hePas = hashlib.md5(pas.encode()).hexdigest()
    if cursor.execute(f"SELECT * FROM users WHERE login = '{heLog}'").fetchone() is None:
        cursor.execute(f'INSERT INTO users (login,password) VALUES (?,?)', (heLog,hePas))
        conn.commit()
        print('Готово, вы зарегестрированы !')
    else:
        print('Данный Login занят, придумайте другой')


# вход
def logi(log,pas):
    heLog = hashlib.md5(log.encode()).hexdigest()
    hePas = hashlib.md5(pas.encode()).hexdigest()

    if cursor.execute(f"SELECT * FROM users WHERE login = '{heLog}'").fetchone() is None:
        print('Такого пользователея нет, зарегестрируйтесь')
    else:
        global id
        id = cursor.execute(f"SELECT id FROM users WHERE login = '{heLog}' AND password='{hePas}'").fetchone()[0]
        if id is None:
            print('Неправильный логин или пароль !')
        else:
            cursor.execute(f'INSERT INTO users_online (id) VALUES ({id})')
            conn.commit()
            print('Вы вошли!')


# выход из аккаунта
def exit(id):
    # time.sleep(5)
    cursor.execute(f"DELETE FROM users_online WHERE id={id}").fetchone()
    conn.commit()
    print("Вы из вышли аккаунта")


# 
# 
# Публичные
# 
# 


# добавление публичной ссылки
def add_genURL(id,url):
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else:
        addUrl=cursor.execute(f"SELECT * FROM general WHERE url = '{url}'").fetchone()
        if addUrl is None:
            shURL=get_shortURL(url)
            cursor.execute(f"INSERT INTO general (url,short,id_user) VALUES (?,?,?)", (url,shURL,id))
            conn.commit()
            print("Ссылка добавлена в общий список")
            print(shURL)
        else:
            print("Ссылка взята из общего списока")
            print(addUrl[2])


# все публичные ссылки пользователя
def allGebUrlUser(id_user):
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM general WHERE id_user = {id_user}").fetchall()
        if url == []:
            print("У вас нет публичных ссылок")
        else:
            print("Ваши публичные сокращенные ссылки:")
            for i in range(len(url)):
                print(f'id - {url[i][0]} / URL - {url[i][2]}')

   
# все публичные ссылки
def allGebUrl():
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM general").fetchall()
        if url == []:
            print("Нет публичных сокрашенных ссылок")
        else:
            print("Все публичные сокращенные ссылки:")
            for i in range(len(url)):
                print(f'id - {url[i][0]} / URL - {url[i][2]}')


# удаление публичной ссылки пользователя
def delGebUrl(id_user,id):
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM general WHERE id_user = {id_user} AND id = {id}").fetchone()
        if url is None:
            print("Ошибка ввода информации")
        else:
            cursor.execute(f"DELETE FROM general WHERE id={id}").fetchone()
            conn.commit()
            print("Ссылка удалена")
        

# 
# 
# Приватные
# 
# 


# добавление приватной ссылки
def add_prURL(id_user,url):
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else: 
        addUrl=cursor.execute(f"SELECT * FROM private WHERE url = '{url}' AND id_user = {id_user}").fetchone()
        if addUrl is None:
            shURL=get_shortURL(url)
            cursor.execute(f"INSERT INTO private (url,short,id_user) VALUES (?,?,?)", (url,shURL,id_user))
            conn.commit()
            print("Ссылка добавлена в ваш приватный список")
            print(shURL)
        else:
            print("Ссылка взята из вашего приватного списка")
            print(addUrl[2])


# все приватные ссылки пользователя
def allPrUrlUser(id_user):
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM private WHERE id_user = {id_user}").fetchall()
        if url == []:
            print("У вас нет приватных ссылок")
        else:
            print("Ваши приватные сокращенные ссылки:")
            for i in range(len(url)):
                print(f'id - {url[i][0]} / URL - {url[i][2]}')
        


# удаление приватной ссылки пользователя
def delPrUrl(id_user,id):
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        print('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM private WHERE id_user = '{id_user}' AND id = '{id}'").fetchone()
        if url is None:
            print("Ошибка ввода информации")
        else:
            cursor.execute(f"DELETE FROM private WHERE id={id}").fetchone()
            conn.commit()
            print("Ссылка удалена")


# Проверка

# сокращение ссылки
# print (get_shortURL("https://www.avito.ru/chelyabinsk/tovary_dlya_kompyutera/topovyy_izognutyy_curved_monitor_samsung_fullhd_2275547029"))

# Публичные

# удаление
# delGebUrl(2,3)

#вывод всех публичных ссылок пользователя 
# allGebUrlUser(1,4)

# вывод всех публичных ссылок
# allGebUrl()

# добавлени ссылки
# add_genURL("https://www.avito.ru/chelyabinsk/tovary_dlya_kompyutera/videokarta_rtx_3090_gigabyte_aorus_na_garantii_2293381009")
    

# Приватные

# добавление ссылки
# add_prURL(1,'https://www.avito.ru/chelyabinsk/tovary_dlya_kompyutera/topovyy_izognutyy_curved_monitor_samsung_fullhd_2275547029')

# просмотр приватных ссылок
# allPrUrlUser(2)

# удаление ссылки
# delPrUrl(1,3)

# регистрация
# print("Регистрация")
# login = input("Login = ")
# password=input("Password = ")
# reg(log=login,pas=password)


# вход
# print("Вход")
# login = input("Login = ")
# password=input("Password = ")
# logi(log=login,pas=password)

# выход
# exit()