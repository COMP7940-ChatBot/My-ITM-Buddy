from telegram import Update, Bot, InlineKeyboardMarkup, InlineKeyboardButton
from telegram.ext import Updater, CommandHandler, MessageHandler, Filters, CallbackContext
import configparser
import logging
#import redis
import pymysql
import os 
import sys
#global redis1
from config import Development as Config
  


#[telegram.ext.Updater]("https://python-telegrambot.readthedocs.io/en/latest/telegram.ext.updater.html#telegram.ext.updater.Updater")

#[telegram.ext.Dispatcher]("https://pythontelegrambot.readthedocs.io/en/latest/telegram.ext.dispatcher.html#telegram.ext.Dispatcher")

#[telegram.ext.Handler]("http://python-telegrambot.readthedocs.io/en/latest/telegram.ext.messagehandler.html")

# Load your token and create an Updater for your Bot
    config = configparser.ConfigParser()
    #config.read('config.ini')
    #config.read('config.py')
    #updater = Updater(token=(Config.API_KEY), use_context=True)
    updater = Updater(Config.API_KEY, use_context=True)
    dispatcher = updater.dispatcher

    #global redis1
    #redis1 = redis.Redis(host=(Config.HOST), password=(Config.PASSWORD), port=(Config.REDISPORT))
    print("abc")
    TOKEN = Config.API_KEY
    print(TOKEN) 
    OWNER_ID = int(Config.OWNER_ID)
    print(OWNER_ID)
    #host = Config.HOST
    ##password = Config.PASSWORD
    #port = Config.REDISPORT
    #print(host)
    #print(password)
    #print(port)

    db = pymysql.connect(host="database-2.ckqwwshghlpj.ap-east-1.rds.amazonaws.com", user="administrator", password="administrator", port=3298)
    #db = pymysql.connect('database-2.ckqwwshghlpj.ap-east-1.rds.amazonaws.com', 'administrator', 'administrator', '3298')
    cursor = db.cursor()
    cursor
    cursor.execute("select version()")

    data = cursor.fetchone()
    print(data)

    sql = '''use Test_Schema'''
    cursor.execute(sql)
    sql = '''SELECT * FROM Persons'''
    cursor.execute(sql)
    data = cursor.fetchall()


    print(data)

    logging.basicConfig(format='%(asctime)s - %(name)s - %(levelname)s - %(message)s', level=logging.INFO)
    
    dispatcher.add_handler(CommandHandler("start", start))
    dispatcher.add_handler(MessageHandler(Filters.text & (~Filters.command), echo))
    dispatcher.add_handler(CommandHandler("add", add))
    dispatcher.add_handler(CommandHandler("help", help_command))
    dispatcher.add_handler(CommandHandler("hello", hello_command))
    dispatcher.add_handler(CommandHandler('info', info))

    updater.start_polling()
    updater.idle()


def info(update: Update, context: CallbackContext) -> None:
    """Send a message with ITM info as an inline keyboard markup."""
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id, 'ITM Info',
        reply_markup=InlineKeyboardMarkup([
            [InlineKeyboardButton('ITM Website', url='https://www.comp.hkbu.edu.hk/msc/itm/en/')],
            [InlineKeyboardButton('Curriculum', url='https://www.comp.hkbu.edu.hk/msc/itm/en/curriculum.php')],
            [InlineKeyboardButton('Contact', url='https://www.comp.hkbu.edu.hk/msc/itm/tc/contact.php')],
            [InlineKeyboardButton('Prospectus', url='https://www.comp.hkbu.edu.hk/msc/msc_booklet.pdf?4')]
        ])
    )


def start(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /start is issued."""
    bot = context.bot
    chat_id = update.effective_chat.id
    bot.send_message(chat_id=chat_id, text="Welcome to ITM Buddy! Please find the following functions available:")
    bot.send_message(chat_id=chat_id, text="(1) Command /hello : say hello to us 🙈 ")
    bot.send_message(chat_id=chat_id, text="(2) Command /gradreq <studentID> : Check your study progression")   
    bot.send_message(chat_id=chat_id, text="(3) Command /course <course> :  Check information for a specific course in ITM")
    bot.send_message(chat_id=chat_id, text="(4) Command /core :  Check the list and schedule of the core courses for 2022-2023")
    bot.send_message(chat_id=chat_id, text="(5) Command /elective :  Check the list and schedule of the elective courses available in 2022-2023")
    bot.send_message(chat_id=chat_id, text="(6) Command /map <buildingshortname> :  Check the location of a building")
    bot.send_message(chat_id=chat_id, text="(7) Command /print :  Check the location for the printer service")   
    bot.send_message(chat_id=chat_id, text="(8) Command /eat :  Check the location for the canteen") 
    bot.sendMessage(chat_id=chat_id, text="(9) Command /study :  Check the location for the study place, such as library, learning common, computer room")
    bot.sendMessage(chat_id=chat_id, text="(10) Command /help :  Check if you have further enquiry")

#def echo(update: Update, context: CallbackContext) -> None:
    #"""Respond to the user's message with the same message in uppercase."""
    #bot = context.bot
    #reply_message = update.message.text.upper()
    #logging.info("Update: " + str(update))
    #logging.info("context: " + str(context))
    #bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def echo(update: Update, context: CallbackContext) -> None:
    """Respond to the user's message with a greeting."""
    bot = context.bot
    user_name = update.message.from_user.first_name
    reply_message = f'Good day, {user_name}! This is My ITM Buddy. Please use the /start command to begin your journey with the chatbot.'
    bot.send_message(chat_id=update.effective_chat.id, text=reply_message)

def help_command(update: Update, context: CallbackContext) -> None: 
    """Send a message when the command /help is issued."""
    bot = context.bot
    bot.send_message(chat_id=update.effective_chat.id, text='Helping you helping you.\nIf you have further inquiries, please contact us during office hours at Telephone: +852 3411 7079 or Email: itm@comp.hkbu.edu.hk..')


#def hello_command(update: Update, context: CallbackContext) -> None:
    #"""Send a message when the command /hello is issued with an argument."""
    #bot = context.bot
    #try:
        #msg = context.args[0] # /hello keyword <-- this should store the keyword
        #bot.send_message(chat_id=update.effective_chat.id, text='Good day, '+msg+'! This is Alvin_bot')
    #except (IndexError, ValueError):
        #bot.send_message(chat_id=update.effective_chat.id, text='Usage: /hello <keyword>')

def hello_command(update: Update, context: CallbackContext) -> None:
    """Respond to the /hello command with a greeting message."""
    bot = context.bot
    user_name = update.message.from_user.first_name
    reply_message = f'Good day, {user_name}! This is My ITM Buddy.'
    bot.send_message(chat_id=update.effective_chat.id, text=reply_message)


def add(update: Update, context: CallbackContext) -> None:
    """Send a message when the command /add is issued."""
    try:
        print(1)
        #global redis1
        print(2)
        logging.info(context.args[0])
        print(3)
        msg = context.args[0] # /add keyword <-- this should store the keyword
        print(4)

        #redis1.incr(msg)
        #update.message.reply_text('You have said ' + msg + ' for ' + redis1.get(msg).decode('UTF-8') + ' times.')
    except (IndexError, ValueError):
        update.message.reply_text('Usage: /add <keyword>')


if __name__ == '__main__':
    main()