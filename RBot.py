import telebot
import sqlite3
from telebot import types
import datetime
import time
import threading
bot=telebot.TeleBot("Your_bot_Token")
global j,i,data, mt, mdt
polz_id = None
from keyboard import keyboard1,keyboard2,keyboard3,keyboard4,keyboard5,keyboard6,keyboardback



#Starting the bot, the handler of "start" command
@bot.message_handler(commands=['start'])
def start(message):
    global i,polz_id
    i=0
    polz_id = message.chat.id
    conn = sqlite3.connect('YOUR_DB_NAME')
    cur = conn.cursor()
    cur.execute('CREATE TABLE IF NOT EXISTS TABLE_NAME (id TEXT NOT NULL , name TEXT NOT NULL, task TEXT NOT NULL, datatime TEXT NOT NULL)')
    conn.commit()
    cur.close()
    conn.close()
    bot.send_message(message.chat.id, f'Привет, {message.from_user.first_name}!',)
    bot.send_message(message.chat.id, 'Я бот который будет напоминать тебе о важном😉',reply_markup=keyboard1)

#A loop that checks if there are user notes in the database that need to be notified now(checking every 60 seconds)
def check_task():
    while True:
        global data,tt,dtt,j,polz_id
        if polz_id:
            j=0
            conn = sqlite3.connect('YOUR_DB_NAME')
            cursor = conn.cursor()
            cursor.execute('SELECT task, datatime FROM TABLE_NAME WHERE id = ?', [polz_id])
            data2 = cursor.fetchall()
            conn.close()
            while j < len(data2):
                tt, dtt = data2[j]
                min_difference = datetime.timedelta(minutes=1)
                checkt = datetime.datetime.strptime(dtt, '%d.%m.%Y %H:%M')
                current_time = datetime.datetime.now()
                if ((checkt - current_time) < min_difference):
                    bot.send_message(polz_id,f'Напоминаю, {tt}')
                    conn = sqlite3.connect('hubs.sql')
                    cursor = conn.cursor()
                    cursor.execute("DELETE FROM zp WHERE task = ? AND datatime = ?",(tt,dtt))
                    conn.commit()
                    conn.close()
                    j += 1
                elif  (checkt.date() == (current_time + datetime.timedelta(days=1)).date() and checkt.hour == current_time.hour and checkt.minute == current_time.minute):
                    bot.send_message(polz_id, f'Напоминаю, {tt} уже завтра')
                    j += 1
                else:
                    j += 1
        time.sleep(60)
t = threading.Thread(target=check_task)
t.start()



#Button callback handler
@bot.callback_query_handler(func=lambda call: True)
def callback_handler(callback):
    global i,data
    if callback.data == 'prev':
        i += 1
        if i < len(data):
            mt, mdt = data[i]
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.id,text=f'Название: {mt}\nДедлайн: {mdt}', reply_markup=keyboard2)
        else:
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.id,text='записей больше нет', reply_markup=keyboard3)
    elif callback.data == 'next':
        i -= 1
        if i >= 0:
            mt, mdt = data[i]
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.id,text=f'Название: {mt}\nДедлайн: {mdt}', reply_markup=keyboard2)
        else:
            bot.edit_message_text(chat_id=callback.message.chat.id,message_id=callback.message.id,text='Записей больше нет', reply_markup=keyboard4)
    elif callback.data == 'chng':
        bot.send_message(callback.message.chat.id,f'Что сделать с записью?', reply_markup=keyboard5)
        bot.register_next_step_handler(callback.message,rename)
    elif callback.data == 'yes':
        mt, mdt = data[i]
        conn = sqlite3.connect('YOUR_DB_NAME')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM zp WHERE TABLE_NAME = ? AND datatime = ?",(mt,mdt))
        conn.commit()
        conn.close()
        bot.send_message(callback.message.chat.id,'Запись удалена👌', reply_markup=keyboard1)
    elif callback.data == 'no':
        change_task(callback.message)
    elif callback.data == 'back':
        bot.send_message(callback.message.chat.id,'Назад', reply_markup=keyboard1)
        start2(callback.message)
#Create new notes and viewing existing now
@bot.message_handler(content_types=['text'])
def start2(message):
    if (message.text== 'Создать новую запись'):
        new_task(message)
    elif (message.text== 'Мои записи📋'):
        conn = sqlite3.connect('hubs.sql')
        cur = conn.cursor()
        exists = cur.execute("SELECT 1 FROM TABLE_NAME WHERE id = ?", [message.from_user.id]).fetchone()
        if exists:
            change_task(message)
        else:
            bot.send_message(message.chat.id, 'У вас ещё нет ни одной напоминалки🥺', reply_markup=keyboard1)
    else: bot.send_message(message.chat.id, 'Выбирете одну из кнопок ниже',reply_markup=keyboard1)
#Create new notes
def new_task(message):
    bot.send_message(message.chat.id, 'Давай создадим напоминалку', reply_markup=keyboardback)
    bot.send_message(message.chat.id, 'Напишите название')
    bot.register_next_step_handler(message, name)
