from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters
from random import randint

# token = '5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU'
bot = Bot(token='5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU')
updater = Updater(token='5934547319:AAHs2zQ1MiBL1SdrApl-xwKnek_6xd219DU')
dispatcher = updater.dispatcher

a = 0
b = 1
# обучение бота

def start(update, context):
    context.bot.send_message(update.effective_chat.id, 'Хай! Сам чо как?')
    return a

def rand(update, context):
    context.bot.send_message(update.effective_chat.id, randint(1, 100))

def func(update, context):
    text = update.message.text
    if 'прив' in text.lower():
        context.bot.send_message(update.effective_chat.id, 'Салам пополам!')
    else:
        context.bot.send_message(update.effective_chat.id, 'Здороваться не учили??')

def how_are_you(update, context):
    text = update.message.text
    if 'норм' or 'хор' in text.lower():
        context.bot.send_message(update.effective_chat.id, 'Каеф ))')
    else:
        context.bot.send_message(update.effective_chat.id, 'Вот жаль ...')
    context.bot.send_message(update.effective_chat.id, 'Как погодка?')



start_handler = CommandHandler('start', start)
random_handler = CommandHandler('random', rand)
message_handler = MessageHandler(Filters.text, func)
message_handler = MessageHandler(Filters.text, how_are_you)
# message_handler = MessageHandler(Filters.text, func)
# message_handler = MessageHandler(Filters.text, func)
# message_handler = MessageHandler(Filters.text, func)

dispatcher.add_handler(start_handler)
dispatcher.add_handler(random_handler)
dispatcher.add_handler(message_handler)

#запуск и закрытие бота
updater.start_polling()
updater.idle()