# Reminder in the telegram bot without timer(telebot)
This bot made for helping people not forget their tasks. If you do project like that, you will take any part of this code, for solving your problems or take idea.
## Installation
```rb
pip install pyTelegramBotAPI
pip install threaded
pip install sqlite3-api
```
## Libraries
```
import telebot
import sqlite3
from telebot import types
import datetime
import time
import threading
```
To send messages in time, a loop was created that runs every minute and checks the database
```
def check_task():
    while True:
        global data,tt,dtt,j,polz_id
        if polz_id:
            j=0
            conn = sqlite3.connect('hubs.sql')
            cursor = conn.cursor()
            cursor.execute('SELECT task, datatime FROM zp WHERE id = ?', [polz_id])
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
```
## Documentation
https://pypi.org/project/pyTelegramBotAPI/ 

https://docs.python.org/3/library/threading.html

You can read the full code in the attached file

## Bot link
https://t.me/remrume_bot