def name (message):
    if message.text == "Назад":
        start2(message)
    else:
        global task
        task = message.text.strip()
        bot.send_message(message.chat.id, 'Впишите дату и время события(ДД.ММ.ГГГГ чч:мм.)')
        bot.register_next_step_handler(message, time_task)
def time_task(message):
    global date
    date = message.text.strip()
    try:
        time = datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        now = datetime.datetime.now()
        delta = time - now
        if (delta.total_seconds() <= 0):
            bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
            bot.register_next_step_handler(message, time_task)
        else:
            conn = sqlite3.connect('YOUR_DB_NAME')
            cur = conn.cursor()
            cur.execute('INSERT INTO TABLE_NAME (id, name,task,datatime) VALUES("%s","%s","%s","%s")' % (message.from_user.id, message.from_user.first_name,task,date))
            conn.commit()
            cur.close()
            conn.close()
            bot.send_message(message.chat.id, 'Всё записано, обязательно напомню🙌', reply_markup=keyboard1)
    except ValueError:
        bot.send_message(message.chat.id, 'Неккоректные данные, попробуйте ещё раз.')
        bot.register_next_step_handler(message, time_task)
#Viewing and editing existing notes
def change_task(message):
    global data
    i=0
    bot.send_message(message.chat.id, 'Давай изменим напоминалку', reply_markup=types.ReplyKeyboardRemove())
    conn = sqlite3.connect('YOUR_DB_NAME')
    cursor = conn.cursor()
    cursor.execute('SELECT "task", datatime FROM "NAME_TABLE_FROM_YOUR_DB" WHERE id = ?', [message.from_user.id])
    data = cursor.fetchall()
    conn.close()
    if i < len(data):
        mt, mdt = data[i]
        bot.send_message(message.chat.id, f'Название: {mt}\nДедлайн: {mdt}',reply_markup=keyboard2)
#Choice: rename,change deadline or delete note
def rename(message):
    global i
    mt, mdt = data[i]
    if (message.text== 'Изменить название'):
        conn = sqlite3.connect('YOUR_DB_NAME')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TABLE_NAME WHERE task = ? AND datatime = ?",(mt,mdt))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, 'Введите новое название',reply_markup=keyboardback)
        bot.register_next_step_handler(message, change_name)
    elif (message.text== 'Изменить дедлайн'):
        conn = sqlite3.connect('YOUR_DB_NAME')
        cursor = conn.cursor()
        cursor.execute("DELETE FROM TABLE_NAME WHERE task = ? AND datatime = ?",(mt,mdt))
        conn.commit()
        conn.close()
        bot.send_message(message.chat.id, 'Введите новый дедлайн (ДД.ММ.ГГГГ чч:мм.)')
        bot.register_next_step_handler(message, change_deadline)
    elif(message.text=='Удалить'):
        bot.send_message(message.chat.id,f'Вы уверены что хотите удалить запись? \n Название:{mt}\nДедлайн: {mdt}',reply_markup=keyboard6)

    elif(message.text == 'Назад'):
        change_task(message)
#Change notes name
def change_name(message):
    mt, mdt = data[i]
    if (message.text== 'Назад'):
        bot.send_message(message.chat.id, 'Назад',reply_markup=keyboard5)
        rename()
    else:
        nt = message.text.strip()
        conn = sqlite3.connect('YOR_DB_NAME')
        cur = conn.cursor()
        cur.execute('INSERT INTO TABLE_NAME (id, name,task,datatime) VALUES("%s","%s","%s","%s")' % (message.from_user.id, message.from_user.first_name,nt,mdt))
        conn.commit()
        cur.close()
        conn.close()
        bot.send_message(message.chat.id, 'Название изменено👌', reply_markup=keyboard1)
#Change notes deadline
def change_deadline(message):
    global newdl
    mt, mdt = data[i]
    newdl = message.text.strip()
    try:
        time = datetime.datetime.strptime(message.text, '%d.%m.%Y %H:%M')
        now = datetime.datetime.now()
        delta = time - now
        if (delta.total_seconds() <= 0):
            bot.send_message(message.chat.id, 'Вы ввели прошедшую дату, попробуйте еще раз.')
            bot.register_next_step_handler(message, change_deadline)
        elif (message.text== 'Назад'):
            bot.send_message(message.chat.id, 'Назад')
            rename()
        else:
            conn = sqlite3.connect('hubs.sql')
            cur = conn.cursor()
            cur.execute('INSERT INTO TABlE_NAME (id, name,task,datatime) VALUES("%s","%s","%s","%s")' % (message.from_user.id, message.from_user.first_name,mt,newdl))
            conn.commit()
            cur.close()
            conn.close()
            bot.send_message(message.chat.id,'Время изменено👌', reply_markup=keyboard1)
    except ValueError:
        bot.edit_message_text(message.chat.id, 'Неккоректные данные, попробуйте ещё раз.')
        bot.register_next_step_handler(message, change_deadline)
bot.infinity_polling()
