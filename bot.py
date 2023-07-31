import os
import sqlite3
import telebot

from dotenv import load_dotenv
from telebot import types
from typing import Tuple


HELP_TEXT = (
    'Этот бот знает следующие команды:'
    '\n/repo - выводит ссылку на репозиторий с исходным кодом;'
    '\n/help - вызывает этот список команд, вот так сюрприз!'
    '\n/start - знакомство с ботом и установка обращения к пользователю;'
    '\n/menu - главное меню бота;'
    '\n/hobby - бот показывает хобби;'
    '\n/photos - меню фотографий;'
    '\n/selfie - бот отправляет пользователю селфи;'
    '\n/school - бот отправляет пользователю школьное фото;'
    '\n/voices - меню голосовых сообщений;'
    '\n/gpt - бот отправляет голосовое сообщение про GPT;'
    '\n/love - бот отправляет голосовое сообщение про любовь;'
    '\n/sql - бот отправляет голосовое сообщение про SQL.'
)

load_dotenv()

BOT_TOKEN = os.getenv('SET_SAILS_BOT_TOKEN')
bot = telebot.TeleBot(token=BOT_TOKEN)


# база данных
def create_database():
    """ Создание БД. """
    conn = sqlite3.connect('usernames.db')
    cur = conn.cursor()
    cur.execute(
        """CREATE TABLE IF NOT EXISTS users(
        user_id INT PRIMARY KEY,
        name TEXT);"""
    )
    conn.commit()


def add_to_database(user_data: Tuple[int, str]) -> None:
    """ Добавление имени пользователя в БД. """

    conn = sqlite3.connect('usernames.db')
    cur = conn.cursor()

    # проверяем наличие записи
    cur.execute(
        'SELECT count(*) FROM users WHERE user_id = ?', (user_data[0],)
    )

    # если нет такой записи
    if cur.fetchone()[0] == 0:
        cur.execute('INSERT INTO users VALUES(?, ?);', user_data)
        conn.commit()

    # если такая запись есть
    else:
        cur.execute(
            'UPDATE users SET name = ? WHERE user_id = ?;',
            (user_data[1], user_data[0])
        )
        conn.commit()


def read_from_database(user_id: int):
    """ Чтение имени пользователя из БД. """

    conn = sqlite3.connect('usernames.db')
    cur = conn.cursor()
    cur.execute(
        'SELECT name FROM users WHERE user_id = ?;', (user_id,)
    )

    # на случай, если что-то случится с БД
    name = cur.fetchone()
    if name is None:
        return 'Пользователь',

    return name


# функции под команды
@bot.message_handler(content_types=['text'], commands=['repo'])
def repo(message):
    """ Выводит ссылку на исходный код. """

    bot.send_message(
        chat_id=message.chat.id,
        text=(
            'https://github.com/andrzej-skuridin/'
            'yandex-bot-for-teenagers-test-assigment.git'
        )
    )


@bot.message_handler(content_types=['text'], commands=['help'])
def helper(message):
    """ Выводит список команд. """

    bot.send_message(
        chat_id=message.chat.id,
        text=HELP_TEXT
    )


@bot.message_handler(content_types=['text'], commands=['start'])
def start(message):
    """ Здоровается и предлагает выбрать обращение к пользователю. """

    bot.send_message(
        chat_id=message.chat.id,
        text='Привет, пользователь! Как к тебе обращаться?'
    )
    bot.register_next_step_handler(
        message=message,
        callback=acquaintance
    )


def acquaintance(message):
    """ Устанавливает обращение к пользователю. """

    user_id = message.from_user.id
    name = message.text
    add_to_database(user_data=(user_id, name))

    if name in ('Аноним', 'Анонимус', 'Anonymous'):
        bot.send_photo(
            chat_id=message.chat.id,
            caption='Желаешь остаться инкогнито? Очень хорошо.',
            photo=open('media/anonymous.jpg', 'rb')
        )
    bot.send_message(
        chat_id=message.chat.id,
        text='Отлично, привет ещё раз, '
             f'{read_from_database(user_id=message.chat.id)[0]}!'
             '\nЧтобы открыть главное меню, введи "/menu".'
             '\nЧтобы открыть список команд, введи "/help".'
    )


