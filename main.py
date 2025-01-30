from config import *
import telebot
import sqlite3

bot = telebot.TeleBot(TOKEN)


@bot.message_handler(commands=['start', "help"])
def start_message(message):
    bot.send_message(message.chat.id, 'Привет! Я бот. могу ответить на часто задаваемые вопросы. вопросы можно посмотреть по команте /avg_qestions')

@bot.message_handler(commands=['avg_qestions'])
def qa(message):
    bot.send_message(message.chat.id, 'Список часто задаваемых вопросов:')
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT questions FROM queans')
        for user in cursor.fetchall():
            bot.send_message(message.chat.id, user[0])   
        bot.send_message(message.chat.id, 'напишите номер вопроса на который вы бы хотели узнать ответ(начиная с нуля)')
        bot.register_next_step_handler(message, ans)
def ans(message):
    q = message.text
    with sqlite3.connect('database.db') as conn:
        cursor = conn.cursor()
        cursor.execute('SELECT answers FROM queans WHERE id = ?', (q,))
        bot.send_message(message.chat.id, cursor.fetchone()[0])

@bot.message_handler(func= lambda message: True)
def echo_all(message):
    f = message.text
    if "оформить" in f:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT answers FROM queans WHERE id = 0')
            bot.send_message(message.chat.id, cursor.fetchone())
    if "статус" in f:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT answers FROM queans WHERE id = 1')
            bot.send_message(message.chat.id, cursor.fetchone())
    if "отменит" in f:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT answers FROM queans WHERE id = 2')
            bot.send_message(message.chat.id, cursor.fetchone())
    if "брак" in f or "поврежден" in f:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT answers FROM queans WHERE id = 3')
            bot.send_message(message.chat.id, cursor.fetchone())
    if "связатся" in f:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT answers FROM queans WHERE id = 4')
            bot.send_message(message.chat.id, cursor.fetchone())
    if "информац" in f:
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('SELECT answers FROM queans WHERE id = 5')
            bot.send_message(message.chat.id, cursor.fetchone())
    words = ["оформить", "статус", "отменит", "брак", "связатся", "поврежден", "информац"]
    count = 0
    for word in words:
        if word not in f:
            count += 1
    if count == len(words):
        with sqlite3.connect('database.db') as conn:
            cursor = conn.cursor()
            cursor.execute('INSERT INTO queans (questions, answers) VALUES (?, ?)', (f, "none"))


if __name__ == '__main__':
    bot.polling()
