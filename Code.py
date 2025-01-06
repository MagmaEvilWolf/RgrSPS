import telebot
from telebot import types
import webbrowser
from pyexpat.errors import messages

bot = telebot.TeleBot('7279406794:AAHEuoNDMpkOC6cKRwP2emufano1Df5X1eM')

#@bot.message_handler(commands=['site','website'])
#def site(messages):
    #webbrowser.open('')

#@bot.message_handler(commands=['start'])
#def start(message):




@bot.message_handler(content_types=['photo', 'document'])
def get_photo(message):
    markup =types.InlineKeyboardMarkup()
    btn1= types.InlineKeyboardButton('Перейти по сылке откуда знания',url='https://www.youtube.com/watch?v=RpiWnPNTeww&list=PL0lO_mIqDDFUev1gp9yEwmwcy8SicqKbt&index=3')
    markup.row(btn1)
    btn2=types.InlineKeyboardButton('Удалить файл',callback_data='delete')
    btn3=types.InlineKeyboardButton('Изменить файл',callback_data='edit')
    markup.row(btn2,btn3)
    bot.reply_to(message,'Откуда браись знания', reply_markup=markup)

@bot.callback_query_handler(func= lambda callback:True)
def callback_message(callback):
    if callback.data == 'delete':
        bot.delete_message(callback.message.chat.id, callback.message.message_id-1)
    elif callback.data == 'edit':
        bot.edit_message_text('Edit text',callback.message.chat.id, callback.message.message_id)


@bot.message_handler(commands=['player'])
def main(message):
    bot.send_message(message.chat.id,message)

@bot.message_handler(commands=['start','main','hello'])
def main(message):
    bot.send_message(message.chat.id,f'Привет {message.from_user.first_name} {message.from_user.last_name}')

@bot.message_handler(commands=['help'])
def main(message):
    bot.send_message(message.chat.id,' <b>Инструкция</b> <em>для</em> <u>начинающих</u>', parse_mode='html')

@bot.message_handler()
def info(message):
    if message.text.lower() == 'привет':
        bot.send_message(message.chat.id, f'Привет {message.from_user.first_name} {message.from_user.last_name}')
    elif message.text.lower() == 'id':
        bot.reply_to(message, f'ID:{message.from_user.id} ')



bot.polling(none_stop=True)
