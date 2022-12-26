from telegram import Bot
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, ConversationHandler
from random import randint

bot = Bot(token='')
updater = Updater(token='')
dispatcher = updater.dispatcher

N = 120
MAX_CHOICE = 28

P_STEP, BOT_STEP, P_ERROR, B_CHOICE = range(4)

def start(update, context):
    context.bot.send_message(update.effective_chat.id,'На столе лежит 120 конфет.\nИграют два игрока, делая ход друг после друга.\n\
    Первый ход делаете Вы. За один ход можно забрать не более чем 28 конфет.\n\
    Победитель - тот, кто оставил на столе 0 конфет.')
    return P_STEP

def player_step(update, context):
    global N
    global now_play
    global player_choice
    now_play = 'Вы'
    context.bot.send_message(update.effective_chat.id, f"Конфет: {N}")
    context.bot.send_message(update.effective_chat.id, 'Сейчас Ваш ход, сколько возьмете конфет? (от 1 до 28 включительно)')
    player_choice = int(update.message.text)
    if player_choice > N:
        return B_CHOICE
    elif player_choice > 28 or player_choice < 1:
        return P_ERROR
    else:
        N -= player_choice
        if N > 0:
            return BOT_STEP
        else:
            winner(update, context, now_play)

def big_choice(update, context):
    global N
    global player_choice
    context.bot.send_message(update.effective_chat.id, f"Осталось всего {N} конфет, нельзя взять больше! Так сколько берете?")
    player_choice = int(update.message.text)
    if player_choice > N:
        return B_CHOICE
    elif player_choice > 28 or player_choice < 1:
        return P_ERROR
    else:
        N -= player_choice
        if N > 0:
            return BOT_STEP
        else:
            winner(update, context, now_play)

def player_error(update, context):
    global N
    global player_choice
    context.bot.send_message(update.effective_chat.id,'Можно взять только от 1 до 28 конфет, так сколько берете?')
    player_choice = int(update.message.text)
    if player_choice > N:
        return B_CHOICE
    elif player_choice > 28 or player_choice < 1:
        return P_ERROR
    else:
        N -= player_choice
        if N > 0:
            return BOT_STEP
        else:
            winner(update, context, now_play)

def bot_step(update, context):
    global N
    global MAX_CHOICE
    global now_play
    global player_choice
    now_play = 'бот'
    context.bot.send_message(update.effective_chat.id, f'Конфет: {N}')
    context.bot.send_message(update.effective_chat.id, 'Теперь мой ход! Я возьму...')
    if N <= MAX_CHOICE:
        bot_choice = N
    elif N % (MAX_CHOICE + 1):
        bot_choice = N % (MAX_CHOICE + 1)        
    else:
        bot_choice = MAX_CHOICE + 1 - player_choice
    context.bot.send_message(update.effective_chat.id, bot_choice)
    N -= bot_choice
    if N > 0:
        return P_STEP
    else:
        winner(update, context, now_play)

def winner(update, context, player):
   
    player = now_play
    context.bot.send_message(update.effective_chat.id, f'Победитель - {player}. Спасибо за игру!')
    return ConversationHandler.END

conv_handler = ConversationHandler(
                                    entry_points=[CommandHandler('start', start)],
                                    states={P_STEP: [MessageHandler(Filters.text ,player_step)],
                                            BOT_STEP: [MessageHandler(Filters.text, bot_step)],
                                            P_ERROR: [MessageHandler(Filters.text, player_error)],
                                            B_CHOICE: [MessageHandler(Filters.text, big_choice)]
                                        },
                                    fallbacks=[MessageHandler(Filters.text, winner)]
                                    )

dispatcher.add_handler(conv_handler)   

updater.start_polling()
updater.idle()

