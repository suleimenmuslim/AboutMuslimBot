

import telebot
import re
import sys
import os
from telebot import types
from telebot.types import InputMediaPhoto, BotCommand
from content import CONTENT, achievs , project_ratings
from google import genai

token_bot = os.getenv("TOKEN_BOT")
Gemini_key = os.getenv("GEMINI_key")


    
debug_mode=False
if len(sys.argv) > 1 and sys.argv[1] == 'debug':
    debug_mode = True
    print("⚠️ Бот запущен в режиме отладки (debug mode)")


def log_action(action_text):
    if debug_mode:
        print(f"log : {action_text}")

bot=telebot.TeleBot(token_bot)

def disable_ai(chat_id):
    ai_mode[chat_id] = False


ai_mode={}
client = genai.Client(api_key=Gemini_key)


rate_mode={}




@bot.message_handler(commands=['start'])
def start(message):
    bot.send_message(message.chat.id, '👋 Добро пожаловать в портфолио-бота Муслима!\n\nЗдесь вы можете узнать обо мне, моих проектах, достижениях и пообщаться с ИИ-ассистентом.\n\n👇 Выберите интересующий раздел:', reply_markup=menu())








def menu():
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)

    markup.add('👤Обо мне', '🎯Цель', '🖥️Путь в IT')
    markup.add('🧑‍🏫Ментор', '📈Прогресс', '👟Хобби')
    markup.add('🏆Достижения', '🔗GitHub', '🤖ИИ')
    markup.add('⭐Оценка проектов', 'ℹ️Info', '📞Контакты' )
    

    return markup

def ai_menu():
    markup = types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('❌Выйти из ИИ')
    return markup


def rating_menu():
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⭐ StudyApp')
    markup.add('⭐ DrinkH2O')
    markup.add('⭐ CurrencyBot')
    return markup
def pro_menu():
    markup=types.ReplyKeyboardMarkup(resize_keyboard=True)
    markup.add('⭐ 1', '⭐ 2', '⭐ 3', '⭐ 4', '⭐ 5')
    

    return markup


@bot.message_handler(func=lambda m: m.text == '⭐Оценка проектов')
def rate_handler(message):
    log_action("Пользователь выбрал '⭐Оценка проектов'")
    ratings = project_ratings.get(message.chat.id, {})
    study = ratings.get("StudyApp", "Нет оценки")
    drink = ratings.get("DrinkH2O", "Нет оценки")
    currency = ratings.get("CurrencyBot", "Нет оценки")
    bot.send_message(message.chat.id, f'⭐Оценка проектов (1-5) : \n📚StudyApp - {study}\n💧DrinkH2O - {drink}\n💱CurrencyBot - {currency}', reply_markup=rating_menu())


@bot.message_handler(func=lambda m: m.text in ['⭐ StudyApp' , '⭐ DrinkH2O', '⭐ CurrencyBot'])
def rate_project(message):
    project = message.text.replace('⭐ ', '')
    rate_mode[message.chat.id] = project 
    log_action(f'Пользователь выбрал {project}')
    bot.send_message(message.chat.id, f"Оцените {project} ", reply_markup=pro_menu())



@bot.message_handler(func=lambda m: m.text in ['⭐ 1', '⭐ 2', '⭐ 3', '⭐ 4', '⭐ 5'])
def set_rating(message):
    
    score = int(message.text[-1])
    log_action(f'Пользователь выбрал {score}')

    
    if message.chat.id not in rate_mode:
        return
    if message.chat.id not in project_ratings:
        project_ratings[message.chat.id]={}
    project = rate_mode[message.chat.id]




    project_ratings[message.chat.id][project]=score
    
    
    ratings = project_ratings.get(message.chat.id, {})

    

    study = ratings.get("StudyApp", "Нет оценки")
    drink = ratings.get("DrinkH2O", "Нет оценки")
    currency = ratings.get("CurrencyBot", "Нет оценки")
    
    bot.send_message(message.chat.id, f"⭐Спасибо : \nStudyApp - {study}\nDrinkH2O - {drink} \nCurrencyBot - {currency}", reply_markup=menu())
    del rate_mode[message.chat.id]





