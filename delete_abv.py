from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters

bot = Bot(token='')
updater = Updater(token='')
dispatcher = updater.dispatcher

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Привет!\n\nЯ умею удалять из твоих сообщений слова, в которых есть сочетание "абв"')
    context.bot.send_message(update.effective_chat.id, 'Напиши мне любое сообщение, и я верну его обратно без слов с "абв"')

def del_abv(update, context):
    text = update.message.text
    user_message = text.split()
    i = 0
    while i < len(user_message):
        if 'абв' in user_message[i].lower():
            del user_message[i]
            i -= 1
        i += 1
    user_message = ' '.join(user_message)
    context.bot.send_message(update.effective_chat.id, user_message)
    
start_handler = CommandHandler('start', start)
message_handler = MessageHandler(Filters.text, del_abv)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(message_handler)

updater.start_polling()
updater.idle()