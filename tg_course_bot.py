import telebot
from telebot.types import InlineKeyboardMarkup, InlineKeyboardButton
import json

bot = telebot.TeleBot("5929423015:AAFU8to5_VT2-ffHxplJGRc0KT0Y3MDNKCk")
data = {}
num = 0


@bot.message_handler(commands=['start'])
def start(message):
    global num
    data[message.chat.id] = []
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Приступить к первому уроку.',callback_data=f'lesson_{num}'))
    markup.add(InlineKeyboardButton(text='Вернуться в меню.', callback_data='menu'))
    bot.send_message(message.chat.id, f"Добрый день!\nВас приветствует компания [Ваше название]!\nЖелаете пройти курс?", reply_markup = markup)


@bot.callback_query_handler(func=lambda call: True)
def callback_worker(call):
    global num
    if call.data == 'lesson_3':
        num = 0
        bot.delete_message(call.message.chat.id, call.message.message_id)
        bot.send_message(call.message.chat.id, "Уроки окончены! Ты молодец)")
        

    elif call.data == f'lesson_{num}':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        markup = InlineKeyboardMarkup()
        markup.add(InlineKeyboardButton(text='Оставить отзыв и перейти к следующему уроку.', callback_data='response'))

        with open('text.txt', 'r', encoding='utf-8') as file:
            text = file.readlines()[num].format(indent='\n')
        video = open(f'video_{num}.mp4', 'rb')
        bot.send_video(call.message.chat.id, video, caption=text, reply_markup = markup)

    elif call.data == 'response':
        bot.delete_message(call.message.chat.id, call.message.message_id)
        msg = bot.send_message(call.message.chat.id, f'Готов принять отзыв к уроку: ')
        bot.register_next_step_handler(msg, feedback)

    elif call.data == "menu":
        bot.send_message(call.message.chat.id, "MENU\nYes, it`s me!")


@bot.message_handler(content_type=['text'])
def feedback(message):
    global num, data
    bot.delete_message(message.chat.id, message.message_id - 1)
    bot.delete_message(message.chat.id, message.message_id)
    data[message.chat.id].append({
        'lesson': f'lesson_{num + 1}',
        'review': message.text,
    })
    with open('data.txt', 'w', encoding='utf-8') as outfile:
        json.dump(data, outfile, ensure_ascii=False)
    num += 1
    markup = InlineKeyboardMarkup()
    markup.add(InlineKeyboardButton(text='Приступить к следующему уроку', callback_data=f'lesson_{num}'))
    bot.send_message(message.from_user.id, "Спасибо за отзыв!", reply_markup = markup)


if __name__ == '__main__':
    bot.polling(none_stop=True, interval=0)