@bot.message_handler(content_types=['text'], commands=['menu'])
def main_menu(message):
    """ Функция главного меню. """

    keyboard = types.InlineKeyboardMarkup()

    key_photos = types.InlineKeyboardButton(
        text='Меню фотографий',
        callback_data='photos_menu'
    )

    key_voices = types.InlineKeyboardButton(
        text='Меню голосовых сообщений',
        callback_data='voices_menu'
    )

    key_hobby = types.InlineKeyboardButton(
        text='Показать хобби',
        callback_data='hobby'
    )
    keyboard.add(key_photos, key_voices)
    keyboard.add(key_hobby)

    bot.send_message(
        chat_id=message.chat.id,
        text='Чем займёмся, '
             f'{read_from_database(user_id=message.chat.id)[0]}?',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'], commands=['hobby'])
def send_hobby(message):
    """ Функция отправки видео ботом пользователю. """

    bot.send_video(
        chat_id=message.chat.id,
        video=open('media/music.mp4', 'rb'),
        caption='Поставьте скорость на 1.2 и берегите уши 🙉',
    )


@bot.message_handler(content_types=['text'], commands=['photos'])
def photos_menu(message):
    """ Функция меню фотографий. """

    keyboard = types.InlineKeyboardMarkup()

    key_selfie = types.InlineKeyboardButton(
        text='Показать селфи',
        callback_data='selfie'
    )

    key_school = types.InlineKeyboardButton(
        text='Показать школьное фото',
        callback_data='school'
    )

    key_main_menu = types.InlineKeyboardButton(
        text='В главное меню',
        callback_data='main_menu'
    )

    keyboard.add(key_selfie, key_school)
    keyboard.add(key_main_menu)

    bot.send_message(
        chat_id=message.chat.id,
        text='Что мне сделать, '
             f'{read_from_database(user_id=message.chat.id)[0]}?',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'], commands=['voices'])
def voices_menu(message):
    """ Функция меню голосовых сообщений. """

    keyboard = types.InlineKeyboardMarkup()

    key_selfie = types.InlineKeyboardButton(
        text='Про любовь',
        callback_data='love'
    )

    key_gpt = types.InlineKeyboardButton(
        text='Про GPT',
        callback_data='gpt'
    )

    key_sql = types.InlineKeyboardButton(
        text='Про (No)SQL',
        callback_data='sql'
    )

    key_main_menu = types.InlineKeyboardButton(
        text='В главное меню',
        callback_data='main_menu'
    )

    keyboard.add(
        key_selfie,
        key_gpt,
        key_sql,
        key_main_menu
    )

    bot.send_message(
        chat_id=message.chat.id,
        text='О чём мне рассказать, '
             f'{read_from_database(user_id=message.chat.id)[0]}?',
        reply_markup=keyboard
    )


@bot.message_handler(content_types=['text'], commands=['selfie'])
def send_selfie(message):
    """ Функция отправки селфи ботом пользователю. """

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open('media/selfie.jpg', 'rb'),
        caption='На фоне конкурирующей организации 😄'
    )


@bot.message_handler(content_types=['text'], commands=['school'])
def send_school_photo(message):
    """ Функция отправки школьного фото ботом пользователю. """

    bot.send_photo(
        chat_id=message.chat.id,
        photo=open('media/school.jpg', 'rb'),
        caption='Это единственная фотка с выпускного, на которой я есть 🤣. '
                'Второй ряд, крайний справа.'
    )


@bot.message_handler(content_types=['text'], commands=['gpt'])
def send_voice_on_gpt(message):
    """ Функция отправки голосового сообщения про GPT. """

    bot.send_voice(
        chat_id=message.chat.id,
        voice=open('media/audio_gpt.wav', 'rb'),
        caption='Crash-course по GPT для бабушек. И для тебя, '
                f'{read_from_database(user_id=message.chat.id)[0]}.'
    )


@bot.message_handler(content_types=['text'], commands=['sql'])
def send_voice_on_sql(message):
    """ Функция отправки голосового сообщения про SQL. """

    bot.send_voice(
        chat_id=message.chat.id,
        voice=open('media/audio_sql.wav', 'rb'),
        caption='О различиях между SQL и NoSQL.'
    )


@bot.message_handler(content_types=['text'], commands=['love'])
def send_voice_on_love(message):
    """ Функция отправки голосового сообщения про любовь. """

    bot.send_voice(
        chat_id=message.chat.id,
        voice=open('media/audio_love.wav', 'rb'),
        caption='Послушай, '
                f'{read_from_database(user_id=message.chat.id)[0]}'
                ', сказ о любви.'
    )


# кнопочный менеджер
command_functions = {
    'main_menu': main_menu,
    'hobby': send_hobby,
    'photos_menu': photos_menu,
    'voices_menu': voices_menu,
    'selfie': send_selfie,
    'school': send_school_photo,
    'love': send_voice_on_love,
    'gpt': send_voice_on_gpt,
    'sql': send_voice_on_sql,
}


@bot.callback_query_handler(func=lambda call: True)
def callback_catcher(call):
    """ Перехватчик команд с кнопок. """

    if call.data in command_functions:
        command_functions[call.data](call.message)
    else:
        pass


# запуск
create_database()
bot.polling(none_stop=True, interval=0)