@bot.message_handler(func=lambda m: m.text == '👤Обо мне')
def about_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '👤Обо мне'")
    try:
        with open('photos/about_me.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, CONTENT["about"], reply_markup=menu())


@bot.message_handler(func=lambda m: m.text == '🎯Цель')
def goal_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '🎯Цель'")
    try:
        with open('photos/goal.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, CONTENT["goal"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '🖥️Путь в IT')
def it_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '🖥️Путь в IT'")
    try:
        with open('photos/road_it.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, CONTENT["it"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '🧑‍🏫Ментор')
def mentor_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '🧑‍🏫Ментор'")
    bot.send_message(message.chat.id, CONTENT["mentor"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '📈Прогресс')
def progress_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '📈Прогресс'")
    try:
        with open('photos/IT.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, CONTENT["progress"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '👟Хобби')
def hobby_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '👟Хобби'")
    try:
        with open('photos/hobby.jpg', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, CONTENT["hobbies"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '🏆Достижения')
def achievements_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '🏆Достижения'")
    bot.send_message(message.chat.id, CONTENT["achievements"])
    try:
        with open('photos/study_app.png', 'rb') as photo:
            bot.send_photo(message.chat.id, photo)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, achievs["study_app"])
    try:
        with open('photos/DrinkH2O (1).png', 'rb') as d1, open('photos/DrinkH2O (2).png', 'rb') as d2:
            media1 = [InputMediaPhoto(d1), InputMediaPhoto(d2)]
            bot.send_media_group(message.chat.id, media1)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, achievs["DrinkH2O"])
    try:
        with open('photos/CurrencyBot (1).png', 'rb') as c1, open('photos/CurrencyBot (2).png', 'rb') as c2:
            media2 = [InputMediaPhoto(c1), InputMediaPhoto(c2)]
            bot.send_media_group(message.chat.id, media2)
    except FileNotFoundError:
        bot.send_message(message.chat.id, "Файл не найден")
    bot.send_message(message.chat.id, achievs["CurrencyBot"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '🔗GitHub')
def github_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '🔗GitHub'")
    bot.send_message(message.chat.id, CONTENT["github"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '🤖ИИ')
def ai_handler(message):
    log_action("Пользователь выбрал '🤖ИИ'")
    ai_mode[message.chat.id] = True
    bot.send_message(message.chat.id, CONTENT["ai"], reply_markup=ai_menu())

@bot.message_handler(func=lambda m: m.text == '❌Выйти из ИИ')
def exit_ai(message):
    if not ai_mode.get(message.chat.id, False):
        bot.send_message(message.chat.id, "Вы не входили в режим ИИ",reply_markup=menu())
        return
    ai_mode[message.chat.id] = False
    bot.send_message(message.chat.id, "Вы вышли из режима ИИ.",reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == 'ℹ️Info')
def info_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал 'ℹ️Info'")
    bot.send_message(message.chat.id, CONTENT["info"], reply_markup=menu())

@bot.message_handler(func=lambda m: m.text == '📞Контакты')
def contacts_handler(message):
    disable_ai(message.chat.id)
    log_action("Пользователь выбрал '📞Контакты'")
    bot.send_message(message.chat.id, CONTENT['contacts'], reply_markup=menu())




@bot.message_handler(commands=['about'])
def about_command(message):
    about_handler(message)

@bot.message_handler(commands=['goal'])
def goal_command(message):
    goal_handler(message)

@bot.message_handler(commands=['it'])
def it_command(message):
    it_handler(message)

@bot.message_handler(commands=['mentor'])
def mentor_command(message):
    mentor_handler(message)

@bot.message_handler(commands=['progress'])
def progress_command(message):
    progress_handler(message)

@bot.message_handler(commands=['hobby'])
def hobby_command(message):
    hobby_handler(message)

@bot.message_handler(commands=['achievements'])
def achievements_command(message):
    achievements_handler(message)

@bot.message_handler(commands=['github'])
def github_command(message):
    github_handler(message)
@bot.message_handler(commands=['ai'])
def ai_command(message):
    ai_handler(message)
@bot.message_handler(commands=['info'])
def info_command(message):
    info_handler(message)

@bot.message_handler(commands=['contacts'])
def contacts_command(message):
    contacts_handler(message)

@bot.message_handler(commands=['rate'])
def rate_command(message):
    rate_handler(message)



@bot.message_handler(commands=['exitai'])
def exit_command(message):
    exit_ai(message)






bot.set_my_commands([
    BotCommand("start", "🚀 Старт"),
    BotCommand("about", "👤 Обо мне"),
    BotCommand("goal", "🎯 Цель"),
    BotCommand("it", "🖥️ Путь в IT"),
    BotCommand("mentor", "🧑‍🏫 Ментор"),
    BotCommand("progress", "📈 Прогресс"),
    BotCommand("hobby", "👟 Хобби"),
    BotCommand("achievements", "🏆 Достижения"),
    BotCommand("github", "🔗 GitHub"),
    BotCommand("contacts", "📞 Контакты"),
    BotCommand("ai", "🤖ИИ"),
    BotCommand("rate", "⭐Оценка проектов"),
    BotCommand("info", "ℹ️ Информация"),
    BotCommand("exitai", "❌Выйти из ИИ (если Вы вошли)")
])


@bot.message_handler(func=lambda m: ai_mode.get(m.chat.id))
def gemini_chat(message):
    if len(message.text) > 1000:
        bot.send_message(message.chat.id, "Слишком длинное сообщение.")
        return


    log_action(f"Запрос отправлен в Gemini: {message.text}")
    
    
    prompt = f"""
Ты — персональный ИИ-ассистент Муслима. Отвечай кратко и дружелюбно на основе этой информации, Если ответа нет в информации — скажи:
"Я не знаю этого о Муслиме.":
{CONTENT}


Вопрос пользователя:
{message.text}

Проекты:
{achievs}
"""

    try:

        response = client.models.generate_content(
            model="gemini-2.5-flash",
            contents=prompt
        )

        bot.send_message(
            message.chat.id,
            response.text, reply_markup=ai_menu()
        )

    except Exception as e:
        print('error : ', e)
        if "429" in str(e):
            bot.send_message(message.chat.id, "Лимит запросов к ИИ временно исчерпан, попробуйте через несколько минут")
        else:
            bot.send_message(message.chat.id, f"Извините, сей час ИИ временно недоступен.", reply_markup=ai_menu())

    








@bot.message_handler(func=lambda m: m.text and not ai_mode.get(m.chat.id) and not m.text.startswith('/'))
def re_handler(message):
    text=message.text.lower()
    if re.search(r'возраст| лет|сколько тебе лет', text):
        bot.send_message(message.chat.id, 'Муслиму 15 лет', reply_markup=menu())
    elif re.search(r'город|место проживания|где живет', text):
        bot.send_message(message.chat.id, 'Муслим живет в городе Уральск📍', reply_markup=menu())
    elif re.search(r"баскетбол", text):
        bot.send_message(message.chat.id, CONTENT["hobbies"], reply_markup=menu())
    elif re.search(r"ссылка на github|ссылка на гитхаб", text):
        bot.send_message(message.chat.id, CONTENT["github"], reply_markup=menu())
    elif re.search(r"ии|ai|gemini", text):
        bot.send_message(message.chat.id,"Нажмите кнопку 🤖ИИ для общения с искусственным интеллектом.")
    else:
        bot.send_message(message.chat.id, "🤔 Я не понял запрос.\nИспользуйте лоступные кнопки меню, команды или нажмите 🤖ИИ для общения с ассистентом.", reply_markup=menu())





try:
    bot.infinity_polling()
except Exception as e:
    print(f"Произошла ошибка: {e}")
