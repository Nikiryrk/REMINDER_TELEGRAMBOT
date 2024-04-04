from telebot import types

global keyboard1
keyboard1 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnnew = types.KeyboardButton('Создать новую запись')
btnchange = types.KeyboardButton('Мои записи📋')
keyboard1.row(btnnew, btnchange)

global keyboard2
keyboard2 = types.InlineKeyboardMarkup()
btnup = types.InlineKeyboardButton(text='➡️', callback_data='prev')
btndown = types.InlineKeyboardButton(text='⬅️', callback_data='next')
btnren = types.InlineKeyboardButton(text='Изменить', callback_data='chng')
keyboard2.add(btndown,btnren,btnup)
btnback = types.InlineKeyboardButton(text='Назад', callback_data='back')
keyboard2.add(btnback)

global keyboard3
keyboard3 = types.InlineKeyboardMarkup()
keyboard3.add(btndown)

global keyboard4
keyboard4 = types.InlineKeyboardMarkup()
keyboard4.add(btnup)

global keyboard5
keyboard5 = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnrename = types.KeyboardButton('Изменить название')
btnredate = types.KeyboardButton('Изменить дедлайн')
keyboard5.row(btnrename, btnredate)
btndelete = types.KeyboardButton('Удалить')
keyboard5.row(btndelete)
btnback1 = types.KeyboardButton('Назад')
keyboard5.row(btnback1)

global keyboard6
keyboard6 = types.InlineKeyboardMarkup()
btnyes = types.InlineKeyboardButton(text='Да', callback_data='yes')
btnno = types.InlineKeyboardButton(text='Нет', callback_data='no')
keyboard6.add(btnyes,btnno)

global keyboardback
keyboardback = types.ReplyKeyboardMarkup(resize_keyboard=True)
btnback3 = types.KeyboardButton('Назад')
keyboardback.add(btnback3)
