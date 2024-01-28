# pip install pytelegrambotapi pyenchant
import telebot
import config
import messages
import enchant
import sqlite3
from time import sleep
from utils import intro, build_markup


bot = telebot.TeleBot(config.TOKEN)
dic = enchant.Dict('en_US')


@bot.message_handler(commands=['start'])
def start(message):
    intro(message, bot)


@bot.message_handler(content_types=['text'])
def game(message):
    if message.text == 'Сбросить до буквы "A" с сохранением счёта':
        intro(message, bot)
        return

    chat_id = message.chat.id
    word = message.text.lower()

    connect = sqlite3.connect('database.db')
    cursor = connect.cursor()

    cursor.execute(f"""
        SELECT first_letter, score, vocabulary FROM users_data
        WHERE chat_id={chat_id}
    """)
    first_letter, score, vocabulary = cursor.fetchone()

    if len(word) < 2:
        text_message = 'Слово не должно состоять из одной буквы!'
    elif word[0] == first_letter and dic.check(word):
        first_letter = word[-1]

        if word not in vocabulary:
            score += 1
            vocabulary += f', {word}'
            text_message = f'Супер! Твой счёт: {score}! Теперь напиши слово на букву "{first_letter}"'
        else:
            text_message = f'{messages.AGAIN_MESSAGE} "{first_letter}"'

        sql = f"""UPDATE users_data SET 
        first_letter='{first_letter}', 
        score={score},
        vocabulary='{vocabulary}'
        WHERE chat_id={chat_id}"""
        cursor.execute(sql)

        connect.commit()
    else:
        text_message = messages.ERROR_MESSAGE

    bot.send_message(chat_id, text_message, reply_markup=build_markup())


if __name__ == '__main__':
    while True:
        try:
            bot.polling()
        except Exception as e:
            print(e)
            sleep(15)