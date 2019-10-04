"""
Програма для пошуку фото в директорії,
записування данних в локальну базу даних
та подальшої відправки на інший сервер

"""

import os
import shutil
import sqlite3
from glob import glob

data_base = 'tz.sqlite3'
direct = glob('d:\\camera\\*')

def date_convert(srn):
    """
    функція для дати
    :param srn:
    :return: Date in format dd.mm.yyyy HH:MM:SS:MS
    """
    year = srn[:4]
    month = srn[4:6]
    day = srn[6:8]
    hour = srn[8:10]
    minute = srn[10:12]
    sec = srn[12:14]
    m_sec = srn[14:]
    return f'{day}.{month}.{year} {hour}:{minute}:{sec}:{m_sec}'.format(srn)


def spl_date(filename):
    """
    функція роботи з назвою файлу
    :param filename:
    :return: date, num
    """
    name = filename.split('_')  # розділяє назву на чистини по _
    f_date = name[0]  # присвоюєм дату
    num = name[1]  # присвоюєм номер
    date = date_convert(f_date)
    return date, num


def FolderParse(wlk):
    """
    ф-ція перебору файлів у папці
    :param wlk:
    :return: None
    """
    date, fom = os.path.splitext(wlk)  # відділяєм формат від назви файлу
    if fom == '.jpg':  # перевірям чи формат відповідає
        vehicle = spl_date(date)  # магія
        print(vehicle)
        Insert(vehicle)
        shutil.copy2(wlk, 'D:\\arhiv')
    else:  # якщо ні виводим помилку
        print('This is don\'t .jpg')


def Insert(date):
    """
    запис в базу даних
    :type date: tuple
    """
    try:  # обробка виключень
        cursor.execute("INSERT INTO tz (ddk, num_tz) VALUES (?, ?)", date)
        print('Recorded')
        connect.commit()
    except sqlite3.DatabaseError as err:  # видає помилку якщо вона є
        print('Error: ' + str(err))

# перевіряє на існування бази даних
if not os.path.exists(data_base):
    try:
        # створення бази + створення таблиці
        print('The database is missing \nCreated DataBase!')
        connect = sqlite3.connect(data_base)
        # якщо нема бази створеної то вона автоматично ствоюється
        cursor = connect.cursor()
        cursor.execute('''CREATE TABLE tz (ddk data , num_tz text)''')
        connect.commit()
        print('DataBase create')
    except sqlite3.DatabaseError as err:
        print('Error: ' + str(err))
else: # якщо база вже є то просто підключаємся до неї
    print('DataBase in ' + str(os.getcwd() + '\\' + str(data_base)))
    connect = sqlite3.connect(data_base)
    cursor = connect.cursor()

for d in direct:
    os.chdir(str(d))
    print(d)
    for i in os.listdir(d):
        FolderParse(i)
cursor.close()
connect.close()
