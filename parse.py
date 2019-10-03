"""
Програма для пошуку фото в директорії,
записування данних в локальну базу даних
та подальшої відправки на інший сервер

"""

import os
import shutil
import sqlite3

dtbs = 'tz.sqlite3'
"""
перевіряє на існування бази даних
"""
if not os.path.exists(dtbs):
    try:
        # створення бази + створення таблиці
        print('The database is missing \n Created DataBase!')
        connect = sqlite3.connect(dtbs)
        # якщо нема бази створеної то вона автоматично ствоюється
        cursor = connect.cursor()
        cursor.execute('''CREATE TABLE tz (ddk data , num_tz text)''')
        connect.commit()
        print('DataBase create')
    except sqlite3.DatabaseError as err:
        print('Error: ' + str(err))
else:
    print('DataBase in ' + str(os.getcwd() + '\\' + str(dtbs)))
    conn = sqlite3.connect(dtbs)
    curs = conn.cursor()


# функція для дати
def dt_convert(srn=list):
    year = srn[:4]
    month = srn[4:6]
    day = srn[6:8]
    hour = srn[8:10]
    minuts = srn[10:12]
    sec = srn[12:14]
    msec = srn[14:]
    return f'{day}.{month}.{year} {hour}:{minuts}:{sec}:{msec}'.format(srn)


# функція роботи з назвою файлу
def spldate(filename):
    d = filename.split('_')  # розділяє назву на чистини по _
    dt = d[0]  # присвоюєм дату
    num = d[1]  # присвоюєм номер
    date = dt_convert(dt)
    return date, num


# ф-ція перебору файлів у папці
def FolderParse(wlk):
    vehicle = []
    date, fom = os.path.splitext(wlk)  # відділяєм формат від назви файлу
    if fom == '.jpg':  # перевірям чи формат відповідає
        vehicle = spldate(date)  # магія
        print(vehicle)
        Insert(vehicle)
        shutil.copy2(wlk, 'D:\\camera\\arh')
    else:  # якщо ні виводим помилку
        print('This is don\'t .jpg')


# запис в базу даних
def Insert(date=tuple):
    """

    :type date: tuple
    """
    try:  # обробка виключень
        cursor.execute("INSERT INTO tz (ddk, num_tz) VALUES (?, ?)", date)
        print('Recorded')
        conn.commit()
    except sqlite3.DatabaseError as err:  # видає помилку якщо вона є
        print('Error: ' + str(err))


os.chdir('D:\\camera\\fran2')
for i in os.listdir():
    FolderParse(i)
cursor.close()
connect.close()
