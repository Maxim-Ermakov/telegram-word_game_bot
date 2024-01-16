import telebot
import sqlite3
import stickers
import messages



def build_markup():
    markup = telebot.types.ReplyKeyboardMarkup(resize_keyboard = True)
    markup.add(telebot.types.KeyboardButton('Сбросить до буквы "A" с сохранением счета'))
    return markup



def intro(message, bot):
    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    chat_id = message.chat.id
    first_letter = 'a'
    score = 0
    vocabulary = ''


    cursor.execute('''CREATE TABLE IF NOT EXISTS users_data(
        chat_id INTEGER UNIQUE, 
        first_letter VARCHAR(1),
        score INTEGER,
        vocabulary TEXT
    )''')

    try:
        sql = f'INSERT INTO users_data VALUES(?, ?, ?, ?)'
        data = (chat_id, first_letter, score, vocabulary)
        cursor.execute(sql, data)
    except:
        sql = f'UPDATE users_data SET first_letter = "a" WHERE chat_id = {chat_id}'
        cursor.execute(sql)

    
    connect.commit()

    bot.send_sticker(message.chat.id, stickers.SAY_HELLO)
    bot.send_message(message.chat.id,
        f'''Привет, {message.from_user.first_name}!\n{messages.START_MESSAGE}
      ''',
    )