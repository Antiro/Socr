from flask import Flask, request, render_template, redirect, url_for
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
        return 1
        # вы зарегестрированы
    else:
        return 0
        # Данный Login занят, придумайте другой


# вход
def logi(log,pas):
    heLog = hashlib.md5(log.encode()).hexdigest()
    hePas = hashlib.md5(pas.encode()).hexdigest()

    if cursor.execute(f"SELECT * FROM users WHERE login = '{heLog}'").fetchone() is None:
        return 0
        # нет такого пользователя
    else:
        global id
        id = cursor.execute(f"SELECT id FROM users WHERE login = '{heLog}' AND password='{hePas}'").fetchone()[0]
        if id is None:
            return 2
            # неправильный пароль или логин
        else:
            cursor.execute(f'INSERT INTO users_online (id) VALUES ({id})')
            conn.commit()
            return 1 
            # вошли


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
    arr=[]
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        arr.append('Вы не зарегестрированы, войдите в аккаунт')
    else:
        addUrl=cursor.execute(f"SELECT * FROM general WHERE url = '{url}'").fetchone()
        if addUrl is None:
            shURL=get_shortURL(url)
            cursor.execute(f"INSERT INTO general (url,short,id_user) VALUES (?,?,?)", (url,shURL,id))
            conn.commit()
            arr.append("Ссылка добавлена в общий список")
            arr.append(shURL)
        else:
            arr.append("Ссылка взята из общего списока")
            arr.append(addUrl[2])


# все публичные ссылки пользователя
def allGebUrlUser(id_user):
    arr=[]
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
       arr.append('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM general WHERE id_user = {id_user}").fetchall()
        
        if url == []:
            arr.append("У вас нет публичных ссылок")
        else:
            for i in range(len(url)):
                arr.append(f'id - {url[i][0]} / URL - <a href="{url[i][2]}">{url[i][2]}</a>')
                
    return arr

   
# все публичные ссылки
def allGebUrl():
    arr=[]
    url=cursor.execute(f"SELECT * FROM general").fetchall()
    if url == []:
        arr.append("Нет публичных сокрашенных ссылок")
    else:
        for i in range(len(url)):
            arr.append([url[i][0],url[i][2]])
    
    return arr


# удаление публичной ссылки пользователя
def delGebUrl(id_user,id):
    arr=[]
    if cursor.execute(f"SELECT * FROM users_online WHERE id = {id}").fetchone() is None:
        arr.append('Вы не зарегестрированы, войдите в аккаунт')
    else:
        url=cursor.execute(f"SELECT * FROM general WHERE id_user = {id_user} AND id = {id}").fetchone()
        if url is None:
            arr.append("Ошибка ввода информации")
        else:
            cursor.execute(f"DELETE FROM general WHERE id={id}").fetchone()
            conn.commit()
            arr.append("Ссылка удалена")


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



app = Flask(__name__)


# вход
@app.route('/')
def index():
    return render_template('index.html',title="Вход")

@app.route('/sub',methods = ['POST', 'GET'])
def login():
    name = request.form['Name']
    password=request.form['password']

    log=logi(name,password)
      
    if log == 1:
        return redirect(url_for('pub'))
    elif log == 0:
        info="Нет такого ползователя"
        return redirect(url_for('index'))
    else:
        info="Неправильный логин или пароль"
        return redirect(url_for('index'))

# регистрация
@app.route('/reg')
def regs():
    return render_template('reg.html',title="Регистрация")

@app.route('/registr',methods = ['POST', 'GET'])
def registr():
    name = request.form['Name']
    password=request.form['password']

    regi=reg(name,password)
    
    if regi == 0:
        info="Такой Name уже занят, придумайте другой"
        return redirect(url_for('reg'))
    else:
        info = "Вы зарегистрированы"
        return redirect(url_for('index'))



# публичные ссылки
@app.route('/pub')
def pub():
    urlP=allGebUrl()
    return render_template('pub.html',urlAll=urlP)


@app.route('/private')
def private():
    return render_template('private.html',title="Приватные ссылки")



if __name__ == '__main__':
    app.run()
