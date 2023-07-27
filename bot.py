import telebot
from telebot import types

bot = telebot.TeleBot(token='placeholder')
name = 'Аноним'
HELP_TEXT = (
    'Этот бот знает следующие команды:'
    '\n/repo - выводит ссылку на репозиторий с исходным кодом;'
    '\n/help - вызывает этот список команд, вот так сюрприз!'
    '\n/start - знакомство с ботом и установка обращения к пользователю;'
    '\n/menu - главное меню бота;'
    '\n/photos - меню фотографий;'
    '\n/selfie - бот отправляет пользователю селфи;'
    '\n/school - бот отправляет пользователю школьное фото;'
    '\n/voices - меню голосовых сообщений;'
    '\n/gpt - бот отправляет голосовое сообщение про GPT;'
    '\n/love - бот отправляет голосовое сообщение про любовь;'
    '\n/sql - бот отправляет голосовое сообщение про SQL.'
)


# функции под команды
@bot.message_handler(content_types=['text'], commands=['repo'])
def repo(message):
    """ Выводит ссылку на исходный код. """

    bot.send_message(
        chat_id=message.chat.id,
        text='Здесь будет ссылка на репозиторий'
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
        text=f'Привет, {name}! Как к тебе обращаться?'
    )
    bot.register_next_step_handler(
        message=message,
        callback=acquaintance
    )


def acquaintance(message):
    """ Устанавлиевает обращение к пользователю. """

    global name
    name = message.text
    if name in ('Аноним', 'Анонимус', 'Anonymous'):
        bot.send_photo(
            chat_id=message.chat.id,
            caption='Желаешь остаться инкогнито? Очень хорошо.',
            photo=open('media/anonymous.jpg', 'rb')
        )
    bot.send_message(
        chat_id=message.chat.id,
        text=f'Отлично, привет ещё раз, {name}!'
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
    keyboard.add(key_photos)

    key_photos = types.InlineKeyboardButton(
        text='Меню голосовых сообщений',
        callback_data='voices_menu'
    )
    keyboard.add(key_photos)

    bot.send_message(
        chat_id=message.chat.id,
        text=f'Чем займёмся, {name}?',
        reply_markup=keyboard
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
        text=f'Что мне сделать, {name}?',
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
        text=f'О чём мне рассказать, {name}?',
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
        voice=open('media/audio_test.wav', 'rb'),
        caption=f'Crash-course по GPT для бабушек. И для тебя, {name}.'
    )


@bot.message_handler(content_types=['text'], commands=['sql'])
def send_voice_on_sql(message):
    """ Функция отправки голосового сообщения про SQL. """

    bot.send_voice(
        chat_id=message.chat.id,
        voice=open('media/audio_test.wav', 'rb'),
        caption='О различиях между SQL и NoSQL.'
    )


@bot.message_handler(content_types=['text'], commands=['love'])
def send_voice_on_love(message):
    """ Функция отправки голосового сообщения про любовь. """

    bot.send_voice(
        chat_id=message.chat.id,
        voice=open('media/audio_test.wav', 'rb'),
        caption=f'Послушай, {name}, сказ о любви.'
    )


# кнопочный менеджер
command_functions = {
    'main_menu': main_menu,
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


# петля
bot.polling(none_stop=True, interval=0)